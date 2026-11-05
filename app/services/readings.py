from app.domain.entities import Leitura


class ReadingCycleService:
    def __init__(self, dataset: list[Leitura]) -> None:
        if not dataset:
            raise ValueError("dataset vazio")

        self._dataset = dataset
        self.reset()

    def reset(self) -> None:
        self._cursor = 0
        self._current = self._dataset[-1]

    @property
    def current(self) -> Leitura:
        return self._current

    def advance(self) -> Leitura:
        self._current = self._dataset[self._cursor]
        self._cursor = (self._cursor + 1) % len(self._dataset)
        return self._current
