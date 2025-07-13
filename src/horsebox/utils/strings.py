from typing import List


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
