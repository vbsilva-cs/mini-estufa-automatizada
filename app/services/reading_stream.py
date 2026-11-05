from __future__ import annotations

from datetime import UTC, datetime

from app.domain.entities import Leitura


class ReadingStreamService:
    def __init__(self, dataset: list[Leitura]) -> None:
        self.dataset = dataset

    def current(self, cursor: int) -> Leitura:
        return self.dataset[self._normalize_cursor(cursor)]

    def next_cursor(self, cursor: int) -> int:
        return (self._normalize_cursor(cursor) + 1) % len(self.dataset)

    def _normalize_cursor(self, cursor: int) -> int:
        if not self.dataset:
            raise ValueError("dataset vazio")
        return cursor % len(self.dataset)

    @staticmethod
    def elapsed_label(last_refresh_iso: str | None) -> str:
        if not last_refresh_iso:
            return "há 12 s"

        last_refresh = datetime.fromisoformat(last_refresh_iso)
        elapsed_seconds = max(int((datetime.now(UTC) - last_refresh).total_seconds()), 0)
        if elapsed_seconds < 60:
            return f"há {elapsed_seconds} s"
        return f"há {elapsed_seconds // 60} min"
