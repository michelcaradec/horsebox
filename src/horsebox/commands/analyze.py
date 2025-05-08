from typing import (
    List,
    Optional,
    cast,
)

from horsebox.cli import FILENAME_PREFIX
from horsebox.cli.render import (
    Format,
    render,
)
from horsebox.indexer.analyzer import (
    FilterType,
    TokenizerType,
    get_analyzer,
)


def analyze(
    text: str,
    tokenizer_type: TokenizerType,
    tokenizer_params: Optional[str],
    filter_types: List[FilterType],
    filter_params: Optional[str],
    format: Format,
) -> None:
    """
    Analyze a text.

    Args:
        text (str): The text to analyze.
        tokenizer_type (TokenizerType): The tokenizer to use.
        tokenizer_params (Optional[str]): The parameters of the tokenizer.
        filter_types (List[FilterType]): The filters to use.
        filter_params (Optional[str]): The parameters of the filters.
        format (Format): The rendering format to use.
    """
    analyzer = get_analyzer(
        tokenizer_type,
        tokenizer_params,
        filter_types,
        filter_params,
    )

    if text.startswith(FILENAME_PREFIX):
        with open(text[1:], 'r') as file:
            text = file.read()

    analyzed: List[str] = analyzer.analyze(cast(str, text))

    output = {'analyzed': analyzed}

    render(output, format)
