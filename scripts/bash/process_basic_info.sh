#!/bin/bash

# This script processes the basic information of the samples in the dataset.

# Relative path to the directory containing this script
script_directory="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
root_directory="$script_directory/../../samples"
output_directory="$script_directory/../../results_analysis"
python_script_directory="$script_directory/../../scripts/python"

output_file="$output_directory/sample_basic_info.tsv"
temp_file="$output_directory/sample_basic_info.tmp"

# Create output directory if it does not exist
mkdir -p "$output_directory"

# Creates the output file if it does not exist
if [ ! -f "$output_file" ]; then
    echo -e "filename\tmalware_name\tsource\tcategory\tfirst_bytes\tnum_sections\tcompiler" > "$output_file"
fi

# Function to process a file
process_file() {
    local file="$1"
    local filename=$(basename "$file")

    # If the filename is already in the output file, skip it
    if grep -q "$filename" "$output_file"; then
        return
    fi

    # Gather basic information
    local malware_name=$(basename "$(dirname "$file")")
    local source=$(basename "$(dirname "$(dirname "$file")")")
    local category="Original dataset"
    local first_bytes=$(python3 "$python_script_directory/x86_disassembler.py" "$file")
    local num_sections=$(pescan "$file" | grep 'section count:' | cut -d':' -f2 | awk '{print $1}')
    local compiler=$(pestr "$file" | grep "COMPILER=" | awk -F'=' '{print $2}')
    
    if [ "$malware_name" == "webapp_uploads" ]; then
        source=$malware_name
        malware_name="Not defined"
        category="User uploaded"
    fi
    
    # If compiler is empty, set it to "Unknown"
    if [ -z "$compiler" ]; then
        compiler="Unknown"
    fi
    
    echo -e "$filename\t$malware_name\t$source\t$category\t$first_bytes\t$num_sections\t$compiler" >> "$temp_file"
}

export -f process_file
export output_file
export temp_file
export python_script_directory

# Usar find y xargs to process files in parallel
find "$root_directory" -type f -print0 | xargs -0 -P $(nproc --all) -I {} bash -c 'process_file "{}"'

# Merge temp file with output file
if [ -f "$temp_file" ]; then
    cat "$temp_file" >> "$output_file"
    rm "$temp_file"
fi