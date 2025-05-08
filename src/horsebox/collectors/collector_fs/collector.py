import itertools
import os
from abc import abstractmethod
from glob import iglob
from typing import (
    Any,
    Generator,
    Iterable,
    List,
)

from horsebox.model import TDocument
from horsebox.model.collector import Collector


class CollectorFS(Collector):
    """File System Collector Class."""

    root_path: List[str]
    pattern: List[str]

    def __init__(  # noqa: D107
        self,
        root_path: List[str],
        pattern: List[str],
    ) -> None:
        self.root_path = root_path
        self.pattern = pattern

    def collect(self) -> Iterable[TDocument]:
        """
        Collect the data to index.

        Returns:
            Iterable[TDocument]: The collected documents.
        """
        return itertools.chain.from_iterable(
            # Parse the file...
            self.parse(root_path, filename)
            # ...for each folder...
            for root_path in self.root_path
            # ...for each file in the folder.
            for filename in itertools.chain.from_iterable(
                iglob(os.path.join(os.path.expanduser(root_path), f'**/{p}'), recursive=True) for p in self.pattern
            )
            if os.path.isfile(filename)
        )

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
