from typing import List

from horsebox.cli import ELLIPSIS


def split_with_escaped(
    text: str,
    sep: str,
) -> List[str]:
    """
    Return a list of the substrings in a string, with support of an escaped separator.

    An escaped separator is enclosed in curly brackets (e.g. {,} for an escaped comma).

    >>> split_with_escaped('', ',')
    ['']

    >>> split_with_escaped('lorem', ',')
    ['lorem']

    >>> split_with_escaped('lorem,ipsum', ',')
    ['lorem', 'ipsum']

    >>> split_with_escaped('lorem,ipsum{,}dolor', ',')
    ['lorem', 'ipsum,dolor']

    >>> split_with_escaped('{,}lorem,ipsum{,}', ',')
    [',lorem', 'ipsum,']

    >>> split_with_escaped('{,}{,},', ',')
    [',,', '']

    Args:
        text (str): the string to split.
        sep (str): The separator used to split the string.
    """
    pivot_chr = chr(26)  # SUB
    escaped = text.replace('{' + sep + '}', pivot_chr)
    return [
        # Rebuild the part with the original (non-escaped) separator
        part.replace(pivot_chr, sep)
        for part
        # Split the escaped string according to the (non-escaped) separators
        in escaped.split(sep)
    ]


def ellipsize(
    text: str,
    size: int,
) -> str:
    """
    Get the content of a string, limited to a maximum size.

    >>> ellipsize('', 0)
    ''

    >>> ellipsize('lorem', 3)
    '...'

    >>> ellipsize('lorem', 5)
    'lorem'

    >>> ellipsize('lorem', 10)
    'lorem'

    >>> ellipsize('lorem ipsum', 10)
    'lorem i...'

    Args:
        text (str): The text to get the content from.
        size (int): The maximum size to return.
    """
    return text if len(text) <= max(size, len(ELLIPSIS)) else text[: size - len(ELLIPSIS)] + ELLIPSIS
