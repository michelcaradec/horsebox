from typing import (
    List,
    Optional,
)

import tantivy

from horsebox.cli.config import config
from horsebox.cli.param_parser import build_params_group
from horsebox.indexer.analyzer import (
    FilterType,
    TokenizerType,
    get_analyzer,
)

__analyzer: Optional[tantivy.TextAnalyzer] = None

_STOP_WORDS_EN_COUNT = 174
"""Number of English stop-words - https://snowballstem.org/algorithms/english/stop.txt"""
_STOP_WORDS_FR_COUNT = 144
"""Number of French stop-words - https://snowballstem.org/algorithms/french/stop.txt"""
STOP_WORDS_COUNT = _STOP_WORDS_EN_COUNT + _STOP_WORDS_FR_COUNT
"""Number of stop-words used in top-keywords analyzer."""


def is_stopword(word: str) -> bool:
    """
    Check if a work is a stop-word or not.

    >>> is_stopword('lorem')
    False

    >>> is_stopword('ipsum')
    False

    >>> is_stopword('and')
    True

    >>> is_stopword('is')
    True

    >>> is_stopword('et')
    True

    >>> is_stopword('il')
    True

    Args:
        word (str): The word to check.
    """
    global __analyzer

    if not __analyzer:
        filter_types: List[FilterType] = [
            FilterType.ALPHANUM_ONLY,
            FilterType.REMOVE_LONG,
            FilterType.LOWERCASE,
            FilterType.STOPWORD,
            FilterType.STOPWORD,
        ]
        filter_params = [
            '',
            'length_limit=40',
            '',
            'language=english',
            'language=french',
        ]

        if config.custom_stopwords:
            filter_types.append(FilterType.CUSTOM_STOPWORD)
            filter_params.append(f'stopwords=[{config.custom_stopwords}]')

        __analyzer = get_analyzer(
            TokenizerType.RAW,
            None,
            filter_types,
            build_params_group(filter_params),
        )

    analyzed: List[str] = __analyzer.analyze(word)

    return len(analyzed) == 0  # The list will be empty for a stop-word
