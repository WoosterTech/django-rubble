from importlib.util import find_spec

from .infisical import Secrets

__all__ = ["Secrets"]

if find_spec("typer") is not None:
    from . import env

    __all__ += ["env"]
