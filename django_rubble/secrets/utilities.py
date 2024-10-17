import ast
from pathlib import Path
from typing import override

from loguru import logger
from rich import print


class SecretsFinder(ast.NodeVisitor):
    def __init__(self):
        self.secrets = []

    @override
    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute):
            if node.func.attr == "get_secret":
                for keyword in node.args:
                    value = keyword.value
                    logger.info(f"Found secret: {value}")
                    self.secrets.append(value)
        self.generic_visit(node)


def find_secrets_in_settings(settings_file: str):
    settings_file_path = Path(settings_file)
    with settings_file_path.open("r") as file:
        tree = ast.parse(file.read(), filename=settings_file)

    finder = SecretsFinder()
    finder.visit(tree)
    return finder.secrets


def create_env_sample(secrets: list[str], output_file: str):
    output_file_path = Path(output_file)

    with output_file_path.open("w") as file:
        for secret in secrets:
            file.write(f"{secret.upper()}=\n")


if __name__ == "__main__":
    settings_file_path = "C:/Users/KW131407/repos/homebin/config/settings/production.py"
    output_file_path = ".env.sample"

    secrets = find_secrets_in_settings(settings_file_path)
    print(f"Secrets found in settings file: {secrets}")
    create_env_sample(secrets, output_file_path)
    print(f"Sample .env file created at {output_file_path}")
