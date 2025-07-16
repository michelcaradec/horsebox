from enum import Enum


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
    """
    Tokenize the text by using a regex pattern to split.
    
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
