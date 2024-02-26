import Levenshtein
import pandas as pd

data_set = pd.read_csv('../../results_analysis/example.tsv', sep='\t')

def compare_strings(string1, string2):
    return Levenshtein.distance(string1, string2)

result_list = []

for i in range(len(data_set)):
    for j in range(i + 1, len(data_set)):
        result_list.append({
            'filename1': data_set.iloc[i]['filename'],
            'filename2': data_set.iloc[j]['filename'],
            'distance': compare_strings(data_set.iloc[i]['first_bytes'], data_set.iloc[j]['first_bytes'])
        })

result_df = pd.DataFrame(result_list)
result_df.to_csv('../../results_analysis/compare.tsv', sep='\t', index=False)
