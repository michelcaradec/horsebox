import re
import unicodedata

__RE_HTML_STRIP = re.compile('<[^>]*>')


def normalize_string(
    text: str,
    keep_accents: bool = False,
) -> str:
    """
    Normalize a string.

    - Replacement of accented characters by their non-accented equivalent.
    - Conversion of Unicode escaped characters.

    Args:
        text (str): The string to normalize.
        keep_accents (bool): Whether the accented characters should be preserved or not.

    Returns:
        str: The normalized string.
            Empty string in case of conversion error (silent fail).
    """
    # Normalize the string
    form = 'NFKC' if keep_accents else 'NFKD'
    normalized = ''.join(
        [
            c
            for c in unicodedata.normalize(form, text)
            if not unicodedata.combining(c)
        ]
    )
    # Convert Unicode escapes
    try:
        unescaped = normalized.encode('utf-16', 'surrogatepass').decode('utf-16')
    except Exception:
        return ''

    return unescaped


def strip_html_tags(text: str) -> str:
    """
    Remove the HTML tags from a string.

    >>> strip_html_tags('<p>lorem ipsum</p>')
    'lorem ipsum'

    >>> strip_html_tags('lorem ipsum')
    'lorem ipsum'

    Args:
        text (str): The string to process.

    Returns:
        str: The cleaned string.
    """
    return __RE_HTML_STRIP.sub('', text).strip()


def strip_spaces(text: str) -> str:
    r"""
    Remove the duplicate spaces from a string.

    >>> strip_spaces('')
    ''

    >>> strip_spaces('lorem  ipsum dolor')
    'lorem ipsum dolor'

    >>> strip_spaces('lorem  ipsum\ndolor\tsit')
    'lorem ipsum dolor sit'

    Args:
        text (str): The string to process.

    Returns:
        str: The cleaned string.
    """
    return ' '.join(text.split())
