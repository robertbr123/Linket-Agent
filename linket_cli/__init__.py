"""Canonical Linket alias package for the legacy ``hermes_cli`` package."""

import hermes_cli as _hermes_cli

from hermes_cli import *  # noqa: F401,F403

__all__ = getattr(_hermes_cli, "__all__", [])
__file__ = getattr(_hermes_cli, "__file__", __file__)
__path__ = list(getattr(_hermes_cli, "__path__", []))
__version__ = getattr(_hermes_cli, "__version__", None)
__release_date__ = getattr(_hermes_cli, "__release_date__", None)


def __getattr__(name):
    return getattr(_hermes_cli, name)


def __dir__():
    return sorted(set(globals()) | set(dir(_hermes_cli)))
