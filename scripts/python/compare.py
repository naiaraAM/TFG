#!/usr/bin/env python3

import pandas as pd
import textdistance as td
import os
from itertools import combinations

script_dir = os.path.dirname(os.path.abspath(__file__))
RELATIVE_DATA_PATH = '../../results_analysis/sample_basic_info.tsv'
DATA_PATH = os.path.abspath(os.path.join(script_dir, RELATIVE_DATA_PATH))

# Create the directory to save the results
SAVE_DIR = os.path.join(script_dir, '../../results_analysis')
os.makedirs(SAVE_DIR, exist_ok=True)

SAVE_DATA_PATH = os.path.join(SAVE_DIR, 'compare.tsv')

# Read the CSV file
data_set = pd.read_csv(DATA_PATH, sep='\t')

def compute_similarity(string1, string2):
    """
    Compute the similarity between two strings using different metrics.

    Args:
        string1 (str): The first string.
        string2 (str): The second string.

    Returns:
        dict: A dictionary containing the similarity scores for different metrics.
            The keys are 'levenshtein', 'jaccard', and 'jarowinkler'.
            The values are the normalized similarity scores between 0 and 1.
            If either string1 or string2 is NaN (null), all similarity scores will be -1.
    """
    if pd.isnull(string1) or pd.isnull(string2):
        return {'levenshtein': -1, 'jaccard': -1, 'jarowinkler': -1}
    return {
        'levenshtein': td.levenshtein.normalized_similarity(string1, string2),
        'jaccard': td.jaccard.normalized_similarity(string1, string2),
        'jarowinkler': td.jaro_winkler.normalized_similarity(string1, string2)
    }

# Load existing data
existing_pairs = set()
if os.path.exists(SAVE_DATA_PATH):
    existing_df = pd.read_csv(SAVE_DATA_PATH, sep='\t', usecols=['filename1', 'filename2'])
    existing_pairs.update(
        (row['filename1'], row['filename2']) for idx, row in existing_df.iterrows()
    )

# Create filenames pairs
filename_pairs = list(combinations(data_set['filename'], 2))

# Remove pairs that are already processed
filename_pairs = [pair for pair in filename_pairs if pair not in existing_pairs and (pair[1], pair[0]) not in existing_pairs]

#  Calculate similarity for each pair
result_list = []
for filename1, filename2 in filename_pairs:
    sim_data = compute_similarity(
        data_set[data_set['filename'] == filename1]['first_bytes'].values[0],
        data_set[data_set['filename'] == filename2]['first_bytes'].values[0]
    )
    result_list.append({
        'filename1': filename1,
        'filename2': filename2,
        **sim_data
    })

# Write results to output file
if result_list:
    result_df = pd.DataFrame(result_list)
    result_df.to_csv(SAVE_DATA_PATH, sep='\t', mode='a', header=True, index=False)
