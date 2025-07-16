from dataclasses import dataclass
from typing import (
    Any,
    Dict,
    List,
)

from horsebox.cli.render import render_error

from .filter_type import FilterType
from .tokenizer_type import TokenizerType

CustomAnalyzerArgs = Dict[str, Any]


@dataclass
class CustomAnalyzerDef:
    """Definition of a custom analyzer."""

    tokenizer: Dict[TokenizerType, CustomAnalyzerArgs]
    filters: List[Dict[FilterType, CustomAnalyzerArgs]]

    def __post_init__(self) -> None:  # noqa: D105
        if not isinstance(self.tokenizer, dict):
            render_error(f'Incorrect tokenizer: {self.tokenizer}')
        if len(self.tokenizer) != 1:
            render_error(f'Only one tokenizer is allowed: {",".join(list(self.tokenizer.keys()))}')

        # Convert enumerations serialized as a string back to the enumeration type
        tokenizer_type, tokenizer_params = self.tokenizer.popitem()
        self.tokenizer[TokenizerType(tokenizer_type)] = tokenizer_params

        filters: List[Dict[FilterType, CustomAnalyzerArgs]] = []
        for filter in self.filters:
            filter_type, filter_params = filter.popitem()
            filters.append({FilterType(filter_type): filter_params})
        self.filters = filters
