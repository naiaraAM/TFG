import sqlite3
import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the relative path to the TSV file from the script directory
RELATIVE_DATA_PATH = '../../TFG/results_analysis/first_bytes_extracted.tsv'

# Construct the absolute path to the TSV file
DATA_PATH = os.path.abspath(os.path.join(script_dir, RELATIVE_DATA_PATH))

# Define the name of the SQLite database file
DB_FILENAME = 'TFG.db'

# Create the full path to the database file using the script's directory
DB_PATH = os.path.join(script_dir, DB_FILENAME)

try:
    # Connect to the SQLite database
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    # Open the TSV file and insert data into the database
    with open(DATA_PATH) as f:
        next(f)  # Skip the header
        for line in f:
            if not line.strip():
                continue
            sha_256, malware_name, source, category, first_bytes = line.strip().split('\t')
            try:
                cursor.execute("INSERT INTO samples VALUES (?, ?, ?, ?, ?)",
                               (sha_256, malware_name, source, category, first_bytes))
            except sqlite3.IntegrityError:
                print(f"Sha_256 {sha_256} already exists in the database")

    # Commit changes to the database
    connection.commit()

except sqlite3.Error as e:
    print(f"SQLite error: {e}")

finally:
    # Close the database connection
    connection.close()
