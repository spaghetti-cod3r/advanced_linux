# import subprocess
# import sys

# def get_file_architecture(file_path):
#     """Get the architecture of a file using `objdump`."""
#     try:
#         result = subprocess.run(['objdump', '-f', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#         if result.returncode == 0:
#             if 'x86-64' in result.stdout or 'x64' in result.stdout:
#                 return 'x86_64'
#             elif 'i386' in result.stdout:
#                 return 'x86'
#             elif 'arm' in result.stdout and 'v7' in result.stdout:
#                 return 'armv7'
#             elif 'aarch64' in result.stdout:
#                 return 'aarch64'
#     except subprocess.CalledProcessError as e:
#         print(f"Error running 'objdump' on {file_path}: {e.stderr}", file=sys.stderr)
#     except FileNotFoundError:
#         print(f"Error: 'objdump' command not found. Please ensure it is installed.", file=sys.stderr)
#     return None

import subprocess
import sys

def get_file_architecture(file_path):
    """Get the architecture of a file using `file` utility."""
    try:
        result = subprocess.run(
            ['file', '-b', file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode == 0:
            output = result.stdout.lower()
            print(output)
            
            if 'x86-64' in output:
                return 'x86_64'
            elif 'i386' in output or '32-bit' in output:
                return 'x86'
            elif 'armv7' in output or ('arm' in output and 'v7' in output):
                return 'armv7'
            elif 'aarch64' in output or 'arm64' in output:
                return 'aarch64'
            else:
                return None
    except subprocess.CalledProcessError as e:
        print(f"Error running 'file' on {file_path}: {e.stderr}", file=sys.stderr)
    except FileNotFoundError:
        print("Error: 'file' command not found. Please install it.", file=sys.stderr)
    return None