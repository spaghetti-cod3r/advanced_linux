# import os
# import sys
# import argparse
# import signal
# from shared_library_finder import find_shared_libraries, find_executables_using_shared_library
# from output_utils import save_to_txt, save_to_pdf

# # ANSI escape codes for colors
# COLORS = {
#     "HEADER": "\033[95m",  # Purple
#     "OKBLUE": "\033[94m",  # Blue
#     "OKGREEN": "\033[92m",  # Green
#     "WARNING": "\033[93m",  # Yellow
#     "FAIL": "\033[91m",  # Red
#     "ENDC": "\033[0m",  # Reset color
#     "BOLD": "\033[1m",  # Bold
#     "UNDERLINE": "\033[4m",  # Underline
# }

# def signal_handler(sig, frame):
#     """Exit gracefully."""
#     print("\nApp interrupted by user. Exiting gracefully...")
#     sys.exit(0)

# def colorize(text, color, use_colors=True):
#     """Apply color to the given text if use_colors is True."""
#     if use_colors:
#         return f"{COLORS[color]}{text}{COLORS['ENDC']}"
#     return text

# def main():
#     # Set up argument parsing with help documentation
#     parser = argparse.ArgumentParser(
#         description="Find executables that use specified shared libraries.",
#         epilog="Examples:\n"
#                "  python3 main.py -lib=f -exec=f /lib/x86_64-linux-gnu/libc.so.6 /bin/ls\n"
#                "  python3 main.py -lib=d -exec=d -output=txt /lib/x86_64-linux-gnu /bin\n"
#                "  python3 main.py -lib=f -exec=d -output=pdf -arch=armv7 /lib/arm-linux-gnueabihf/libc.so.6 /bin",
#         formatter_class=argparse.RawTextHelpFormatter
#     )
#     parser.add_argument('-lib', required=True, choices=['d', 'f'],
#                         help="Specify whether the input is a directory (-lib=d) or a single file (-lib=f).")
#     parser.add_argument('-exec', required=True, choices=['d', 'f'],
#                         help="Specify whether the input is a directory (-exec=d) or a single file (-exec=f).")
#     parser.add_argument('-output', choices=['terminal', 'pdf', 'txt'], default='terminal',
#                         help="Specify the output format: 'terminal' (default), 'pdf', or 'txt'.")
#     parser.add_argument('-hide', action='store_true',
#                         help="Suppress output for shared libraries with no executable files using them.")
#     parser.add_argument('-arch', choices=['x86', 'x86_64', 'armv7', 'aarch64'],
#                         help="Specify the architecture: x86, x86_64, armv7, aarch64. If not specified, all architectures are accepted.")
#     parser.add_argument('-improve', action='store_true',
#                         help="Use ThreadPoolExecutor to improve performance.")
#     parser.add_argument('lib_path',
#                         help="Path to the shared library or directory containing shared libraries.")
#     parser.add_argument('exec_path',
#                         help="Path to the executable or directory containing executables.")
#     parser.add_argument('output_filename', nargs='?',
#                         help="Name of the output file (optional for 'pdf' and 'txt').")
#     args = parser.parse_args()

#     # Register the signal handler for Ctrl+C
#     signal.signal(signal.SIGINT, signal_handler)

#     # Determine if colors should be used
#     use_colors = args.output == 'terminal'

#     # Validate arguments
#     if args.lib == 'd' and not os.path.isdir(args.lib_path):
#         print(f"{colorize(f'Error: {args.lib_path} is not a valid directory.', 'FAIL', use_colors)}", file=sys.stderr)
#         sys.exit(1)
#     elif args.lib == 'f' and not os.path.isfile(args.lib_path):
#         print(f"{colorize(f'Error: {args.lib_path} is not a valid file.', 'FAIL', use_colors)}", file=sys.stderr)
#         sys.exit(1)

#     if args.exec == 'd' and not os.path.isdir(args.exec_path):
#         print(f"{colorize(f'Error: {args.exec_path} is not a valid directory.', 'FAIL', use_colors)}", file=sys.stderr)
#         sys.exit(1)
#     elif args.exec == 'f' and not os.path.isfile(args.exec_path):
#         print(f"{colorize(f'Error: {args.exec_path} is not a valid file.', 'FAIL', use_colors)}", file=sys.stderr)
#         sys.exit(1)

#     # Set default output filename if not provided
#     if args.output in ('pdf', 'txt') and not args.output_filename:
#         args.output_filename = f"output.{args.output}"

#     # Find shared libraries
#     shared_libraries = find_shared_libraries(args.lib_path, args.lib == 'd', args.arch, args.improve)
#     if not shared_libraries:
#         print(f"{colorize(f'No shared libraries found in {args.lib_path}', 'WARNING', use_colors)}", file=sys.stderr)
#         sys.exit(0)

#     # Prepare output
#     output = ""
#     library_usage = []

#     # Collect the number of executables for each shared library
#     for shared_library in shared_libraries:
#         executables = find_executables_using_shared_library(args.exec_path, shared_library, args.exec == 'd', args.arch, args.improve)
#         library_usage.append((shared_library, len(executables)))

#     # Sort shared libraries by the number of executables (from highest to lowest)
#     library_usage.sort(key=lambda x: x[1], reverse=True)

#     # Generate output based on the sorted list
#     for shared_library, usage_count in library_usage:
#         executables = find_executables_using_shared_library(args.exec_path, shared_library, args.exec == 'd', args.arch, args.improve)
#         if executables:
#             output += f"\n{colorize('=== Shared Library:', 'HEADER', use_colors)} {colorize(shared_library, 'OKBLUE', use_colors)}\n"
#             output += f"{colorize('Number of executables using this library:', 'OKGREEN', use_colors)} {colorize(usage_count, 'FAIL', use_colors)}\n"
#             output += f"{colorize('Executable files:', 'OKGREEN', use_colors)}\n"
#             for exe in sorted(executables):  # Sort executables lexicographically
#                 output += f"- {colorize(exe, 'BOLD', use_colors)}\n"
#         elif not args.hide:
#             output += f"\n{colorize('=== Shared Library:', 'HEADER', use_colors)} {colorize(shared_library, 'OKBLUE', use_colors)}\n"
#             output += f"{colorize('No executable files found that use this library.', 'WARNING', use_colors)}\n"

#     # Handle output based on the -output flag
#     if args.output == 'terminal':
#         print(output)
#     elif args.output == 'txt':
#         save_to_txt(output, args.output_filename)
#         print(f"{colorize(f'Output saved to {args.output_filename}', 'OKGREEN', use_colors)}")
#     elif args.output == 'pdf':
#         save_to_pdf(output, args.output_filename)
#         print(f"{colorize(f'Output saved to {args.output_filename}', 'OKGREEN', use_colors)}")

# if __name__ == "__main__":
#     main()

#!/usr/bin/env python3

import os
import sys
import argparse
import signal
from shared_library_finder import find_shared_libraries, find_executables_using_shared_library
from output_utils import save_to_txt, save_to_pdf

# ANSI escape codes for colors
COLORS = {
    "HEADER": "\033[95m",  # Purple
    "OKBLUE": "\033[94m",  # Blue
    "OKGREEN": "\033[92m",  # Green
    "WARNING": "\033[93m",  # Yellow
    "FAIL": "\033[91m",  # Red
    "ENDC": "\033[0m",  # Reset color
    "BOLD": "\033[1m",  # Bold
    "UNDERLINE": "\033[4m",  # Underline
}

def signal_handler(sig, frame):
    """Exit gracefully."""
    print("\nApp interrupted by user. Exiting gracefully...")
    sys.exit(0)

def colorize(text, color, use_colors=True):
    """Apply color to the given text if use_colors is True."""
    if use_colors:
        return f"{COLORS[color]}{text}{COLORS['ENDC']}"
    return text

def main():
    # Set up argument parsing with help documentation
    parser = argparse.ArgumentParser(
        description="Find executables that use specified shared libraries.",
        epilog="Examples:\n"
               "  bldd.py -lib=f -exec=f /lib/x86_64-linux-gnu/libc.so.6 /bin/ls\n"
               "  bldd.py -lib=d -exec=d -output=txt /lib/x86_64-linux-gnu /bin\n"
               "  bldd.py -lib=f -exec=d -output=pdf -arch=armv7 /lib/arm-linux-gnueabihf/libc.so.6 /bin\n"
               "  bldd.py -lib=f -exec=f -hide libs/libm.so.6 exec/cut",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('-lib', required=True, choices=['d', 'f'],
                        help="Specify whether the input is a directory (-lib=d) or a single file (-lib=f).")
    parser.add_argument('-exec', required=True, choices=['d', 'f'],
                        help="Specify whether the input is a directory (-exec=d) or a single file (-exec=f).")
    parser.add_argument('-output', choices=['terminal', 'pdf', 'txt'], default='terminal',
                        help="Specify the output format: 'terminal' (default), 'pdf', or 'txt'.")
    parser.add_argument('-hide', action='store_true',
                        help="Suppress output for shared libraries with no executable files using them.")
    parser.add_argument('-arch', choices=['x86', 'x86_64', 'armv7', 'aarch64'],
                        help="Specify the architecture: x86, x86_64, armv7, aarch64. If not specified, all architectures are accepted.")
    parser.add_argument('-improve', action='store_true',
                        help="Use ThreadPoolExecutor to improve performance.")
    parser.add_argument('lib_path',
                        help="Path to the shared library or directory containing shared libraries.")
    parser.add_argument('exec_path',
                        help="Path to the executable or directory containing executables.")
    parser.add_argument('output_filename', nargs='?',
                        help="Name of the output file (optional for 'pdf' and 'txt').")
    args = parser.parse_args()

    # Register the signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    # Determine if colors should be used
    use_colors = args.output == 'terminal'

    # Validate arguments
    if args.lib == 'd' and not os.path.isdir(args.lib_path):
        print(f"{colorize(f'Error: {args.lib_path} is not a valid directory.', 'FAIL', use_colors)}", file=sys.stderr)
        sys.exit(1)
    elif args.lib == 'f' and not os.path.isfile(args.lib_path):
        print(f"{colorize(f'Error: {args.lib_path} is not a valid file.', 'FAIL', use_colors)}", file=sys.stderr)
        sys.exit(1)

    if args.exec == 'd' and not os.path.isdir(args.exec_path):
        print(f"{colorize(f'Error: {args.exec_path} is not a valid directory.', 'FAIL', use_colors)}", file=sys.stderr)
        sys.exit(1)
    elif args.exec == 'f' and not os.path.isfile(args.exec_path):
        print(f"{colorize(f'Error: {args.exec_path} is not a valid file.', 'FAIL', use_colors)}", file=sys.stderr)
        sys.exit(1)

    # Set default output filename if not provided
    if args.output in ('pdf', 'txt') and not args.output_filename:
        args.output_filename = f"output.{args.output}"

    # Find shared libraries
    shared_libraries = find_shared_libraries(args.lib_path, args.lib == 'd', args.arch, args.improve)
    if not shared_libraries:
        print(f"{colorize(f'No shared libraries found matching criteria in {args.lib_path}', 'WARNING', use_colors)}", file=sys.stderr)
        sys.exit(0)

    # Prepare output
    output = ""
    library_usage = []

    # Collect the number of executables for each shared library
    for shared_library in shared_libraries:
        executables = find_executables_using_shared_library(args.exec_path, shared_library, args.exec == 'd', args.arch, args.improve)
        library_usage.append((shared_library, len(executables)))

    # Filter out empty results if -hide is specified
    if args.hide:
        library_usage = [(lib, count) for lib, count in library_usage if count > 0]

    if not library_usage:
        print(f"{colorize('No executables found using the specified libraries', 'WARNING', use_colors)}")
        sys.exit(0)

    # Sort shared libraries by the number of executables (from highest to lowest)
    library_usage.sort(key=lambda x: x[1], reverse=True)

    # Generate output based on the sorted list
    for shared_library, usage_count in library_usage:
        executables = find_executables_using_shared_library(args.exec_path, shared_library, args.exec == 'd', args.arch, args.improve)
        output += f"\n{colorize('======== Shared Library:', 'HEADER', use_colors)} {colorize(shared_library, 'OKBLUE', use_colors)}\n"
        output += f"{colorize('Number of executables using this library:', 'OKGREEN', use_colors)} {colorize(usage_count, 'FAIL', use_colors)}\n"
        
        if executables:
            output += f"{colorize('Executable files:', 'OKGREEN', use_colors)}\n"
            for exe in sorted(executables):  # Sort executables lexicographically
                output += f"- {colorize(exe, 'BOLD', use_colors)}\n"
        elif not args.hide:
            output += f"{colorize('No executable files found that use this library.', 'WARNING', use_colors)}\n"

    # Handle output based on the -output flag
    if args.output == 'terminal':
        print(output)
    elif args.output == 'txt':
        save_to_txt(output, args.output_filename)
        print(f"{colorize(f'Output saved to {args.output_filename}', 'OKGREEN', use_colors)}")
    elif args.output == 'pdf':
        save_to_pdf(output, args.output_filename)
        print(f"{colorize(f'Output saved to {args.output_filename}', 'OKGREEN', use_colors)}")

if __name__ == "__main__":
    main()