import os
import urllib.request
from typing import (
    Any,
    Generator,
    Iterable,
    List,
)

from trafilatura import extract

from horsebox.cli import FILENAME_PREFIX
from horsebox.indexer.factory import prepare_doc
from horsebox.model import TDocument
from horsebox.model.collector import Collector
from horsebox.utils.ipv6 import ipv6_disabled


class CollectorHtml(Collector):
    """
    HTML Collector Class.

    Used to collect the content of an HTML page.
    """

    pages: List[str]

    def __init__(  # noqa: D107
        self,
        pages: List[str],
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)

        self.pages = pages

    @staticmethod
    def create_instance(**kwargs: Any) -> Collector:
        """Create an instance of the collector."""
        return CollectorHtml(
            kwargs.pop('root_path'),
            **kwargs,
        )

    def collect(self) -> Iterable[TDocument]:
        """
        Collect the data to index.

        Returns:
            Iterable[TDocument]: The collected documents.
        """
        for page in self.pages:
            yield from self.parse('', page)

    def parse(
        self,
        root_path: str,
        file_path: str,
    ) -> Generator[TDocument, Any, None]:
        """
        Parse a file for indexing by its content.

        Args:
            root_path (str): Base path of the file.
            file_path (str): File to parse.

        Yields:
            Generator[TDocument, Any, None]: The document to index (one document per file).
        """
        if self.dry_run:
            yield prepare_doc(
                path=file_path[1:] if file_path.startswith(FILENAME_PREFIX) else file_path,
            )
            return

        if file_path.startswith(FILENAME_PREFIX):
            with open(file_path[1:], 'r') as file:
                content = file.read()
        else:
            with ipv6_disabled():
                with urllib.request.urlopen(file_path) as response:
                    content = response.read()

        if extracted := extract(
            content,
            include_tables=False,
            include_comments=False,
        ):
            yield prepare_doc(
                **{
                    'name': os.path.basename(file_path),
                    'path': file_path,
                    'content': extracted,
                }
            )
