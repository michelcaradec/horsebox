from typing import (
    Any,
    Dict,
    Optional,
    Tuple,
)

from horsebox.cli import OPTION_COLLECT_AS_JSONL
from horsebox.collectors import CollectorType


def guess_raw(item: str) -> Optional[Tuple[CollectorType, Dict[str, Any]]]:
    """
    Guess the use of the RAW collector from an item.

    >>> guess_raw('raw.txt') is None
    True

    >>> guess_raw('raw.json')
    (<CollectorType.RAW: 'raw'>, {})

    >>> guess_raw('raw.jsonl')
    (<CollectorType.RAW: 'raw'>, {'collect_as_jsonl': True})

    Args:
        item (str): The item to check.

    Returns:
        Optional[Tuple[CollectorType, Dict[str, Any]]]:
        - The type of the collector.
        - Some extra arguments to use with the collector.
    """
    if item.endswith('.json'):
        return (CollectorType.RAW, {})
    elif item.endswith('.jsonl'):
        return (CollectorType.RAW, {OPTION_COLLECT_AS_JSONL: True})

    return None
