"""Generate the code reference pages."""

from collections.abc import Iterable
from pathlib import Path

import mkdocs_gen_files
from loguru import logger

nav = mkdocs_gen_files.Nav()

root = Path(__file__).parent.parent
src = root

msg = f"src path: {src}"
logger.debug(msg)


def any_in_iterable(iterable: Iterable[str], values: Iterable[str]) -> bool:
    """Check if any of the values are in the iterable."""
    return any(value in iterable for value in values)


for path in sorted(src.rglob("*.py")):
    module_path = path.relative_to(src).with_suffix("")
    doc_path = path.relative_to(src).with_suffix(".md")
    full_doc_path = Path("reference", doc_path)

    parts = tuple(module_path.parts)

    if parts[-1] == "__init__":
        parts = parts[:-1]
        if len(parts) == 0:
            continue
        doc_path = doc_path.with_name("index.md")
        full_doc_path = full_doc_path.with_name("index.md")
    elif "test" in parts or parts[-1] == "__main__":
        msg = f"Skipping {module_path}"
        logger.debug(msg)

        continue

    nav[parts] = doc_path.as_posix()

    with mkdocs_gen_files.open(full_doc_path, "w") as nav_file:
        identifier = ".".join(parts)
        print("::: " + identifier, file=nav_file)

    mkdocs_gen_files.set_edit_path(full_doc_path, path.relative_to(root))

literate_nav = nav.build_literate_nav()

msg = f"literate_nav: {literate_nav}"
logger.debug(msg)


with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(literate_nav)
