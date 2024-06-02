#!/usr/bin/env python3

import pandas as pd
import textdistance as td
import os
from itertools import combinations
from multiprocessing import Pool, cpu_count

script_dir = os.path.dirname(os.path.abspath(__file__))
RELATIVE_DATA_PATH = '../../results_analysis/sample_basic_info.tsv'
DATA_PATH = os.path.abspath(os.path.join(script_dir, RELATIVE_DATA_PATH))

# Create the directory to save the results
SAVE_DIR = os.path.join(script_dir, '../../results_analysis')
os.makedirs(SAVE_DIR, exist_ok=True)

SAVE_DATA_PATH = os.path.join(SAVE_DIR, 'compare.tsv')

# Read the CSV file
data_set = pd.read_csv(DATA_PATH, sep='\t')

def compute_similarity(pair):
    """
    Compute the similarity between two files based on their first bytes.

    Parameters:
    pair (tuple): A tuple containing the filenames of the two files to compare.

    Returns:
    dict: A dictionary containing the computed similarity measures between the two files.
          The dictionary has the following keys:
          - 'filename1': The filename of the first file.
          - 'filename2': The filename of the second file.
          - 'levenshtein': The normalized Levenshtein similarity between the first bytes of the two files.
          - 'jaccard': The normalized Jaccard similarity between the first bytes of the two files.
          - 'jarowinkler': The normalized Jaro-Winkler similarity between the first bytes of the two files.
          - 'arithmetic_mean': The arithmetic mean of the Levenshtein, Jaccard, and Jaro-Winkler similarities.
          - 'geometric_mean': The geometric mean of the Levenshtein, Jaccard, and Jaro-Winkler similarities.
    """
    filename1, filename2 = pair
    string1 = data_set[data_set['filename'] == filename1]['first_bytes'].values[0]
    string2 = data_set[data_set['filename'] == filename2]['first_bytes'].values[0]

    if pd.isnull(string1) or pd.isnull(string2):
        return {'filename1': filename1, 'filename2': filename2, 'levenshtein': -1, 'jaccard': -1, 'jarowinkler': -1, 'arithmetic_mean': -1, 'geometric_mean': -1}
    levenshtein = td.levenshtein.normalized_similarity(string1, string2)
    jaccard = td.jaccard.normalized_similarity(string1, string2)
    jarowinkler = td.jaro_winkler.normalized_similarity(string1, string2)
    arithmetic_mean = (levenshtein + jaccard + jarowinkler) / 3
    geometric_mean = (levenshtein * jaccard * jarowinkler) ** (1/3)


    return {
        'filename1': filename1,
        'filename2': filename2,
        'levenshtein': levenshtein,
        'jaccard': jaccard,
        'jarowinkler': jarowinkler,
        'arithmetic_mean': arithmetic_mean,
        'geometric_mean': geometric_mean,
    }

# Load existing data
existing_pairs = set()
if os.path.exists(SAVE_DATA_PATH):
    existing_df = pd.read_csv(SAVE_DATA_PATH, sep='\t', usecols=['filename1', 'filename2'])
    existing_pairs.update((row['filename1'], row['filename2']) for _, row in existing_df.iterrows())

# Create filenames pairs
filename_pairs = list(combinations(data_set['filename'], 2))

# Remove pairs that are already processed
filename_pairs = [pair for pair in filename_pairs if pair not in existing_pairs and (pair[1], pair[0]) not in existing_pairs]

# Paralelize the computation
with Pool(cpu_count()) as pool:
    result_list = pool.map(compute_similarity, filename_pairs)

# Write results to output file
if result_list:
    result_df = pd.DataFrame(result_list)
    result_df.to_csv(SAVE_DATA_PATH, sep='\t', mode='a', header=not os.path.exists(SAVE_DATA_PATH), index=False)
