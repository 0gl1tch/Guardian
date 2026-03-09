import urllib.request
import urllib.error
import hashlib
import os
import sys
import platform


def download_bootstrap(url: str, dest: str = "bootstrap.sh", verify_sha256: str | None = None, timeout: int = 15):
    """Download a bootstrap script to `dest` and optionally verify sha256.

    Raises urllib.error.URLError or ValueError on mismatch.
    Uses only stdlib - no external dependencies.
    """
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            with open(dest, "wb") as f:
                while True:
                    chunk = response.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)
    except urllib.error.URLError as e:
        if os.path.exists(dest):
            os.remove(dest)
        raise RuntimeError(f"Failed to download from {url}: {e}")

    if verify_sha256:
        h = hashlib.sha256()
        with open(dest, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        actual = h.hexdigest()
        if actual != verify_sha256:
            os.remove(dest)
            raise ValueError(f"sha256 mismatch: expected {verify_sha256}, got {actual}")

    # Set executable permission on Unix-like systems
    if platform.system() != "Windows":
        os.chmod(dest, 0o750)
    
    return dest
