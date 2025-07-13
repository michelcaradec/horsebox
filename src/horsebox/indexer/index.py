import os
from datetime import datetime
from time import monotonic_ns
from typing import (
    Any,
    Dict,
    Iterable,
    List,
    NoReturn,
    Optional,
    OrderedDict,
    Tuple,
)

import tantivy

from horsebox.cli.config import config
from horsebox.cli.render import (
    Format,
    render,
    render_error,
    render_warning,
)
from horsebox.indexer.analyzer.factory import get_analyzer
from horsebox.indexer.build_args import IndexBuildArgs
from horsebox.indexer.metadata import (
    get_build_args,
    get_timestamp,
    set_metadata,
)
from horsebox.indexer.schema import (
    SCHEMA_ANALYZER_CUSTOM,
    SCHEMA_FIELD_CONTENT,
    SCHEMA_FIELD_CONTENT_CUSTOM,
    SCHEMA_FIELDS_CUSTOM,
    get_schema,
)
from horsebox.model import TDocument
from horsebox.model.collector import Collector
from horsebox.utils.batch import batched


def feed_index(
    collector: Collector,
    index: Optional[str] = None,
    build_args: Optional[IndexBuildArgs] = None,
    format: Format = Format.TXT,
) -> Tuple[tantivy.Index, int]:
    """
    Build an index.

    Args:
        collector (Collector): The collector used to collect the documents.
        index (Optional[str]): The path of the index.
            Defaults to None.
        build_args (Optional[IndexBuildArgs]): The arguments used to build the index.
            Defaults to None.
        format (Format): The rendering format to use.

    Returns:
        Tuple[tantivy.Index, int]:
            (the index, the build time).
    """
    documents = collector.collect()

    if collector.dry_run:
        __collect_dry_mode(documents, format)

    if index:
        os.makedirs(index, exist_ok=True)

    use_custom_field: bool = bool(build_args and build_args.custom_analyzer)

    t_index = tantivy.Index(
        get_schema(custom_fields=SCHEMA_FIELDS_CUSTOM if use_custom_field else None),
        index,
        reuse=False,
    )

    analyzer: Optional[tantivy.TextAnalyzer] = None
    if use_custom_field:
        analyzer = get_analyzer(build_args.custom_analyzer)  # type: ignore[union-attr, arg-type]
        t_index.register_tokenizer(SCHEMA_ANALYZER_CUSTOM, analyzer)

    num_threads = (os.cpu_count() or 0) // 4
    writer: tantivy.IndexWriter = t_index.writer(num_threads=num_threads)

    start = monotonic_ns()

    for batch in batched(documents, config.index_batch_size):
        for document in batch:
            if use_custom_field:
                document[SCHEMA_FIELD_CONTENT_CUSTOM] = document[SCHEMA_FIELD_CONTENT]

            writer.add_document(tantivy.Document(**document))

        writer.commit()

    writer.wait_merging_threads()

    took = monotonic_ns() - start

    if index:
        set_metadata(
            index,
            datetime.now(),
            build_args,
        )

    # Index must be reloaded for search to work
    t_index.reload()

    return (t_index, took)


def __collect_dry_mode(
    documents: Iterable[TDocument],
    format: Format,
) -> NoReturn:
    outputs: List[Dict[str, Any]] = []

    for document in documents:
        output = OrderedDict(
            container=document['path'],
        )
        if size := document.get('size'):
            output['size'] = size
        outputs.append(output)

    render(outputs, format)

    quit(0)


def open_index(
    index: str,
    format: Format,
    skip_expiration_warning: bool = False,
) -> Tuple[Optional[tantivy.Index], Optional[datetime], Optional[IndexBuildArgs]]:
    """
    Open an index.

    Args:
        index (str): The path of the index.
        format (Format): The rendering format to use.
        skip_expiration_warning (bool): Whether the warning on index expiry should be silenced or show.
            Default to False.

    Returns:
        Optional[Tuple[tantivy.Index, Optional[datetime], Optional[IndexBuildArgs]]]:
            (index object, date of creation of the index, index build arguments).
    """
    exists: bool
    try:
        exists = tantivy.Index.exists(index)
    except ValueError:
        exists = False

    if not exists:
        render_error(f'No index was found at {index}')
        return (None, None)

    t_index = tantivy.Index.open(index)
    # FIXME The metadata are read twice where it could be read only once
    timestamp = get_timestamp(index)
    build_args: Optional[IndexBuildArgs] = get_build_args(index)

    if not skip_expiration_warning and timestamp and format == Format.TXT:
        # Do not render warning in JSON mode, as it may be part of a processing pipeline
        age = datetime.now() - timestamp
        if age > config.index_expiration:
            render_warning(f'Index age limit reached: {str(age).split(".")[0]}')

    if build_args and build_args.custom_analyzer:
        analyzer = get_analyzer(build_args.custom_analyzer)
        t_index.register_tokenizer(SCHEMA_ANALYZER_CUSTOM, analyzer)

    return (t_index, timestamp, build_args)
