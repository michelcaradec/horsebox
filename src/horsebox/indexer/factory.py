import html
from datetime import datetime
from time import (
    mktime,
    struct_time,
)
from typing import (
    Any,
    Dict,
    List,
    cast,
)

from feedparser.datetimes import _parse_date

from horsebox.indexer.schema import SCHEMA_FIELD_CONTENT
from horsebox.model import TDocument
from horsebox.utils.normalize import (
    strip_html_tags,
    strip_spaces,
)

__FIELDS_MAP: Dict[str, str] = {
    'name': 'name',
    'type': 'type',
    'content': SCHEMA_FIELD_CONTENT,
    'path': 'path',
    'size': 'size',
    'date': 'date',
}
"""Mapping from parser fields to document ones (argument => schema field)."""


def prepare_doc(**kwargs: Any) -> TDocument:
    """Build a document to be indexed."""
    # If a deterministic `doc_id` is required (for document update/deletion),
    # it could be generated with `abs(hash(kwargs['path']))`

    doc: TDocument = {}

    for arg, field in __FIELDS_MAP.items():
        if value := kwargs.get(arg):
            if field == 'date':
                if isinstance(value, str):
                    # Opportunist use of the datetime parsing function of feedparser
                    dt = _parse_date(value)
                    value = datetime.fromtimestamp(mktime(cast(struct_time, dt))) if dt else None
                elif isinstance(value, struct_time):
                    value = datetime.fromtimestamp(mktime(cast(struct_time, value)))
            elif field == SCHEMA_FIELD_CONTENT:
                value = (
                    [strip_spaces(html.unescape(strip_html_tags(v))) for v in value]
                    if isinstance(value, List)
                    else strip_spaces(strip_html_tags(value))
                )

            if value:
                doc[field] = value

    if not doc.get('size') and (content := doc.get(SCHEMA_FIELD_CONTENT)):
        doc['size'] = len(content)

    return doc
