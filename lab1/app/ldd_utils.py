import subprocess
import sys

def run_ldd(file_path):
    """Run ldd on an executable and return its output."""
    try:
        result = subprocess.run(['ldd', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            return file_path, result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running 'ldd' on {file_path}: {e.stderr}", file=sys.stderr)
    except FileNotFoundError:
        print(f"Error: 'ldd' command not found. Please ensure it is installed.", file=sys.stderr)
    return file_path, None
