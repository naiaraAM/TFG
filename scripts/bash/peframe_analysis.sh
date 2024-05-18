#!/bin/bash

# Save output of the command in a var

$filename

num_sections=$(objdump -h "$filename" grep 'section count:' | cut -d':' -f2 | awk '{print $1}'
)