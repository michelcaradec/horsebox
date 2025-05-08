import json
from datetime import datetime
from typing import (
    Any,
    Generator,
    List,
    cast,
)

from horsebox.formatters import DATE_FORMAT
from horsebox.model import TOutput


def __encoder(value: Any) -> str:
    """
    Return a JSON string representation of a Python object.

    >>> __encoder('lorem')
    'lorem'

    >>> __encoder(None)
    ''

    >>> __encoder(datetime(2025, 4, 13, 12, 34, 56))
    '2025-04-13 12:34:56'
    """
    if value is None:
        return ''
    elif isinstance(value, datetime):
        return cast(datetime, value).strftime(DATE_FORMAT)

    return str(value)


def format_json(output: TOutput) -> Generator[str, Any, None]:
    """
    JSON formatter.

    Args:
        output (TOutput): The content to format.

    Yields:
        Generator[str, Any, None]: The formatted content.
    """
    yield json.dumps(
        output[0] if isinstance(output, List) and len(output) == 1 else output,
        indent=2,
        default=__encoder,
    )
