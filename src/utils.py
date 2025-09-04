from datetime import datetime
import platform

# Global verbose flag
_verbose = False


def set_verbose(verbose: bool) -> None:
    """Set verbose logging mode"""
    global _verbose
    _verbose = verbose


def log(message: str, level: str = "INFO") -> None:
    """
    Logs a message with a timestamp. Only logs DEBUG messages when verbose is enabled.
    """
    if level == "DEBUG" and not _verbose:
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def is_raspberry_pi() -> bool:
    # Dirty hack, not suitable for mac users
    return platform.machine() in ["armv7l", "aarch64", "arm64"]
