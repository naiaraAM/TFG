import sqlite3
import os


DATA_PATH = '../results_analysis/first_bytes_extracted.tsv'
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
            # Separar los campos de la línea
            sha_256, malware_name, source, first_bytes = line.strip().split('\t')
            try:
                # Insertar los datos en la base de datos
                cursor.execute("INSERT INTO samples VALUES (?, ?, ?, ?)", (sha_256, malware_name, source, first_bytes))
            except sqlite3.IntegrityError:
                print(f"El sha_256 {sha_256} ya existe en la base de datos")

    # Confirmar los cambios
    connection.commit()

except sqlite3.Error as e:
    print(f"Error de SQLite: {e}")

finally:
    # Cerrar la conexión
    connection.close()