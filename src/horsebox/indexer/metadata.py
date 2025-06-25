import json
import os
import shutil
from dataclasses import (
    asdict,
    dataclass,
)
from datetime import datetime
from typing import (
    Any,
    Dict,
    List,
    Optional,
)

import tantivy

from horsebox.cli.render import render_error
from horsebox.collectors import CollectorType

__METADATA_FILENAME = 'meta.json'
__METADATA_TIMESTAMP = 'timestamp'
__METADATA_BUILD_ARGS = 'build_args'


def __read_metadata(index: str) -> Dict[str, Any]:
    if not tantivy.Index.exists(index):
        render_error(f'No index was found at {index}')

    with open(os.path.join(index, __METADATA_FILENAME), 'r') as file:
        meta = json.load(file)

    return meta


def __write_metadata(
    index: str,
    metadata: Dict[str, Any],
) -> None:
    if not tantivy.Index.exists(index):
        render_error(f'No index was found at {index}')

    filename = os.path.join(index, __METADATA_FILENAME)
    # Make a backup copy of the file `meta.json` to recover from potential corruption
    shutil.copyfile(filename, filename + '.bak')

    with open(filename, 'w') as file:
        json.dump(metadata, file)


def get_timestamp(index: str) -> Optional[datetime]:
    """
    Get the date of creation of an index.

    Args:
        index (str): The path of the index.
    """
    meta = __read_metadata(index)
    if timestamp := meta.get(__METADATA_TIMESTAMP):
        return datetime.fromtimestamp(timestamp)

    return None


def set_timestamp(
    index: str,
    timestamp: datetime,
) -> None:
    """
    Set the date of creation of an index.

    Args:
        index (str): The path of the index.
        timestamp (datetime): The date of creation of the index.
    """
    meta = __read_metadata(index)
    meta[__METADATA_TIMESTAMP] = timestamp.timestamp()
    __write_metadata(index, meta)


@dataclass
class IndexBuildArgs:
    """Arguments used to build an index."""

    source: List[str]
    """Locations from which to start indexing."""
    pattern: List[str]
    """The containers to index."""
    collector_type: CollectorType
    """The collector to use."""
    collect_as_jsonl: bool
    """Whether the JSON documents should be collected as JSON Lines or not."""


def get_build_args(index: str) -> Optional[IndexBuildArgs]:
    """
    Get the build arguments of an index.

    Args:
        index (str): The path of the index.
    """
    meta = __read_metadata(index)
    if build_args := meta.get(__METADATA_BUILD_ARGS):
        build_args = IndexBuildArgs(**build_args)

        # Set the collector type as enumeration as it was serialized as a string
        build_args.collector_type = CollectorType(build_args.collector_type)

        return build_args

    return None


def set_build_args(
    index: str,
    build_args: IndexBuildArgs,
) -> None:
    """
    Set the build arguments of an index.

    Args:
        index (str): The path of the index.
        build_args (IndexBuildArgs): The arguments used to build the index.
    """
    meta = __read_metadata(index)
    meta[__METADATA_BUILD_ARGS] = asdict(build_args)
    __write_metadata(index, meta)


def set_metadata(
    index: str,
    timestamp: datetime,
    build_args: Optional[IndexBuildArgs],
) -> None:
    """
    Set (atomically) the metadata of an index.

    Args:
        index (str): The path of the index.
        timestamp (datetime): The date of creation of the index.
        build_args (Optional[IndexBuildArgs]): The arguments used to build the index.
    """
    meta = __read_metadata(index)
    meta[__METADATA_TIMESTAMP] = timestamp.timestamp()
    if build_args:
        meta[__METADATA_BUILD_ARGS] = asdict(build_args)
    __write_metadata(index, meta)
