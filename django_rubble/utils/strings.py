def sort_title(title: str) -> str:
    """Sort a title by the first word, ignoring articles.

    Articles include "a", "an", and "the".

    Examples:
        >>> sort_title("The Cat in the Hat")
        'Cat in the Hat, The'
        >>> sort_title("A Tale of Two Cities")
        'Tale of Two Cities, A'
        >>> sort_title("My Fair Lady")
        'My Fair Lady'

    Args:
        title: The title to be sorted.

    Returns:
        The sorted title.
    """
    articles = {"a", "an", "the"}

    title = title.lower()

    first, _, rest = title.partition(" ")
    return f"{rest}, {first}" if first in articles else title


def truncate_secret(
    secret: str, *, max_length: int, mask: str = "*", mask_short: bool = False
) -> str:
    """Truncate a secret to a maximum length and mask truncated characters.

    The secret is truncated to the specified length by removing characters from the
    middle of the path.

    Examples:
        >>> truncate_secret("i72BPzV54LH7lwaez5F5BF9gRuvX5Phy", max_length=20, mask=".")
        'i72BPzV...9gRuvX5Phy'
        >>> truncate_secret("C:/Users/username/Documents/file.txt", max_length=30)
        'i72BPzV54LH7***5F5BF9gRuvX5Phy'
        >>> truncate_secret(
            "i72BPzV54LH7lwaez5F5BF9gRuvX5Phy",
            max_length=40,
            mask_short=True
        )
        '****************************************'
        >>> truncate_secret(
            "i72B",
            max_length=8,
            mask_short=True
        )
        '********'

    Args:
        secret (str): The secret to be truncated.
        max_length (int): The maximum length of the truncated string.
        mask (str): The character to use for masking the truncated characters.
        mask_short (bool): Whether to mask the secret if it is already shorter than the
            maximum length.

    Returns:
        str: The truncated string.

    Raises:
        ValueError: If the secret is already shorter than the maximum length and
            mask_short is False.
    """

    if len(secret) <= max_length and not mask_short:
        msg = f"Secret is already shorter than max_length [{max_length}]"
        raise ValueError(msg)
    if len(secret) <= max_length:
        return mask * max_length

    tail_length = max_length // 2
    head_length = max_length - tail_length - 3

    head = secret[:head_length]
    tail = secret[-tail_length:]

    new_string = f"{head}{3 * mask}{tail}"

    assert len(new_string) <= max_length

    return new_string
