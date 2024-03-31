import sqlite3
import os

DATA_PATH = '../results_analysis/first_bytes_extracted.tsv'
DB_FILENAME = 'TFG.db'

# Get the current working directory
current_directory = os.getcwd()

# Create the full path to the database file
DB_PATH = os.path.join(current_directory, DB_FILENAME)

# Check if the database file exists, create it if not
if not os.path.exists(DB_PATH):
    open(DB_PATH, 'w').close()

try:
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    # Create table if not exists
    cursor.execute('''CREATE TABLE IF NOT EXISTS samples 
                (sha_256 text PRIMARY KEY, 
                malware_name text, 
                source text,
                first_bytes text)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS comparison
                    (filename1 text, 
                    filename2 text, 
                    levenshtein float,
                    jaccard float,
                    jarowinkler float,
                    primary key (filename1, filename2))''')
    connection.commit()
except sqlite3.Error as e:
    print(f"SQLite error: {e}")
finally:
    # Close the connection
    connection.close()