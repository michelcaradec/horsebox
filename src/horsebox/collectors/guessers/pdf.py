from typing import (
    Any,
    Dict,
    Optional,
    Tuple,
)

from horsebox.collectors import CollectorType


def guess_pdf(item: str) -> Optional[Tuple[CollectorType, Dict[str, Any]]]:
    """
    Guess the use of the PDF collector from an item.

    >>> guess_pdf('file.txt') is None
    True

    >>> guess_pdf('file.pdf')
    (<CollectorType.PDF: 'pdf'>, {})

    Args:
        item (str): The item to check.

    Returns:
        Optional[Tuple[CollectorType, Dict[str, Any]]]:
        - The type of the collector.
        - Some extra arguments to use with the collector.
    """
    if item.endswith('.pdf'):
        return (CollectorType.PDF, {})

    return None
