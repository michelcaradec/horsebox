from collections import OrderedDict
from horsebox.cli.render import (
    Format,
    render,
)
from horsebox.indexer.schema import SCHEMA_FIELDS


def schema(format: Format) -> None:
    """
    Show the schema of the index.

    Args:
        format (Format): The rendering format to use.
    """
    output = OrderedDict()

    for field in SCHEMA_FIELDS:
        output[field.name] = {
            'type': field.type.value,
            'description': field.description,
        }

    render(output, format)
