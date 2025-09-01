from datetime import datetime
import platform


def log(message: str) -> None:
    """
    Logs a message with a timestamp.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def is_raspberry_pi():
    return platform.machine() in ["armv7l", "aarch64", "arm64"]
