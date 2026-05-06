"""Check that basic features work.

Catch cases where e.g., files are missing so the import doesn't work. It is recommended
to check that e.g., assets are included."""

from django_rubble.utils.numeric_utils import is_number


def test_basic_imports():
    """Test that basic imports and functions work."""
    _ = is_number(10)


if __name__ == "__main__":
    try:
        from rich import print

        msg = "[bold green]🎉 Smoke test succeeded 🎉[/bold green]"
    except ImportError:
        msg = "Smoke test succeeded"

    try:
        test_basic_imports()
        print(msg)
    except Exception as e:
        raise RuntimeError("Smoke test failed") from e
