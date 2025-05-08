from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    List,
    Union,
)

TDocument = Dict[str, Any]
"""Document to index."""

TOutput = Union[List[Dict[str, Any]], Dict[str, Any]]
"""Output to render."""
TFormatter = Callable[[TOutput], Generator[str, Any, None]]
"""Formatter user to render an output."""
