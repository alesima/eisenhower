"""Shared helpers to resolve the user data directory.

Uses GLib.get_user_data_dir() so the path respects XDG_DATA_HOME and,
inside the Flatpak sandbox, maps to the app's private data directory
(~/.var/app/<app-id>/data). Falls back to ~/.local/share when GLib is
unavailable (e.g. headless test environments).
"""

import os
from pathlib import Path

APP_DATA_DIR_NAME = "eisenhower"


def default_data_dir() -> Path:
    """Return the directory where task/project JSON files are stored."""
    try:
        from gi.repository import GLib

        base = Path(GLib.get_user_data_dir())
    except Exception:
        base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    data_dir = base / APP_DATA_DIR_NAME
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def resolve_data_file(filename: str) -> Path:
    """Resolve a data file, migrating from the legacy location if needed.

    Existing users (pre-Flatpak or older releases) may have files under
    ~/.local/share/eisenhower while XDG_DATA_HOME points elsewhere.
    In that case the legacy file is moved to the new location once.
    """
    target = default_data_dir() / filename
    if target.exists():
        return target

    legacy = Path.home() / ".local" / "share" / APP_DATA_DIR_NAME / filename
    if legacy.exists() and legacy.resolve() != target.resolve():
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            legacy.replace(target)
            return target
        except OSError:
            return legacy
    return target
