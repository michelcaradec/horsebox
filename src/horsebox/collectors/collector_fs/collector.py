import itertools
import os
from glob import iglob
from typing import (
    Any,
    Iterable,
    List,
)

from horsebox.cli import OPTION_DRY_RUN
from horsebox.collectors import FILENAME_PIPE
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
        **kwargs: Any,
    ) -> None:
        self.root_path = root_path
        self.pattern = pattern
        self.dry_run = kwargs.get(OPTION_DRY_RUN, False)

    def collect(self) -> Iterable[TDocument]:
        """
        Collect the data to index.

        Returns:
            Iterable[TDocument]: The collected documents.
        """
        # For each file/folder
        for root_path in self.root_path:
            if root_path == FILENAME_PIPE:
                # Collect from piped content
                yield from self.parse(
                    FILENAME_PIPE,
                    FILENAME_PIPE,
                )
            elif os.path.isfile(root_path):
                # Collect this file
                yield from self.parse(
                    os.path.dirname(root_path),
                    root_path,
                )
            else:
                # For each file in the folder
                for filename in itertools.chain.from_iterable(
                    iglob(
                        os.path.join(os.path.expanduser(root_path), f'**/{p}'),
                        recursive=True,
                    )
                    for p in self.pattern
                ):
                    if not os.path.isfile(filename):
                        continue

                    yield from self.parse(root_path, filename)
