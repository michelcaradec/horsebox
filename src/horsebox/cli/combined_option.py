from typing import (
    Any,
    List,
    Mapping,
    Tuple,
)

import click


class CombinedOption(click.Option):
    """Combined Options Support Class."""

    def __init__(  # noqa: D107
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self.required_if = kwargs.pop('required_if')
        self.ignore_if = kwargs.pop('ignore_if', None)
        self.fallback_value = kwargs.pop('fallback_value', None)

        super().__init__(*args, **kwargs)

    def handle_parse_result(  # noqa: D102
        self,
        ctx: click.Context,
        opts: Mapping[str, Any],
        args: List[str],
    ) -> Tuple[Any, List[str]]:
        if (
            # The option can't be ignored due to the presence of another option
            self.ignore_if not in opts
            # The associated option is not provided
            and self.required_if not in opts
        ):
            raise click.UsageError(f'Option {self.required_if} is required with {self.name}')

        if self.name not in opts and self.fallback_value:
            # `opts` is not mutable, use the default value
            self.default = self.fallback_value

        return super().handle_parse_result(ctx, opts, args)  # type: ignore[no-any-return]
