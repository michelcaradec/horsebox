from typing import (
    Any,
    List,
    Tuple,
)

import click


class CombinedOption(click.Option):
    """Combined Options Support Class."""

    def __init__(self, *args, **kwargs) -> None:  # noqa: D107
        self.required_if = kwargs.pop('required_if')
        self.ignore_if = kwargs.pop('ignore_if', None)

        super().__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args) -> Tuple[Any, List[str]]:  # noqa: D102
        if (
            # The option can't be ignored due to the presence of another option
            self.ignore_if not in opts
            # The associated option is not provided
            and self.required_if not in opts
        ):
            raise click.UsageError(f'Option {self.required_if} is required with {self.name}')

        return super().handle_parse_result(ctx, opts, args)
