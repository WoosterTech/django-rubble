import pytest

from django_rubble.utils.strings import truncate_string


def test_truncate_string_basic():
    assert truncate_string("This is a long string", 10) == "This is..."
    assert truncate_string("This is a long string", 10, postfix="..") == "This is.."
    assert (
        truncate_string("This is a long string", 20, postfix="..")
        == "This is a long str.."
    )
    assert truncate_string("This is a long string", 25) == "This is a long string"


def test_truncate_string_no_truncation():
    assert truncate_string("Short", 10) == "Short"
    assert truncate_string("Exact length", 12) == "Exact length"


def test_truncate_string_with_spaces():
    assert truncate_string("This is a long string ", 10) == "This is..."
    assert truncate_string("This is a long string ", 10, postfix="..") == "This is.."
    assert (
        truncate_string("This is a long string ", 20, postfix="..")
        == "This is a long str.."
    )


@pytest.mark.parametrize(
    ("string", "num_char", "expected"),
    [
        ("", 10, ""),
        (" ", 10, ""),
        ("A", 1, "A"),
        ("A", 2, "A"),
        ("A ", 2, "A"),
    ],
)
def test_truncate_string_edge_cases(string, num_char, expected):
    assert truncate_string(string, num_char) == expected


def test_truncate_string_postfix_longer_than_num_char():
    assert truncate_string("This is a long string", 5, postfix="......") == "....."


if __name__ == "__main__":
    pytest.main()
