#!/usr/bin/python3

import sqlite3
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

RELATIVE_DATA_PATH = '../../TFG/results_analysis/sample_basic_info.tsv'

DATA_PATH = os.path.abspath(os.path.join(script_dir, RELATIVE_DATA_PATH))
DB_FILENAME = 'TFG.db'

# Create the full path to the database file
DB_PATH = os.path.join(script_dir, DB_FILENAME)

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
                category text,
                first_bytes text,
                num_sections integer,
                compiler text)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS comparison
                (id integer primary key autoincrement,
                filename1 text, 
                filename2 text, 
                levenshtein float,
                jaccard float,
                jarowinkler float,
                unique(filename1, filename2))''')
    connection.commit()
    
except sqlite3.Error as e:
    print(f"SQLite error: {e}")

finally:
    connection.close()