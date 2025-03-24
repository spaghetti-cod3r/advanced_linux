import os
import re

def is_executable(file_path):
    """Check if a file is executable."""
    return os.access(file_path, os.X_OK)

def is_shared_library(file_path):
    """Check if a file is a shared library."""
    patterns = [
        r"\.so(\.\d+)*$",  # Unix-like shared libraries (may be with version number)
        r"\.dylib(\.\d+)*$",  # macOS shared libraries
        r"\.dll(\.\d+)*$",    # Windows shared libraries
    ]
    for pattern in patterns:
        if re.search(pattern, os.path.basename(file_path)):
            return True
    return False

def get_library_base_name(library_path):
    """Get the base name of a shared library (ignoring version numbers)."""
    return os.path.basename(library_path).split('.')[0] + '.so'
