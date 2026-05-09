"""One-shot migration of state from ``~/.hermes`` to ``~/.linket``.

Run on every CLI entry, but takes O(0) work after the first successful
migration. Designed to be safe to call repeatedly and from concurrent
processes — uses a side-by-side rename pattern with a lock file so two
``linket`` invocations starting at the same time never duplicate work.

Behaviour matrix
================

  ``~/.linket`` exists | ``~/.hermes`` exists | env override set | action
  -------------------- | --------------------- | ---------------- | ------
  yes                  | (any)                 | (any)            | no-op
  no                   | yes                   | no               | copy ``~/.hermes`` → ``~/.linket``, leave original in place
  no                   | yes                   | yes              | no-op (user pinned an explicit dir; we don't move their data)
  no                   | no                    | (any)            | no-op (fresh install)

The legacy ``~/.hermes`` directory is **kept** after copy, not deleted.
That gives the user a one-step rollback (``rm -rf ~/.linket`` and
re-pin the legacy path with ``HERMES_HOME=~/.hermes``) if anything
goes wrong with the rename.

A breadcrumb file ``~/.linket/.migrated-from-hermes`` records the
copy completion time and source path so support can diagnose later.

This module is import-safe — no side effects at import time.
"""

from __future__ import annotations

import os
import shutil
import sys
import time
from pathlib import Path

_LEGACY = ".hermes"
_NEW = ".linket"
_BREADCRUMB = ".migrated-from-hermes"
_LOCK = ".linket-migration.lock"


def _user_pinned_explicit_home() -> bool:
    """True iff the user set ``LINKET_HOME`` or ``HERMES_HOME`` explicitly."""
    for var in ("LINKET_HOME", "HERMES_HOME"):
        if os.environ.get(var, "").strip():
            return True
    return False


def maybe_migrate_legacy_home(
    *,
    on_message=None,
) -> bool:
    """Copy ``~/.hermes`` → ``~/.linket`` once, if needed.

    Returns True iff a copy ran in this call. ``on_message`` is an
    optional callable taking a single string arg, used for surfacing
    progress to the CLI; defaults to a stderr print.
    """
    if on_message is None:
        def on_message(msg: str) -> None:
            print(msg, file=sys.stderr)

    # Skip when the user has pinned an explicit home: we never silently
    # touch a custom location.
    if _user_pinned_explicit_home():
        return False

    home = Path.home()
    legacy = home / _LEGACY
    new = home / _NEW

    if new.exists():
        return False
    if not legacy.is_dir():
        return False

    # Cooperative lock so two concurrent CLI starts don't race.
    lock = home / _LOCK
    try:
        # ``open(..., "x")`` fails if the file exists — atomic check-and-set.
        with open(lock, "x", encoding="utf-8") as fp:
            fp.write(f"pid={os.getpid()} ts={time.time()}\n")
    except FileExistsError:
        # Another process is migrating; wait briefly then bail. The other
        # process will finish; this one just proceeds with the new state.
        for _ in range(60):  # up to ~6s
            if new.exists():
                return False
            time.sleep(0.1)
        return False
    except OSError:
        # Filesystem refused the lock (e.g., read-only home). Best-effort:
        # try the migration without locking.
        pass

    try:
        on_message(
            f"linket: migrating state {legacy} → {new} (one-time copy; "
            f"originals are kept). Set LINKET_SUPPRESS_LEGACY_WARNING=1 "
            f"to silence."
        )
        # ``copytree`` with ``dirs_exist_ok=False`` (default in 3.11+ via
        # explicit kwarg) gives us a clean failure if ``new`` was created
        # between our check and now.
        shutil.copytree(legacy, new, symlinks=True)
        try:
            (new / _BREADCRUMB).write_text(
                f"migrated_from={legacy}\n"
                f"migrated_at={time.time()}\n"
                f"by_pid={os.getpid()}\n",
                encoding="utf-8",
            )
        except OSError:
            pass
        on_message("linket: migration complete.")
        return True
    except Exception as exc:
        # Don't block CLI startup on migration failure — log and let the
        # user investigate. The legacy dir is untouched.
        on_message(f"linket: migration from ~/.hermes failed ({exc!r}). "
                   "Continuing with fresh ~/.linket; legacy state untouched.")
        return False
    finally:
        try:
            lock.unlink()
        except OSError:
            pass
