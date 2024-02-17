import sqlite3
import os

DATA_PATH = '../results_analysis/example.tsv'
DB_FILENAME = 'samples.db'

# Get the current working directory
current_directory = os.getcwd()

# Create the full path to the database file
DB_PATH = os.path.join(current_directory, DB_FILENAME)

# use database
try:
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    with open(DATA_PATH) as f:
        for line in f:
            sha_256, type, source, first_bytes = line.strip().split('\t')
            try:
                cursor.execute("INSERT INTO samples VALUES (?, ?, ?, ?)", (sha_256, type, source, first_bytes))
            except sqlite3.IntegrityError:
                print(f"El sha_256 {sha_256} ya existe en la base de datos")

    # Commit the changes
    connection.commit()

except sqlite3.Error as e:
    print(f"SQLite error: {e}")

finally:
    # Close the connection
    connection.close()