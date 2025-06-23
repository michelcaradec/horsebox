from enum import Enum
from typing import (
    Dict,
    NoReturn,
    Optional,
    Union,
)

import click

from horsebox.formatters.json import format_json
from horsebox.formatters.text import format_txt
from horsebox.model import (
    TFormatter,
    TOutput,
)


class Format(str, Enum):
    """Rendering Formats."""

    TXT = 'txt'
    JSON = 'json'


__FORMATTERS: Dict[Format, TFormatter] = {
    Format.TXT: format_txt,
    Format.JSON: format_json,
}


def render(
    output: TOutput,
    format: Format,
) -> None:
    """
    Render an output to the terminal.

    Args:
        output (TOutput): The output to render.
        format (Format): The rendering format to use.
    """
    formatter: Optional[TFormatter] = __FORMATTERS.get(format)
    if not formatter:
        raise ValueError('No formatter found')

    for line in formatter(output):
        click.echo(line)


def render_warning(message: str) -> Union[NoReturn, None]:
    """
    Render a warning message to the terminal.

    Args:
        message (str): The warning message to render.
    """
    click.echo(click.style(message, fg='yellow'))


def render_error(message: str) -> NoReturn:
    """
    Render an error message to the terminal and exit the program.

    Args:
        message (str): The error message to render.
    """
    click.echo(click.style(message, fg='red'), err=True)

    quit(-1)
