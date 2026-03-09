import subprocess


def execute(cmd: str, timeout: int = 600):
    """Execute a shell command and return (returncode, stdout, stderr)."""
    try:
        p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except Exception as e:
        return 1, "", str(e)
