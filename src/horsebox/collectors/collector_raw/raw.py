from typing import (
    Any,
    Iterable,
    List,
)

import click
import ijson

from horsebox.cli import FILENAME_PREFIX
from horsebox.indexer.factory import prepare_doc
from horsebox.model import TDocument
from horsebox.model.collector import Collector


class CollectorRaw(Collector):
    """
    Raw Collector Class.

    Used to collect ready to index JSON documents.
    """

    root_path: List[str]

    def __init__(  # noqa: D107
        self,
        root_path: List[str],
    ) -> None:
        self.root_path = root_path

    @staticmethod
    def create_instance(**kwargs: Any) -> Collector:
        """Create an instance of the collector."""
        return CollectorRaw(kwargs['root_path'])

    def collect(self) -> Iterable[TDocument]:
        """
        Collect the documents to index.

        Returns:
            Iterable[TDocument]: The collected documents.
        """
        for root_path in self.root_path:
            filename = root_path[1:] if root_path.startswith(FILENAME_PREFIX) else root_path

            with click.open_file(filename, 'r') as file:
                for item in ijson.items(file, 'item'):
                    yield prepare_doc(**item)
