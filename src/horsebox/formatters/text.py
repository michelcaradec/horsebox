from datetime import datetime
from typing import (
    Any,
    Dict,
    Generator,
    List,
    Optional,
    cast,
)

import tantivy

from horsebox.formatters import DATE_FORMAT
from horsebox.model import TOutput

__SNIPPET_BEGIN = '<b>'
__SNIPPET_END = '</b>'

__COLOR_GREEN = '\033[92m'
__COLOR_RESET = '\033[0m'
__BOLD = '\033[1m'

__INDENT = '  '
__LINE_BREAK = '* * * * *'
LINE_BREAK = {}
"""Line break item."""


def format_txt(output: TOutput) -> Generator[str, Any, None]:
    """
    Text formatter.

    Args:
        output (TOutput): The content to format.

    Yields:
        Generator[str, Any, None]: The formatted content.
    """
    for item in output if isinstance(output, List) else [output]:
        if item == LINE_BREAK:
            yield __LINE_BREAK
            continue

        for field, value in item.items():
            if value is None:
                value = ''
            elif isinstance(value, Dict):
                # Dictionary
                yield f'{field.capitalize()}:'
                for sub_item in format_txt(value):
                    yield f'{__INDENT}{sub_item}'
            elif isinstance(value, List) and len(value) and isinstance(value[0], Dict):
                # List of dictionaries
                for sub_item in format_txt(value):
                    yield sub_item
            else:
                if isinstance(value, float):
                    value = round(value, 3)
                elif isinstance(value, datetime):
                    value = cast(datetime, value).strftime(DATE_FORMAT)
                elif isinstance(value, List):
                    value = ','.join(value)

                yield f'{field.capitalize()}: {value}'


def snippet_add_style(snippet: tantivy.Snippet) -> Optional[str]:
    """
    Add style decorators to a search result snippet.

    Args:
        snippet (tantivy.Snippet): The snippet.

    Returns:
        Optional[str]: The decorated snippet.
    """
    content = snippet.to_html().replace(__SNIPPET_BEGIN, __BOLD + __COLOR_GREEN).replace(__SNIPPET_END, __COLOR_RESET)

    # NOTE The code below has been disabled as the ranges may not be accurate with Unicode (emojis) characters
    """
    highlighted = snippet.highlighted()
    if not highlighted:
        return None

    content = snippet.fragment()
    # Process ranges in reverse order to preserve position information accuracy
    for highlighted in snippet.highlighted()[::-1]:
        content = (
            content[: highlighted.start]
            + __BOLD
            + __COLOR_GREEN
            + content[highlighted.start : highlighted.end]
            + __COLOR_RESET
            + content[highlighted.end :]
        )
    """

    return content
