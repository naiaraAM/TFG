#!/bin/bash

# Directory paths relative to the location of the script
script_directory="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
root_directory="$script_directory/../../samples"
output_directory="$script_directory/../../results_analysis"
python_script_directory="$script_directory/../../scripts/python"

output_file="sample_basic_info.tsv"

# If directory does not exist, create it
if [ ! -d "$output_directory" ]; then
    mkdir "$output_directory"
fi

# If filename does not exist, create it
if [ ! -f "$output_directory/$output_file" ]; then
    touch "$output_directory/$output_file"
    echo -e "filename\tmalware_name\tsource\tcategory\tfirst_bytes\tnum_sections\tcompiler" > "$output_directory/$output_file"
fi

find "$root_directory" -type f -print | while read -r file; do
    filename=$(basename "$file")
    # If filename already exists in the output file, skip processing, avoids overhead of processing
    if grep -q "$filename" "$output_directory/$output_file"; then
        continue
    fi

    malware_name=$(basename "$(dirname "$file")")
    source=$(basename "$(dirname "$(dirname "$file")")")
    category="Original dataset"
    first_bytes=$(python3 "$python_script_directory/x86_disassembler.py" "$file")
    num_sections=$(pescan "$file" | grep 'section count:' | cut -d':' -f2 | awk '{print $1}')
    compiler=$(pestr "$file" | grep "COMPILER=" | awk -F'=' '{print $2}')
    if [ "$malware_name" == "webapp_uploads" ]; then
        source=$malware_name
        malware_name="Not defined"
        category="User uploaded"
    fi
    # If compiler is empty, then compiler value to "Unknown"
    if [ -z "$compiler" ]; then
        compiler="Unknown"
    fi
    echo -e "$filename\t$malware_name\t$source\t$category\t$first_bytes\t$num_sections\t$compiler" >> "$output_directory/$output_file"
done