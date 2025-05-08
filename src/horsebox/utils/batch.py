from itertools import (
    islice,
    chain,
)
from typing import (
    Iterable,
    TypeVar,
)

T = TypeVar('T')


def batched(
    iterable: Iterable[T],
    size: int,
) -> Iterable[Iterable[T]]:
    """
    Batch data from the iterable into tuples of length `size`.

    Adapted from https://docs.python.org/3/library/itertools.html#itertools.batched.

    >>> list(map(lambda b: list(b), batched('ABCDEFG', 3)))
    [['A', 'B', 'C'], ['D', 'E', 'F'], ['G']]

    >>> list(map(lambda b: list(b), batched('ABCDEF', 2)))
    [['A', 'B'], ['C', 'D'], ['E', 'F']]

    >>> list(map(lambda b: list(b), batched('ABC', 1)))
    [['A'], ['B'], ['C']]

    >>> list(map(lambda b: list(b), batched('', 1)))
    []

    Args:
        iterable (Iterable[T]): The iterable to batch.
        size (int): The size of a batch.

    Yields:
        Iterable[Iterable[T]]: The batches.
    """
    if size < 1:
        raise ValueError('size must be at least one')

    iterator = iter(iterable)
    while batch := islice(iterator, size):
        try:
            first = next(batch)
        except StopIteration:
            return
        yield chain((first,), batch)
