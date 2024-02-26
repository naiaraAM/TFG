import sqlite3
import os

DATA_PATH = '../results_analysis/compare.tsv'
DB_FILENAME = 'TFG.db'

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
            filename1, filename2, distance = line.strip().split('\t')
            try:
                cursor.execute("INSERT INTO comparison VALUES (?, ?, ?)", (filename1, filename2, distance))
            except sqlite3.IntegrityError:
                print(f"Ya se ha comparado la pareja {filename1} y {filename2}")

    # Commit the changes
    connection.commit()

except sqlite3.Error as e:
    print(f"SQLite error: {e}")

finally:
    # Close the connection
    connection.close()