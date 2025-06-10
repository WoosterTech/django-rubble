import requests
from attrmagic import SimpleRoot
from furl import furl


class RuleSelector(SimpleRoot[str]): ...


json_to_python_type: dict[str, type] = {
    "string": str,
    "number": float,
    "integer": int,
    "boolean": bool,
    "array": list,
    "object": dict,
}


def generate_ruff_schema(url: furl | str):
    if not isinstance(url, furl):
        url = furl(url)
    schema_json = requests.get(url, timeout=10).json()

    return RuleSelector.model_validate(
        schema_json["definitions"]["RuleSelector"]["enum"]
    )
