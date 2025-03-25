# import subprocess
# import sys

# def run_ldd(file_path):
#     """Run ldd on an executable and return its output."""
#     try:
#         result = subprocess.run(['ldd', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#         if result.returncode == 0:
#             return file_path, result.stdout
#     except subprocess.CalledProcessError as e:
#         print(f"Error running 'ldd' on {file_path}: {e.stderr}", file=sys.stderr)
#     except FileNotFoundError:
#         print(f"Error: 'ldd' command not found. Please ensure it is installed.", file=sys.stderr)
#     return file_path, None

import subprocess
import sys

def run_objdump_needed(file_path):
    """Run objdump -x | grep NEEDED to get dependencies."""
    try:
        result = subprocess.run(
            ['objdump', '-x', file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode == 0:
            needed_libs = []
            for line in result.stdout.split('\n'):
                if 'NEEDED' in line:
                    lib = line.split('NEEDED')[-1].strip()
                    needed_libs.append(lib)
            return file_path, needed_libs
    except subprocess.CalledProcessError as e:
        print(f"Error running 'objdump' on {file_path}: {e.stderr}", file=sys.stderr)
    except FileNotFoundError:
        print(f"Error: 'objdump' not found. Install binutils.", file=sys.stderr)
    return file_path, None

def run_readelf_dynamic(file_path):
    """Alternative: Use readelf -d | grep NEEDED."""
    try:
        result = subprocess.run(
            ['readelf', '-d', file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode == 0:
            needed_libs = []
            for line in result.stdout.split('\n'):
                if 'NEEDED' in line:
                    lib = line.split('[')[-1].split(']')[0].strip()
                    needed_libs.append(lib)
            return file_path, needed_libs
    except subprocess.CalledProcessError as e:
        print(f"Error running 'readelf' on {file_path}: {e.stderr}", file=sys.stderr)
    except FileNotFoundError:
        print(f"Error: 'readelf' not found. Install binutils.", file=sys.stderr)
    return file_path, None