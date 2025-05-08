from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Any,
    Iterable,
)

from horsebox.model import TDocument


class Collector(ABC):
    """Collector Class."""

    @staticmethod
    @abstractmethod
    def create_instance(**kwargs: Any) -> 'Collector':
        """Create an instance of the collector."""
        ...

    @abstractmethod
    def collect(self) -> Iterable[TDocument]:
        """
        Collect the documents to index.

        Returns:
            Iterable[TDocument]: The collected documents.
        """
        ...
