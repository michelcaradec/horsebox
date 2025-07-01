from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Any,
    Generator,
    Iterable,
)

from horsebox.cli import OPTION_DRY_RUN
from horsebox.model import TDocument


class Collector(ABC):
    """Collector Class."""

    dry_run: bool = False

    def __init__(  # noqa: D107
        self,
        **kwargs: Any,
    ) -> None:
        self.dry_run = kwargs.get(OPTION_DRY_RUN, False)

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

    @abstractmethod
    def parse(
        self,
        root_path: str,
        file_path: str,
    ) -> Generator[TDocument, Any, None]:
        """
        Parse a container for indexing.

        Args:
            root_path (str): Base path of the file.
            file_path (str): File to parse.

        Yields:
            Generator[TDocument, Any, None]: The document to index.
        """
        ...
