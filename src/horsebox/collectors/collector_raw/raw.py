import os
from typing import (
    Any,
    Iterable,
    List,
)

import click
import ijson

from horsebox.cli import (
    FILENAME_PREFIX,
    OPTION_COLLECT_AS_JSONL,
)
from horsebox.indexer.factory import prepare_doc
from horsebox.model import TDocument
from horsebox.model.collector import Collector


class CollectorRaw(Collector):
    """
    Raw Collector Class.

    Used to collect ready to index JSON documents.
    """

    root_path: List[str]
    collect_as_jsonl: bool

    def __init__(  # noqa: D107
        self,
        root_path: List[str],
        collect_as_jsonl: bool,
    ) -> None:
        self.root_path = root_path
        self.collect_as_jsonl = collect_as_jsonl

    @staticmethod
    def create_instance(**kwargs: Any) -> Collector:
        """Create an instance of the collector."""
        return CollectorRaw(
            kwargs['root_path'],
            kwargs[OPTION_COLLECT_AS_JSONL],
        )

    def collect(self) -> Iterable[TDocument]:
        """
        Collect the documents to index.

        Returns:
            Iterable[TDocument]: The collected documents.
        """
        for root_path in self.root_path:
            filename = root_path[1:] if root_path.startswith(FILENAME_PREFIX) else root_path

            with click.open_file(filename, 'r') as file:
                if self.__is_jsonl(filename):
                    # See https://pypi.org/project/ijson/#options-1
                    items = ijson.items(file, '', multiple_values=True)
                else:
                    items = ijson.items(file, 'item')

                for item in items:
                    yield prepare_doc(**item)

    def __is_jsonl(
        self,
        filename: str,
    ) -> bool:
        _, fileext = os.path.splitext(filename)
        return self.collect_as_jsonl or fileext in ['.jsonl', '.ndjson']
