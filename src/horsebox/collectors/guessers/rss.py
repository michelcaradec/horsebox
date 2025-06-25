from typing import (
    Any,
    Dict,
    Optional,
    Tuple,
)

from horsebox.collectors import CollectorType


def guess_rss(item: str) -> Optional[Tuple[CollectorType, Dict[str, Any]]]:
    """
    Guess the use of the RSS collector from an item.

    >>> guess_rss('file.txt') is None
    True

    >>> guess_rss('feed.xml')
    (<CollectorType.RSS: 'rss'>, {})

    >>> guess_rss('feed.atom')
    (<CollectorType.RSS: 'rss'>, {})

    >>> guess_rss('https://website.com/feed')
    (<CollectorType.RSS: 'rss'>, {})

    >>> guess_rss('https://website.com/rss')
    (<CollectorType.RSS: 'rss'>, {})

    Args:
        item (str): The item to check.

    Returns:
        Optional[Tuple[CollectorType, Dict[str, Any]]]:
        - The type of the collector.
        - Some extra arguments to use with the collector.
    """
    if (
        item.endswith('.xml')
        or item.endswith('.atom')
        or item.endswith('/feed')
        or item.endswith('/rss')
    ):
        return (CollectorType.RSS, {})

    return None
