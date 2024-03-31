import pandas as pd
import textdistance as td

data_set = pd.read_csv('../../results_analysis/first_bytes_extracted.tsv', sep='\t')

def levenshtein(string1, string2):
    if pd.notnull(string1) and pd.notnull(string2):  # Verificar si ambos valores no son NaN
        return td.levenshtein.normalized_similarity(string1, string2)
    else:
        return -1
def jaccard(string1, string2):
    if pd.notnull(string1) and pd.notnull(string2):  # Verificar si ambos valores no son NaN
        return td.jaccard.normalized_similarity(string1, string2)
    else:
        return -1
def jarowinkler(string1, string2):
    if pd.notnull(string1) and pd.notnull(string2):  # Verificar si ambos valores no son NaN
        return td.jaro_winkler.normalized_similarity(string1, string2)
    else:
        return -1

result_list = []

for i in range(len(data_set)):
    for j in range(i + 1, len(data_set)):
        result_list.append({
            'filename1': data_set.iloc[i]['filename'],
            'filename2': data_set.iloc[j]['filename'],
            'levenshtein': levenshtein(data_set.iloc[i]['first_bytes'], data_set.iloc[j]['first_bytes']),
            'jaccard': jaccard(data_set.iloc[i]['first_bytes'], data_set.iloc[j]['first_bytes']),
            'jarowinkler': jarowinkler(data_set.iloc[i]['first_bytes'], data_set.iloc[j]['first_bytes'])
        })

result_df = pd.DataFrame(result_list)
result_df.to_csv('../../results_analysis/compare.tsv', sep='\t', index=False)
