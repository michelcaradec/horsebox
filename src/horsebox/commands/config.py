from collections import OrderedDict
import os
from horsebox.cli.config import CONFIGS
from horsebox.cli.render import (
    Format,
    render,
)
from horsebox.formatters.text import LINE_BREAK
from horsebox.model import TOutput


def config(format: Format) -> None:
    """
    Show the configuration.

    Args:
        format (Format): The rendering format to use.
    """
    outputs: TOutput = []

    for name, config in CONFIGS.items():
        outputs.append(
            OrderedDict(
                name=name,
                description=config.description,
                current=os.environ.get(name, config.default) or '',
                default=config.default or '',
            )
        )
        if format == Format.TXT:
            outputs.append(LINE_BREAK)

    render(outputs, format)
