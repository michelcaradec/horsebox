from typing import (
    Any,
    Dict,
    Optional,
    Tuple,
)

from horsebox.collectors import CollectorType


def guess_html(item: str) -> Optional[Tuple[CollectorType, Dict[str, Any]]]:
    """
    Guess the use of the HTML collector from an item.

    >>> guess_html('file.txt') is None
    True

    >>> guess_html('file.html')
    (<CollectorType.HTML: 'html'>, {})

    Args:
        item (str): The item to check.

    Returns:
        Optional[Tuple[CollectorType, Dict[str, Any]]]:
        - The type of the collector.
        - Some extra arguments to use with the collector.
    """
    if item.endswith('.html'):
        return (CollectorType.HTML, {})

    return None
