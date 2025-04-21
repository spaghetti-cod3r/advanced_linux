#!/usr/bin/env bash

output="$(./kernel_stack "$@" 2>&1)"
raw_status=$?

# if >127, subtract 256 to restore the original value
if (( raw_status > 127 )); then
  signed_status=$(( raw_status - 256 ))
else
  signed_status=$raw_status
fi

# print any output from the command
if [[ -n "$output" ]]; then
  printf '%s\n' "$output"
fi

# if there is an error, display its code
if [ "$signed_status" -ne 0 ]; then
    printf 'exit code: %d\n' "$signed_status" >&2
fi

