"""Backwards-compat shims for the Hermes Agent → Linket Agent CLI rename.

The ``hermes`` / ``hermes-agent`` / ``hermes-acp`` entry points are kept
as deprecated aliases that emit a one-time warning and dispatch into the
canonical ``linket`` / ``linket-agent`` / ``linket-acp`` entry points.

Plan: drop the deprecated names after two minor releases.

Implementation note — the warning is printed once per process on stderr
and is suppressed when ``LINKET_SUPPRESS_LEGACY_WARNING=1`` is set, so
cron jobs and automation that haven't migrated yet stay quiet in logs.
"""

from __future__ import annotations

import os
import sys

_WARNED: set[str] = set()


def warn_deprecated(old_name: str, new_name: str) -> None:
    """Print a one-shot deprecation hint for an old CLI command name."""
    if old_name in _WARNED:
        return
    _WARNED.add(old_name)

    if os.environ.get("LINKET_SUPPRESS_LEGACY_WARNING") == "1":
        return

    # ANSI yellow if attached to a TTY; plain text otherwise so logs stay clean.
    is_tty = hasattr(sys.stderr, "isatty") and sys.stderr.isatty()
    head = "\033[33m" if is_tty else ""
    tail = "\033[0m" if is_tty else ""
    print(
        f"{head}note: '{old_name}' is a deprecated alias for '{new_name}'. "
        f"Please update your scripts and shell aliases — '{old_name}' will be "
        f"removed in a future release. "
        f"(silence this with LINKET_SUPPRESS_LEGACY_WARNING=1){tail}",
        file=sys.stderr,
    )
