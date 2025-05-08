import json
import os
import shutil
from datetime import datetime
from typing import (
    Any,
    Dict,
    Optional,
)

import tantivy

from horsebox.cli.render import render_error

__METADATA_FILENAME = 'meta.json'
__METADATA_TIMESTAMP = 'timestamp'


def __read_metadata(index: str) -> Dict[str, Any]:
    if not tantivy.Index.exists(index):
        render_error(f'No index was found at {index}', exit=True)

    with open(os.path.join(index, __METADATA_FILENAME), 'r') as file:
        meta = json.load(file)

    return meta


def __write_metadata(
    index: str,
    metadata: Dict[str, Any],
) -> None:
    if not tantivy.Index.exists(index):
        render_error(f'No index was found at {index}', exit=True)

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
