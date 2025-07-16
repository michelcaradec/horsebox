from enum import Enum


class FilterType(str, Enum):
    """
    Types of Filters.

    See https://docs.rs/tantivy/latest/tantivy/tokenizer/trait.TokenFilter.html.
    """

    ALPHANUM_ONLY = 'alphanum_only'
    """Removes all tokens that contain non ascii alphanumeric characters."""
    ASCII_FOLD = 'ascii_fold'
    """
    Converts alphabetic, numeric, and symbolic Unicode characters which are not in the first 127 ASCII characters
    into their ASCII equivalents, if one exists.
    """
    LOWERCASE = 'lowercase'
    """Lowercase terms."""
    REMOVE_LONG = 'remove_long'
    """
    Removes tokens that are longer than a given number of bytes.

    Args:
        length_limit (int)
    """
    STEMMER = 'stemmer'
    """
    Stemmer token filter.

    Tokens are expected to be lowercased beforehand.

    Args:
        language (str)
    """
    STOPWORD = 'stopword'
    """
    Removes stop words for a given language.

    Args:
        language (str)
    """
    CUSTOM_STOPWORD = 'custom_stopword'
    """
    Removes stop words from a given a list.

    Args:
        stopwords (List[str])
    """
    SPLIT_COMPOUND = 'split_compound'
    """
    Splits compound words into their parts based on a given dictionary.

    Args:
        constituent_words: (List[str])
    """
