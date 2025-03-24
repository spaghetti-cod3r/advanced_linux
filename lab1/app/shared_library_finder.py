import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from file_utils import is_executable, is_shared_library, get_library_base_name
from architecture_utils import get_file_architecture
from ldd_utils import run_ldd

def find_executables_using_shared_library(exec_folder, shared_library, is_exec_dir, arch, improve):
    """Find all executable files in the folder that use the specified shared library."""
    executables_using_lib = []
    resolved_lib = os.path.realpath(shared_library)
    lib_base_name = get_library_base_name(resolved_lib)

    if is_exec_dir:
        if improve:
            with ThreadPoolExecutor() as executor:
                futures = []
                for root, dirs, files in os.walk(exec_folder):
                    for file in files:
                        file_path = os.path.join(root, file)
                        if is_executable(file_path):
                            futures.append(executor.submit(process_file, file_path, lib_base_name, arch))

                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        executables_using_lib.append(result)
        else:
            for root, dirs, files in os.walk(exec_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    if is_executable(file_path):
                        result = process_file(file_path, lib_base_name, arch)
                        if result:
                            executables_using_lib.append(result)
    else:
        if is_executable(exec_folder):
            result = process_file(exec_folder, lib_base_name, arch)
            if result:
                executables_using_lib.append(result)

    executables_using_lib.sort()
    return executables_using_lib

def process_file(file_path, lib_base_name, arch):
    """Process a single file to check if it uses the specified shared library."""
    file_arch = get_file_architecture(file_path)
    if file_arch and file_arch != arch:
        return None

    _, ldd_output = run_ldd(file_path)
    if ldd_output and lib_base_name in ldd_output:
        return file_path
    return None

def find_shared_libraries(lib_folder, is_lib_dir, arch, improve):
    """Find all shared libraries in the specified folder or return the single file."""
    shared_libraries = []
    if is_lib_dir:
        if improve:
            with ThreadPoolExecutor() as executor:
                futures = []
                for root, dirs, files in os.walk(lib_folder):
                    for file in files:
                        file_path = os.path.join(root, file)
                        futures.append(executor.submit(process_shared_library, file_path, arch))

                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        shared_libraries.append(result)
        else:
            for root, dirs, files in os.walk(lib_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    result = process_shared_library(file_path, arch)
                    if result:
                        shared_libraries.append(result)
    else:
        result = process_shared_library(lib_folder, arch)
        if result:
            shared_libraries.append(result)
    return shared_libraries

def process_shared_library(file_path, arch):
    """Process a single file to check if it's a shared library with the specified architecture."""
    if is_shared_library(file_path):
        file_arch = get_file_architecture(file_path)
        if file_arch and file_arch == arch:
            return file_path
    return None
