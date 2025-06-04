import os
from dataclasses import dataclass
from datetime import timedelta
from typing import (
    Dict,
    Optional,
    Union,
    cast,
)

_CONFIG_INDEX_BATCH_SIZE = 'HB_INDEX_BATCH_SIZE'
_CONFIG_HIGHLIGHT_MAX_CHARS = 'HB_HIGHLIGHT_MAX_CHARS'
_CONFIG_PARSER_MAX_LINE = 'HB_PARSER_MAX_LINE'
_CONFIG_PARSER_MAX_CONTENT = 'HB_PARSER_MAX_CONTENT'
_CONFIG_RENDER_MAX_CONTENT = 'HB_RENDER_MAX_CONTENT'
_CONFIG_INDEX_EXPIRATION = 'HB_INDEX_EXPIRATION'
_CONFIG_CUSTOM_STOPWORDS = 'HB_CUSTOM_STOPWORDS'
_CONFIG_STRING_NORMALIZE = 'HB_STRING_NORMALIZE'
_CONFIG_TOP_MIN_CHARS = 'HB_TOP_MIN_CHARS'


@dataclass
class Config:
    """Configuration Details."""

    description: str
    default: Optional[Union[int, str]] = None


CONFIGS: Dict[str, Config] = {
    _CONFIG_INDEX_BATCH_SIZE: Config('Batch size when indexing.', 1_000),
    _CONFIG_HIGHLIGHT_MAX_CHARS: Config('Maximum number of characters to show for highlights.', 200),
    _CONFIG_PARSER_MAX_LINE: Config('Maximum size of a line in a container (unlimited if null).'),
    _CONFIG_PARSER_MAX_CONTENT: Config('Maximum size of a container (unlimited if null).'),
    _CONFIG_RENDER_MAX_CONTENT: Config('Maximum size of a document content to render (unlimited if null).'),
    _CONFIG_INDEX_EXPIRATION: Config('Index freshness threshold (in seconds).', 3_600),
    _CONFIG_CUSTOM_STOPWORDS: Config('Custom list of stop-words (separated by a comma).'),
    _CONFIG_STRING_NORMALIZE: Config('Normalize strings when reading files (0=disabled, other value=enabled).', 1),
    _CONFIG_TOP_MIN_CHARS: Config('Minimum number of characters of a top keyword.', 1),
}


class __Config:
    """Configuration Class."""

    __index_batch_size: int
    __highlight_max_chars: int
    __parser_max_content: Optional[int]
    __parser_max_line: Optional[int]
    __render_max_content: int
    __index_expiration: timedelta
    __custom_stopwords: Optional[str]
    __string_normalize: bool
    __top_min_chars: int

    def __init__(self) -> None:  # noqa: D107
        self.__index_batch_size = cast(int, self.__get_int(_CONFIG_INDEX_BATCH_SIZE))
        self.__highlight_max_chars = cast(int, self.__get_int(_CONFIG_HIGHLIGHT_MAX_CHARS))
        self.__parser_max_content = self.__get_int(_CONFIG_PARSER_MAX_CONTENT)
        self.__parser_max_line = self.__get_int(_CONFIG_PARSER_MAX_LINE)
        self.__render_max_content = cast(int, self.__get_int(_CONFIG_RENDER_MAX_CONTENT))
        self.__index_expiration = timedelta(seconds=cast(int, self.__get_int(_CONFIG_INDEX_EXPIRATION)))
        self.__custom_stopwords = os.environ.get(_CONFIG_CUSTOM_STOPWORDS)
        self.__string_normalize = bool(self.__get_int(_CONFIG_STRING_NORMALIZE))
        self.__top_min_chars = cast(int, self.__get_int(_CONFIG_TOP_MIN_CHARS))

    def __get_int(
        self,
        key: str,
    ) -> Optional[int]:
        default = CONFIGS[key].default
        value = os.environ.get(key, default)
        try:
            return int(value)  # type: ignore
        except (ValueError, TypeError):
            # Silently fail, and return the default value
            return default  # type: ignore

    @property
    def index_batch_size(self) -> int:
        """Batch size when indexing."""
        return self.__index_batch_size

    @property
    def highlight_max_chars(self) -> int:
        """Maximum number of characters to show for highlights."""
        return self.__highlight_max_chars

    @property
    def parser_max_content(self) -> Optional[int]:
        """
        Maximum size of a container.

        Not limited if `None`.
        """
        return self.__parser_max_content

    @property
    def parser_max_line(self) -> Optional[int]:
        """
        Maximum size of a line in a container.

        Not limited if `None`.
        """
        return self.__parser_max_line

    @property
    def render_max_content(self) -> Optional[int]:
        """
        Maximum size of a document content to render.

        Not limited if `None`.
        """
        return self.__render_max_content

    @property
    def index_expiration(self) -> timedelta:
        """
        Index freshness threshold.

        Not limited if `None`.
        """
        return self.__index_expiration

    @property
    def custom_stopwords(self) -> Optional[str]:
        """Custom list of stop-words."""
        return self.__custom_stopwords

    @property
    def string_normalize(self) -> bool:
        """Custom list of stop-words."""
        return self.__string_normalize

    @property
    def top_min_chars(self) -> int:
        """Minimum number of characters of a top keyword."""
        return self.__top_min_chars


config = __Config()
"""Configuration."""
