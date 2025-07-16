import json
from typing import (
    Any,
    Dict,
    List,
    Optional,
)

import click
import tantivy

from horsebox.cli.param_parser import (
    parse_params,
    parse_params_group,
)
from horsebox.cli.render import render_error
from horsebox.indexer.analyzer import (
    CustomAnalyzerDef,
    FilterType,
    TokenizerType,
)
from horsebox.indexer.analyzer.custom_analyzer_def import CustomAnalyzerArgs
from horsebox.utils.strings import ellipsize


def get_custom_analyzer_def(
    tokenizer_type: TokenizerType,
    tokenizer_params: Optional[str],
    filter_types: List[FilterType],
    filter_params: Optional[str],
) -> CustomAnalyzerDef:
    """
    Get a custom analyzer definition form raw parameters.

    Args:
        tokenizer_type (TokenizerType): The tokenizer to use.
        tokenizer_params (Optional[str]): The parameters of the tokenizer.
        filter_types (List[FilterType]): The filters to use.
        filter_params (Optional[str]): The parameters of the filters.
    """
    filters: List[Dict[FilterType, CustomAnalyzerArgs]] = []

    filter_params_group = parse_params_group(filter_params, len(filter_types))
    for filter_type, filter_params in zip(filter_types, filter_params_group):
        filters.append({FilterType(filter_type): parse_params(filter_params)})

    return CustomAnalyzerDef(
        tokenizer={
            tokenizer_type: parse_params(
                tokenizer_params,
                is_raw=tokenizer_type in [TokenizerType.REGEX],
            ),
        },
        filters=filters,
    )


def load_custom_analyzer_def(filename: str) -> CustomAnalyzerDef:
    """
    Load the definition of a custom analyzer from a file.

    Args:
        filename (str): The name of the file.
    """
    content: Dict[str, Any]

    try:
        with click.open_file(filename, 'r') as file:
            content = json.load(file)
    except json.decoder.JSONDecodeError as e:
        render_error(f'Invalid custom analyzer JSON file: {filename} - {e}')

    try:
        return CustomAnalyzerDef(**content)
    except Exception as e:
        dump = json.dumps(content)
        render_error(f'Error while parsing custom analyzer definition: {filename} - {e} - {ellipsize(dump, 50)}')
        raise


def get_analyzer(custom_analyzer: CustomAnalyzerDef) -> tantivy.TextAnalyzer:
    """
    Create a text analyzer.

    Attention! The configuration `HB_CUSTOM_STOPWORDS` is ignored.

    Args:
        custom_analyzer (CustomAnalyzer): The custom analyzer definition to use.
    """
    tokenizer_type, tokenizer_params = next(iter(custom_analyzer.tokenizer.items()))
    tokenizer_factory = getattr(tantivy.Tokenizer, tokenizer_type.value)
    t_tokenizer: tantivy.Tokenizer = tokenizer_factory(**tokenizer_params)

    builder = tantivy.TextAnalyzerBuilder(t_tokenizer)

    for filter in custom_analyzer.filters:
        filter_type, filter_param = next(iter(filter.items()))

        filter_factory = getattr(tantivy.Filter, filter_type.value)
        t_filter: tantivy.Filter = filter_factory(**filter_param)
        builder = builder.filter(t_filter)

    return builder.build()
