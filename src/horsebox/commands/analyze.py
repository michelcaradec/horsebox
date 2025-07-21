from typing import (
    List,
    Optional,
)

import tantivy

from horsebox.cli import FILENAME_PREFIX
from horsebox.cli.render import (
    Format,
    render,
)
from horsebox.indexer.analyzer import (
    FilterType,
    TokenizerType,
)
from horsebox.indexer.analyzer.factory import (
    get_analyzer,
    get_custom_analyzer_def,
    load_custom_analyzer_def,
)


def analyze(
    text: str,
    tokenizer_type: TokenizerType,
    tokenizer_params: Optional[str],
    filter_types: List[FilterType],
    filter_params: Optional[str],
    analyzer: Optional[str],
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
        analyzer (Optional[str]): The file containing the definition of the custom analyzer.
        format (Format): The rendering format to use.
    """
    _analyzer: tantivy.TextAnalyzer = (
        get_analyzer(load_custom_analyzer_def(analyzer))
        if analyzer
        else get_analyzer(
            get_custom_analyzer_def(
                tokenizer_type,
                tokenizer_params,
                filter_types,
                filter_params,
            ),
        )
    )

    if text.startswith(FILENAME_PREFIX):
        with open(text[1:], 'r') as file:
            text = file.read()

    analyzed: List[str] = _analyzer.analyze(text)

    output = {'analyzed': analyzed}

    render(output, format)
