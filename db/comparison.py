import sqlite3
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
RELATIVE_DATA_PATH = '../../TFG/results_analysis/compare.tsv'
DATA_PATH = os.path.abspath(os.path.join(script_dir, RELATIVE_DATA_PATH))
DB_FILENAME = 'TFG.db'

# Create the full path to the database file
DB_PATH = os.path.join(script_dir, DB_FILENAME)

# Use database
try:
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    with open(DATA_PATH) as f:
        next(f) # Skip the header
        for line in f:
            filename1, filename2, levenshtein, jaccard, jarowinkler = line.strip().split('\t')
            try:
                cursor.execute("INSERT INTO comparison (filename1, filename2, levenshtein, jaccard, jarowinkler) VALUES (?, ?, ?, ?, ?)", (filename1, filename2, levenshtein, jaccard, jarowinkler))
            except sqlite3.IntegrityError:
                print(f"{filename1} and {filename2} already exists in the database")
    connection.commit()

except sqlite3.Error as e:
    print(f"SQLite error: {e}")

finally:
    connection.close()