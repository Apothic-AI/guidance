from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Any

try:
    from re import _constants as re_constants  # type: ignore[attr-defined]
    from re import _parser as re_parser  # type: ignore[attr-defined]
except ImportError:  # pragma: no cover
    import sre_constants as re_constants
    import sre_parse as re_parser

@dataclass(frozen=True)
class NormalizedTopLogprob:
    token: str
    logprob: float | None
    token_bytes: bytes | None


@dataclass(frozen=True)
class NormalizedTokenLogprob:
    token: str
    logprob: float | None
    token_bytes: bytes | None
    top_logprobs: tuple[NormalizedTopLogprob, ...]


def _read_field(value: Any, field: str) -> Any:
    if isinstance(value, dict):
        return value.get(field)
    return getattr(value, field, None)


def _coerce_float(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            return None
        try:
            return float(stripped)
        except ValueError:
            return None
    return None


def _coerce_token_bytes(value: Any) -> bytes | None:
    if value is None:
        return None
    if isinstance(value, (bytes, bytearray)):
        return bytes(value)
    if isinstance(value, list):
        out: list[int] = []
        for entry in value:
            if not isinstance(entry, int):
                return None
            out.append(entry)
        try:
            return bytes(out)
        except ValueError:
            return None
    return None


def _normalize_top_logprobs(raw: Any) -> tuple[NormalizedTopLogprob, ...]:
    if not isinstance(raw, list):
        return ()
    normalized: list[NormalizedTopLogprob] = []
    for entry in raw:
        token = str(_read_field(entry, "token") or "")
        normalized.append(
            NormalizedTopLogprob(
                token=token,
                logprob=_coerce_float(_read_field(entry, "logprob")),
                token_bytes=_coerce_token_bytes(_read_field(entry, "bytes")),
            )
        )
    return tuple(normalized)


def extract_chunk_logprob_tokens(choice: Any) -> list[NormalizedTokenLogprob]:
    """Extract logprob tokens from OpenAI/OpenRouter-like chunk choice payloads."""
    logprobs = _read_field(choice, "logprobs")
    content = _read_field(logprobs, "content")
    if not isinstance(content, list):
        return []

    normalized: list[NormalizedTokenLogprob] = []
    for entry in content:
        token = str(_read_field(entry, "token") or "")
        normalized.append(
            NormalizedTokenLogprob(
                token=token,
                logprob=_coerce_float(_read_field(entry, "logprob")),
                token_bytes=_coerce_token_bytes(_read_field(entry, "bytes")),
                top_logprobs=_normalize_top_logprobs(_read_field(entry, "top_logprobs")),
            )
        )
    return normalized


def probability_from_logprob(logprob: float | None) -> float:
    if logprob is None or not math.isfinite(logprob):
        return float("nan")
    try:
        return math.exp(logprob)
    except OverflowError:
        return float("nan")


def logprob_from_probability(probability: float) -> float | None:
    if not math.isfinite(probability) or probability <= 0:
        return None
    return math.log(probability)


class CaptureLogProbAccumulator:
    """Accumulates token-level logprobs and computes capture-level logprobs."""

    def __init__(self) -> None:
        self._segments: list[tuple[str, float | None]] = []

    def add(self, token_text: str, logprob: float | None) -> None:
        if token_text:
            self._segments.append((token_text, logprob))

    def logprob_for_text(self, text: str) -> float | None:
        if text == "":
            return 0.0
        if not self._segments:
            return None

        cursor = 0
        total = 0.0
        for segment_text, segment_logprob in self._segments:
            if cursor >= len(text):
                break
            if not text.startswith(segment_text, cursor):
                return None
            cursor += len(segment_text)
            if segment_logprob is None:
                return None
            total += segment_logprob
        if cursor != len(text):
            return None
        return total


@dataclass(frozen=True)
class RegexStopUpdate:
    emit_text: str
    matched: bool = False
    stop_text: str | None = None
    rewind_characters: int = 0


class StreamingRegexStopMatcher:
    """Client-side stop-regex matcher for streamed text chunks."""

    def __init__(self, pattern: str) -> None:
        try:
            self._regex = re.compile(pattern)
        except re.error as exc:
            raise ValueError(f"Invalid stop_regex pattern: {pattern}") from exc
        self._raw_generated = ""
        self._emitted_len = 0
        self._matched = False
        self._stop_text: str | None = None

        max_width = re_parser.parse(pattern).getwidth()[1]
        if max_width >= re_constants.MAXREPEAT:
            self._max_match_width: int | None = None
        else:
            self._max_match_width = int(max_width)

    def _earliest_match_bounds(self) -> tuple[int, int] | None:
        first = self._regex.search(self._raw_generated)
        if first is None:
            return None
        start = first.start()
        # Tie-break same-start alternatives by earliest end.
        for end in range(start, len(self._raw_generated) + 1):
            if self._regex.fullmatch(self._raw_generated[start:end]) is not None:
                return start, end
        return start, first.end()

    def _safe_emit_end(self) -> int:
        if self._max_match_width is None:
            return 0
        if self._max_match_width <= 1:
            return len(self._raw_generated)
        return max(0, len(self._raw_generated) - self._max_match_width + 1)

    def _emit_until(self, end: int) -> str:
        bounded_end = max(self._emitted_len, min(end, len(self._raw_generated)))
        emit_text = self._raw_generated[self._emitted_len : bounded_end]
        self._emitted_len = bounded_end
        return emit_text

    def feed(self, text: str) -> RegexStopUpdate:
        if self._matched:
            return RegexStopUpdate(emit_text="", matched=True, stop_text=self._stop_text, rewind_characters=0)

        self._raw_generated += text
        match_bounds = self._earliest_match_bounds()
        if match_bounds is not None:
            match_start, match_end = match_bounds
            emit_text = self._emit_until(match_start)
            self._matched = True
            self._stop_text = self._raw_generated[match_start:match_end]
            rewind_characters = len(self._raw_generated) - match_start
            return RegexStopUpdate(
                emit_text=emit_text,
                matched=True,
                stop_text=self._stop_text,
                rewind_characters=rewind_characters,
            )

        emit_text = self._emit_until(self._safe_emit_end())
        return RegexStopUpdate(emit_text=emit_text)

    def finish(self) -> RegexStopUpdate:
        if self._matched:
            return RegexStopUpdate(emit_text="", matched=True, stop_text=self._stop_text, rewind_characters=0)
        return RegexStopUpdate(emit_text=self._emit_until(len(self._raw_generated)))

    @property
    def emitted_text(self) -> str:
        return self._raw_generated[: self._emitted_len]

    @property
    def matched(self) -> bool:
        return self._matched

    @property
    def stop_text(self) -> str | None:
        return self._stop_text
