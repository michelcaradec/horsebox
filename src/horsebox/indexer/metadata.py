import json
import os
import shutil
from dataclasses import asdict
from datetime import datetime
from typing import (
    Any,
    Dict,
    Optional,
)

import tantivy

from horsebox import __version__
from horsebox.cli.render import render_error
from horsebox.indexer.build_args import IndexBuildArgs

__METADATA_FILENAME = 'meta.json'
__METADATA_TIMESTAMP = 'timestamp'
__METADATA_BUILD_ARGS = 'build_args'
__METADATA_VERSION = 'version'


def __read_metadata(index: str) -> Dict[str, Any]:
    if not tantivy.Index.exists(index):
        render_error(f'No index was found at {index}')

    with open(os.path.join(index, __METADATA_FILENAME), 'r') as file:
        meta: Dict[str, Any] = json.load(file)

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

    metadata[__METADATA_VERSION] = __version__

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


def get_build_args(index: str) -> Optional[IndexBuildArgs]:
    """
    Get the build arguments of an index.

    Args:
        index (str): The path of the index.
    """
    meta = __read_metadata(index)
    if build_args := meta.get(__METADATA_BUILD_ARGS):
        return IndexBuildArgs(**build_args)

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
