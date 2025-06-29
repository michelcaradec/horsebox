import logging
import os
from datetime import datetime
from typing import (
    Any,
    Generator,
    List,
)

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer

from horsebox.cli.config import config
from horsebox.collectors.collector_fs.collector import CollectorFS
from horsebox.indexer.factory import prepare_doc
from horsebox.indexer.schema import SCHEMA_FIELD_CONTENT
from horsebox.model import TDocument
from horsebox.model.collector import Collector
from horsebox.utils.normalize import normalize_string

# Disable logging messages of PDFMiner
logging.getLogger('pdfminer').setLevel(logging.ERROR)


class CollectorPdf(CollectorFS):
    """
    PDF Collector Class.

    Used to collect the content of a PDF document.
    """

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
        return CollectorPdf(
            kwargs['root_path'],
            kwargs['pattern'],
        )

    def parse(
        self,
        root_path: str,
        file_path: str,
    ) -> Generator[TDocument, Any, None]:
        """
        Parse a PDF document for indexing by its content.

        Args:
            root_path (str): Base path of the file.
            file_path (str): File to parse.

        Yields:
            Generator[TDocument, Any, None]: The document to index (one document per file).
        """
        stats: os.stat_result = os.stat(file_path)
        if config.parser_max_content is not None and stats.st_size > config.parser_max_content:
            return

        filename = os.path.basename(file_path)
        _, ext = os.path.splitext(filename)
        # Time of most recent content modification expressed in seconds.
        file_date = datetime.fromtimestamp(stats.st_mtime)

        for pos, page in enumerate(extract_pages(file_path), start=1):
            content: List[str] = []
            # Process file block-by-block to limit memory allocation during string normalization
            for element in page:
                if isinstance(element, LTTextContainer):
                    text = element.get_text().strip()

                    if config.string_normalize:
                        text = normalize_string(text)
                    if text:
                        content.append(text)

            if not content:
                continue

            yield prepare_doc(
                **{
                    'name': filename,
                    'type': ext,
                    'path': f'{file_path}#L{pos}',
                    SCHEMA_FIELD_CONTENT: content,
                    'size': stats.st_size,
                    'date': file_date,
                }
            )
