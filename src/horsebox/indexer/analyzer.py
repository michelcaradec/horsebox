from enum import Enum
from typing import (
    List,
    Optional,
)

import tantivy

from horsebox.cli.param_parser import (
    parse_params,
    parse_params_group,
)


class TokenizerType(str, Enum):
    """
    Types of Tokenizers.

    See https://docs.rs/tantivy/latest/tantivy/tokenizer/trait.Tokenizer.html.
    """

    RAW = 'raw'
    """For each value of the field, emit a single unprocessed token."""
    SIMPLE = 'simple'
    """Tokenize the text by splitting on whitespaces and punctuation."""
    WHITESPACE = 'whitespace'
    """Tokenize the text by splitting on whitespaces."""
    FACET = 'facet'
    """Process a Facet binary representation and emits a token for all of its parent."""
    REGEX = 'regex'
    """Tokenize the text by using a regex pattern to split.
    
    Args:
        pattern (str)
    """
    NGRAM = 'ngram'
    """
    Tokenize the text by splitting words into n-grams of the given size(s).

    Args:
        min_gram (int) = 2
        max_gram (int) = 3
        prefix_only (bool) = False
    """


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


def get_analyzer(
    tokenizer_type: TokenizerType,
    tokenizer_params: Optional[str],
    filter_types: List[FilterType],
    filter_params: Optional[str],
) -> tantivy.TextAnalyzer:
    """
    Create an analyzer.

    Args:
        tokenizer_type (TokenizerType): The type of tokenizer to use.
        tokenizer_params (Optional[str]): The parameters of the tokenizer.
        filter_types (List[FilterType]): The list of filters to apply.
        filter_params (Optional[str]): The parameters of the filters.
    """
    params = parse_params(tokenizer_params, is_raw=tokenizer_type in [TokenizerType.REGEX])

    tokenizer_factory = getattr(tantivy.Tokenizer, tokenizer_type.value)
    t_tokenizer: tantivy.Tokenizer = tokenizer_factory(**params)

    builder = tantivy.TextAnalyzerBuilder(t_tokenizer)

    filter_params_group = parse_params_group(filter_params, len(filter_types))

    for filter_type, filter_param in zip(filter_types, filter_params_group):
        params = parse_params(filter_param)

        filter_factory = getattr(tantivy.Filter, filter_type.value)
        t_filter: tantivy.Filter = filter_factory(**params)
        builder = builder.filter(t_filter)

    return builder.build()
