import os
from datetime import datetime
from typing import (
    Any,
    Generator,
    List,
)

from horsebox.collectors.collector_fs.collector import CollectorFS
from horsebox.indexer.factory import prepare_doc
from horsebox.indexer.index import config
from horsebox.model.collector import (
    Collector,
    TDocument,
)
from horsebox.utils.normalize import normalize_string


class CollectorFSByLine(CollectorFS):
    """By Line File System Collector Class."""

    def __init__(  # noqa: D107
        self,
        root_path: List[str],
        pattern: List[str],
    ) -> None:
        super().__init__(
            root_path,
            pattern,
        )

    @staticmethod
    def create_instance(**kwargs: Any) -> Collector:
        """Create an instance of the collector."""
        return CollectorFSByLine(
            kwargs['root_path'],
            kwargs['pattern'],
        )

    def parse(
        self,
        root_path: str,
        file_path: str,
    ) -> Generator[TDocument, Any, None]:
        """
        Parse a file for indexing by its content with line detail.

        Args:
            root_path (str): Base path of the file.
            file_path (str): File to parse.

        Yields:
            Generator[TDocument, Any, None]: The document to index (one document per line).
        """
        stats: os.stat_result = os.stat(file_path)

        filename = file_path[len(root_path) :].strip('/')
        _, ext = os.path.splitext(filename)

        parser_max_line = config.parser_max_line

        with open(
            file_path,
            'r',
            errors='surrogateescape',
        ) as file:
            for pos, line in enumerate(file, start=1):
                if parser_max_line is not None and len(line) > parser_max_line:
                    continue

                line = line.strip()
                if config.string_normalize:
                    line = normalize_string(line)
                if not line:
                    continue

                yield prepare_doc(
                    name=filename,
                    type=ext,
                    content=line,
                    path=f'{file_path}#L{pos}',
                    size=stats.st_size,
                    # Time of most recent content modification expressed in seconds.
                    updated=datetime.fromtimestamp(stats.st_mtime),
                )
