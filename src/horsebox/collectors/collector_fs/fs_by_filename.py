import os
from datetime import datetime
from typing import (
    Any,
    Generator,
    List,
)

from horsebox.collectors.collector_fs.collector import CollectorFS
from horsebox.indexer.factory import prepare_doc
from horsebox.model import TDocument
from horsebox.model.collector import Collector


class CollectorFSByFilename(CollectorFS):
    """By Filename File System Collector Class."""

    def __init__(  # noqa: D107
        self,
        root_path: List[str],
        pattern: List[str],
        **kwargs: Any,
    ) -> None:
        super().__init__(
            root_path,
            pattern,
            **kwargs,
        )

    @staticmethod
    def create_instance(**kwargs: Any) -> Collector:
        """Create an instance of the collector."""
        return CollectorFSByFilename(
            kwargs.pop('root_path'),
            kwargs.pop('pattern'),
            **kwargs,
        )

    def parse(
        self,
        root_path: str,
        file_path: str,
    ) -> Generator[TDocument, Any, None]:
        """
        Parse a file for indexing by its filename.

        Args:
            root_path (str): Base path of the file.
            file_path (str): File to parse.

        Yields:
            Generator[TDocument, Any, None]: The document to index (one document per file).
        """
        stats: os.stat_result = os.stat(file_path)

        filename = file_path[len(root_path) :].strip('/')
        _, ext = os.path.splitext(filename)

        # No difference between the returned document in real-mode or in dry-mode
        yield prepare_doc(
            name=filename,
            type=ext,
            path=file_path,
            size=stats.st_size,
            # Time of most recent content modification expressed in seconds.
            date=datetime.fromtimestamp(stats.st_mtime),
        )
