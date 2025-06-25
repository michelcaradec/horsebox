from typing import (
    Any,
    Dict,
)

import click

from horsebox import __version__
from horsebox.cli import (
    OPTION_COLLECT_AS_JSONL,
    PATTERN_ANY,
)
from horsebox.cli.combined_option import CombinedOption
from horsebox.cli.render import Format
from horsebox.collectors import CollectorType
from horsebox.commands import (
    analyze,
    build,
    config,
    inspect,
    refresh,
    schema,
    search,
)
from horsebox.indexer.analyzer import (
    FilterType,
    TokenizerType,
)


def __refine_args(**kwargs: Any) -> Dict[str, Any]:
    if kwargs.pop('json', False):
        kwargs['format'] = Format.JSON

    return kwargs


@click.group(
    context_settings={
        'help_option_names': ['-h', '--help'],
    },
)
@click.version_option(__version__)
def __cli() -> None:
    pass


# region Schema Command


@__cli.command('schema', help='Show the schema of the index.')
@click.option(
    '--json', type=bool, is_flag=True, default=False, help='Format the output as JSON (same as --format json).'
)
@click.option(
    '--format',
    type=click.Choice(list(Format), case_sensitive=False),
    default=Format.TXT,
    show_default=True,
    help='Format of the output.',
)
def __schema_cmd(**kwargs: Any) -> None:
    schema(**__refine_args(**kwargs))


# endregion
# region Configuration Command


@__cli.command('config', help='Show the configuration.')
@click.option(
    '--json', type=bool, is_flag=True, default=False, help='Format the output as JSON (same as --format json).'
)
@click.option(
    '--format',
    type=click.Choice(list(Format), case_sensitive=False),
    default=Format.TXT,
    show_default=True,
    help='Format of the output.',
)
def __config_cmd(**kwargs: Any) -> None:
    config(**__refine_args(**kwargs))


# endregion
# region Build Command


@__cli.command('build', help='Build an index.')
@click.option(
    '--from',
    '-f',
    'source',
    type=click.Path(dir_okay=True, file_okay=True, allow_dash=True),
    multiple=True,
    required=True,
    help='Datasource to index. Prefix filename with @.',
)
@click.option('--pattern', '-p', multiple=True, default=[PATTERN_ANY], show_default=True, help='Containers to index.')
@click.option('--index', '-i', required=True, help='Location where to persist the index.')
@click.option(
    '--using',
    '-u',
    'collector_type',
    type=click.Choice(list(CollectorType), case_sensitive=False),
    default=CollectorType.GUESS,
    show_default=True,
    help='Collector to use for indexing.',
)
@click.option(
    '--jsonl',
    OPTION_COLLECT_AS_JSONL,
    type=bool,
    is_flag=True,
    default=False,
    help='Collect JSON documents as JSON Lines (only with --using raw).',
)
@click.option(
    '--json', type=bool, is_flag=True, default=False, help='Format the output as JSON (same as --format json).'
)
@click.option(
    '--format',
    type=click.Choice(list(Format), case_sensitive=False),
    default=Format.TXT,
    show_default=True,
    help='Format of the output.',
)
def __build_cmd(**kwargs: Any) -> None:
    build(**__refine_args(**kwargs))


# endregion
# region Refresh Command


@__cli.command('refresh', help='Refresh an index.')
@click.option('--index', '-i', required=True, help='Location of the index.')
@click.option(
    '--json', type=bool, is_flag=True, default=False, help='Format the output as JSON (same as --format json).'
)
@click.option(
    '--format',
    type=click.Choice(list(Format), case_sensitive=False),
    default=Format.TXT,
    show_default=True,
    help='Format of the output.',
)
def __refresh_cmd(**kwargs: Any) -> None:
    refresh(**__refine_args(**kwargs))


# endregion
# region Inspect Command


@__cli.command('inspect', help='Inspect an index.')
@click.option('--index', '-i', required=True, help='Location of the index.')
@click.option(
    '--json', type=bool, is_flag=True, default=False, help='Format the output as JSON (same as --format json).'
)
@click.option(
    '--format',
    type=click.Choice(list(Format), case_sensitive=False),
    default=Format.TXT,
    show_default=True,
    help='Format of the output.',
)
def __inspect_cmd(**kwargs: Any) -> None:
    inspect(**__refine_args(**kwargs))


# endregion
# region Search Command


@__cli.command('search', help='Search an index.')
@click.option(
    '--from',
    '-f',
    'source',
    type=click.Path(dir_okay=True, file_okay=True, allow_dash=True),
    multiple=True,
    help='Datasource to index. Prefix filename with @.',
)
@click.option(
    '--pattern',
    '-p',
    type=str,
    multiple=True,
    default=['*'],
    show_default=True,
    help='Containers to index.',
    cls=CombinedOption,
    required_if='source',
    ignore_if='index',
)
@click.option('--index', '-i', help='Location of the index to build/search.')
@click.option(
    '--using',
    '-u',
    'collector_type',
    type=click.Choice(list(CollectorType), case_sensitive=False),
    default=CollectorType.GUESS,
    show_default=True,
    help='Collector to use for indexing.',
)
@click.option(
    '--jsonl',
    OPTION_COLLECT_AS_JSONL,
    type=bool,
    is_flag=True,
    default=False,
    help='Collect JSON documents as JSON Lines (only with --using raw).',
)
@click.option(
    '--query',
    '-q',
    'query_string',
    type=str,
    default='*',
    help='Search query - Syntax: https://docs.rs/tantivy/latest/tantivy/query/struct.QueryParser.html.',
)
@click.option('--limit', '-l', default=10, show_default=True, help='Number of search results.')
@click.option('--highlight', type=bool, is_flag=True, default=False, help='Highlight the found keywords.')
@click.option('--count', type=bool, is_flag=True, default=False, help='Count the number of items found.')
@click.option('--top', type=bool, is_flag=True, default=False, help='Get the top keywords of the result.')
@click.option(
    '--json', type=bool, is_flag=True, default=False, help='Format the output as JSON (same as --format json).'
)
@click.option(
    '--format',
    type=click.Choice(list(Format), case_sensitive=False),
    default=Format.TXT,
    show_default=True,
    help='Format of the output.',
)
def __search_cmd(**kwargs: Any) -> None:
    search(**__refine_args(**kwargs))


# endregion
# region Analyze Command


@__cli.command('analyze', help='Analyze some text.')
@click.option('--text', required=True, help='Text to analyze. Prefix filename with @.')
@click.option(
    '--tokenizer',
    'tokenizer_type',
    type=click.Choice(list(TokenizerType), case_sensitive=False),
    default=TokenizerType.SIMPLE,
    show_default=True,
    help='Tokenizer.',
)
@click.option('--tokenizer-params', 'tokenizer_params', type=str, help='Tokenizer parameters.')
@click.option(
    '--filter',
    'filter_types',
    type=click.Choice(list(FilterType), case_sensitive=False),
    multiple=True,
    default=[],
    show_default=True,
    help='Filter.',
)
@click.option('--filter-params', 'filter_params', type=str, help='Filter parameters.')
@click.option(
    '--json', type=bool, is_flag=True, default=False, help='Format the output as JSON (same as --format json).'
)
@click.option(
    '--format',
    type=click.Choice(list(Format), case_sensitive=False),
    default=Format.TXT,
    show_default=True,
    help='Format of the output.',
)
def __analyze_cmd(**kwargs: Any) -> None:
    analyze(**__refine_args(**kwargs))


# endregion


def main() -> None:  # noqa: D103
    __cli()


if __name__ == '__main__':
    main()
