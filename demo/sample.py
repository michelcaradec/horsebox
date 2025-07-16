from typing import (
    Dict,
    List,
    Tuple,
)


def tokenize_me(text: str) -> List[str]:
    """
    Split a text into tokens.

    Args:
        text (str): The text to tokenize.

    Returns:
        List[str]: The tokens.
    """
    words = text.split(',')

    return [word for word in words if len(word) > 2]


def get_top_count(
    text: str,
    count: int = 5,
) -> List[Tuple[str, int]]:
    """
    Get the top count words of a string.

    Args:
        text (str): The string to count the words from.
        count (int, optional): The number of top words to return.
            Defaults to 5.

    Returns:
        List[Tuple[str, int]]: The top words.
    """
    top: Dict[str, int] = {}
    for word in text.split():
        top[word] = top.get(word, 0) + 1

    items = sorted(top.items(), key=lambda i: i[1], reverse=True)
    return items[:count]
