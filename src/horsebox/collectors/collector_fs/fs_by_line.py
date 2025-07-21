import os
from datetime import datetime
from typing import (
    Any,
    Generator,
    List,
    Optional,
)

import click

from horsebox.cli.config import config
from horsebox.collectors import FILENAME_PIPE
from horsebox.collectors.collector_fs.collector import CollectorFS
from horsebox.indexer.factory import prepare_doc
from horsebox.model import TDocument
from horsebox.model.collector import Collector
from horsebox.utils.normalize import normalize_string


class CollectorFSByLine(CollectorFS):
    """By Line File System Collector Class."""

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
        return CollectorFSByLine(
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
        Parse a file for indexing by its content with line detail.

        Args:
            root_path (str): Base path of the file.
            file_path (str): File to parse.

        Yields:
            Generator[TDocument, Any, None]: The document to index (one document per line).
        """
        stats: Optional[os.stat_result] = None
        filename: str

        if file_path == FILENAME_PIPE:
            filename = FILENAME_PIPE
        else:
            stats = os.stat(file_path)
            filename = file_path[len(root_path) :].strip('/')

        _, ext = os.path.splitext(filename)

        if self.dry_run:
            yield prepare_doc(
                name=filename,
                type=ext,
                path=file_path,
                size=stats.st_size if stats else None,
                # Time of most recent content modification expressed in seconds.
                date=datetime.fromtimestamp(stats.st_mtime) if stats else None,
            )
            return

        parser_max_line = config.parser_max_line

        with click.open_file(
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
                    path=f'{file_path}#{pos}',
                    size=stats.st_size if stats else None,
                    # Time of most recent content modification expressed in seconds.
                    date=datetime.fromtimestamp(stats.st_mtime) if stats else None,
                )
