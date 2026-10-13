"""Schowek wieloplatformowy (macOS/Linux/Windows) — komenda wstrzykiwalna do testów."""
import platform
import subprocess
from typing import List, Optional


def _command_for(platform_name: str) -> Optional[List[str]]:
    if platform_name == "Darwin":
        return ["pbcopy"]
    if platform_name == "Linux":
        # Wayland lub X11
        return ["wl-copy"] if _which("wl-copy") else (["xclip", "-selection", "clipboard"] if _which("xclip") else None)
    if platform_name == "Windows":
        return ["powershell", "-command", "$input | Set-Clipboard"]
    return None


def _which(name: str) -> Optional[str]:
    from shutil import which
    return which(name)


def copy_to_clipboard(text: str, command: Optional[List[str]] = None) -> bool:
    """Kopiuje tekst do schowka. Zwraca True/False; komendę można wstrzyknąć w testach."""
    cmd = command or _command_for(platform.system())
    if not cmd:
        return False
    try:
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        proc.communicate(text.encode("utf-8"))
        return proc.returncode == 0
    except OSError:
        return False
