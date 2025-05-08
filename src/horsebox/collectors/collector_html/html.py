import urllib.request
from typing import (
    Any,
    Iterable,
    List,
)

from bs4 import BeautifulSoup

from horsebox.cli import FILENAME_PREFIX
from horsebox.indexer.factory import prepare_doc
from horsebox.indexer.schema import SCHEMA_FIELD_CONTENT
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
    ) -> None:
        self.pages = pages

    @staticmethod
    def create_instance(**kwargs: Any) -> Collector:
        """Create an instance of the collector."""
        return CollectorHtml(kwargs['root_path'])

    def collect(self) -> Iterable[TDocument]:
        """
        Collect the data to index.

        Returns:
            Iterable[TDocument]: The collected documents.
        """
        for page in self.pages:
            if page.startswith(FILENAME_PREFIX):
                with open(page[1:], 'r') as file:
                    content = file.read()
            else:
                with ipv6_disabled():
                    with urllib.request.urlopen(page) as response:
                        content = response.read()

            soup = BeautifulSoup(content, 'html.parser')

            name = (
                title[0].get_text()
                if (soup.html and (title := soup.html.find_all('title', limit=1)) and len(title))
                else None
            )

            yield prepare_doc(
                **{
                    'name': name,
                    'path': page,
                    SCHEMA_FIELD_CONTENT: soup.get_text(),
                }
            )
