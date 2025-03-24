import subprocess
import sys

def get_file_architecture(file_path):
    """Get the architecture of a file using `objdump`."""
    try:
        result = subprocess.run(['objdump', '-f', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            if 'x86-64' in result.stdout or 'x64' in result.stdout:
                return 'x86_64'
            elif 'i386' in result.stdout:
                return 'x86'
            elif 'arm' in result.stdout and 'v7' in result.stdout:
                return 'armv7'
            elif 'aarch64' in result.stdout:
                return 'aarch64'
    except subprocess.CalledProcessError as e:
        print(f"Error running 'objdump' on {file_path}: {e.stderr}", file=sys.stderr)
    except FileNotFoundError:
        print(f"Error: 'objdump' command not found. Please ensure it is installed.", file=sys.stderr)
    return None
