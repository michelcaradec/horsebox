from typing import (
    Any,
    Dict,
    List,
    Tuple,
)
from urllib.parse import urlparse

from horsebox.cli import PATTERN_ANY
from horsebox.cli.render import render_error
from horsebox.collectors import CollectorType
from horsebox.collectors.guessers import (
    guess_html,
    guess_raw,
    guess_rss,
)


def guess_collector(
    collector_type: CollectorType,
    source: List[str],
    pattern: List[str],
) -> Tuple[CollectorType, Dict[str, Any]]:
    """
    Guess the collector to use.

    >>> guess_collector(CollectorType.FILECONTENT, [], [])
    (<CollectorType.FILECONTENT: 'filecontent'>, {})

    >>> guess_collector(CollectorType.FILECONTENT, [], ['*'])
    (<CollectorType.FILECONTENT: 'filecontent'>, {})

    >>> guess_collector(CollectorType.FILECONTENT, [], ['*.md'])
    (<CollectorType.FILECONTENT: 'filecontent'>, {})

    >>> guess_collector(CollectorType.GUESS, [], [])
    (<CollectorType.GUESS: 'guess'>, {})

    >>> guess_collector(CollectorType.GUESS, ['raw.json'], [])
    (<CollectorType.RAW: 'raw'>, {})

    >>> guess_collector(CollectorType.GUESS, ['raw.jsonl'], [])
    (<CollectorType.RAW: 'raw'>, {'collect_as_jsonl': True})

    >>> guess_collector(CollectorType.GUESS, [], ['*.txt'])
    (<CollectorType.FILECONTENT: 'filecontent'>, {})

    >>> guess_collector(CollectorType.GUESS, ['https://planetpython.org/rss20.xml'], [])
    (<CollectorType.RSS: 'rss'>, {})

    >>> guess_collector(CollectorType.GUESS, ['@planetpython.xml'], [])
    (<CollectorType.RSS: 'rss'>, {})

    >>> guess_collector(CollectorType.GUESS, ['@planetpython.atom'], [])
    (<CollectorType.RSS: 'rss'>, {})

    >>> guess_collector(CollectorType.GUESS, ['https://en.wikipedia.org/wiki/Python_(programming_language)'], [])
    (<CollectorType.HTML: 'html'>, {})

    >>> guess_collector(CollectorType.GUESS, ['@Python_(programming_language).html'], [])
    (<CollectorType.HTML: 'html'>, {})

    Args:
        collector_type (CollectorType): The provided type of the collector.
        source (List[str]): The provided locations from which to start indexing.
        pattern (List[str]): The provided containers to index.

    Returns:
        Tuple[CollectorType, Dict[str, Any]]:
        - The type of the collector.
        - Some extra arguments to use with the collector.
    """
    if collector_type != CollectorType.GUESS:
        return (collector_type, {})

    if pattern := [p for p in pattern if p != PATTERN_ANY]:
        # Patterns are only supported by File System Collectors.
        # Use the File System Collector by default.
        return (CollectorType.FILECONTENT, {})

    for s in source:
        parsed = urlparse(s)
        if parsed.scheme in ['http', 'https']:
            # Online source
            if guess := guess_rss(parsed.path):
                return guess
            else:
                # If it's not an RSS feed, then it has to be an HTML page
                return (CollectorType.HTML, {})
        elif parsed.scheme:
            render_error(f'Unsupported scheme {parsed.scheme}')
        elif (
            (guess := guess_html(parsed.path)) or (guess := guess_rss(parsed.path)) or (guess := guess_raw(parsed.path))
        ):
            # Offline source
            return guess

    return (collector_type, {})
