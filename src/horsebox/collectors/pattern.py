import os
from typing import (
    List,
    Set,
    Tuple,
)

from horsebox.cli import PATTERN_ANY


def explode_pattern(
    source: List[str],
    pattern: List[str],
) -> Tuple[List[str], List[str]]:
    """
    Convert locations and containers description to canonical ones.

    >>> explode_pattern([], [])
    ([], [])

    >>> explode_pattern(['*.txt'], ['*'])
    (['.'], ['*.txt'])

    >>> explode_pattern(['this/folder'], ['*'])
    (['this/folder'], ['*'])

    >>> explode_pattern(['this/folder'], ['*.txt'])
    (['this/folder'], ['*.txt'])

    >>> explode_pattern(['this/folder/*.txt'], ['*'])
    (['this/folder/'], ['*.txt'])

    >>> explode_pattern(['this/folder/*.txt'], ['*.pdf'])
    (['this/folder/'], ['*.pdf', '*.txt'])

    >>> explode_pattern(['this/folder*/*.txt'], ['*.pdf'])
    (['this/'], ['*.pdf', 'folder*/*.txt'])

    >>> explode_pattern(['this/folder*/file.txt'], ['*'])
    (['this/'], ['folder*/file.txt'])

    Args:
        source (List[str]): Locations from which to start indexing.
        pattern (List[str]): The containers to index.

    Returns:
        Tuple[List[str], List[str]]: The canonicalized (locations, containers).
    """
    source2: List[str] = []
    pattern2: Set[str] = set(pattern)

    for s in source:
        if PATTERN_ANY in s:
            # Only the magic '*' is supported
            magic_pos = s.find(PATTERN_ANY)
            if sep_last_pos := s.rfind(os.sep, None, magic_pos) + 1:
                root_path = s[:sep_last_pos]
                p = s[sep_last_pos:]
            else:
                root_path = '.'
                p = s

            source2.append(root_path)
            pattern2.add(p)
        else:
            source2.append(s)

    if len(pattern2) > 1:
        # The joker pattern is not required if there are more specific patterns
        pattern2.discard(PATTERN_ANY)

    # HACK Return a sorted list of patterns to allow repeatable tests
    return (source2, sorted(pattern2))
