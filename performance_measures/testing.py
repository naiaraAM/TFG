import subprocess
import time
import os
import matplotlib.pyplot as plt

current_dir = os.path.dirname(os.path.realpath(__file__))

def run_scripts_parallel():
    process_malware_path = os.path.abspath(os.path.join(current_dir, '..', '..', 'TFG', 'scripts', 'bash', 'process_basic_info.sh'))
    subprocess.run([process_malware_path], shell=True)
    compare_malware_path = os.path.abspath(os.path.join(current_dir, '..', '..', 'TFG', 'scripts', 'python', 'compare.py'))
    subprocess.run(['python3', compare_malware_path])
    creation_path = os.path.abspath(os.path.join(current_dir, '..', '..', 'TFG', 'db', 'creation.py'))
    subprocess.run(['python3', creation_path])
    insertion_path = os.path.abspath(os.path.join(current_dir, '..', '..', 'TFG', 'db', 'insertion.py'))
    subprocess.run(['python3', insertion_path])
    comparison_path = os.path.abspath(os.path.join(current_dir, '..', '..', 'TFG', 'db', 'comparison.py'))
    subprocess.run(['python3', comparison_path])

def run_scripts_non_parallel():
    process_malware_path = os.path.abspath(os.path.join(current_dir, '..', '..', 'TFG', 'scripts', 'bash', 'process_basic_info_non_parallel.sh'))
    subprocess.run([process_malware_path], shell=True)
    compare_malware_path = os.path.abspath(os.path.join(current_dir, '..', '..', 'TFG', 'scripts', 'python', 'compare_non_parallel.py'))
    subprocess.run(['python3', compare_malware_path])
    creation_path = os.path.abspath(os.path.join(current_dir, '..', '..', 'TFG', 'db', 'creation.py'))
    subprocess.run(['python3', creation_path])
    insertion_path = os.path.abspath(os.path.join(current_dir, '..', '..', 'TFG', 'db', 'insertion.py'))
    subprocess.run(['python3', insertion_path])
    comparison_path = os.path.abspath(os.path.join(current_dir, '..', '..', 'TFG', 'db', 'comparison.py'))
    subprocess.run(['python3', comparison_path])

def eliminar_ficheros():
    compare_path = os.path.abspath(os.path.join(current_dir, '..', '..', 'TFG', 'results_analysis', 'compare.tsv'))
    info_path = os.path.abspath(os.path.join(current_dir, '..', '..', 'TFG', 'results_analysis', 'sample_basic_info.tsv'))
    db_path = os.path.abspath(os.path.join(current_dir, '..', '..', 'TFG', 'db', 'TFG.db'))
    try:
        os.remove(compare_path)
        os.remove(info_path)
        os.remove(db_path)
    except FileNotFoundError:
        pass

def parallel_time():
    tiempos = []

    for i in range(10):
        print("Iter num: " + str(i) + " parallel")
        eliminar_ficheros()
        try:
            inicio = time.time()  # Iniciar cronómetro
            run_scripts_parallel()
            fin = time.time()  # Detener cronómetro
            tiempos.append(fin - inicio)  # Calcular tiempo de ejecución y almacenar
        except subprocess.CalledProcessError as e:
            print(f"Error ejecutando el script: {e}")
            tiempos.append(None)  # Registrar None en caso de error

    tiempos_validos = [t for t in tiempos if t is not None]
    if tiempos_validos:
        tiempo_medio = sum(tiempos_validos) / len(tiempos_validos)  # Calcular el tiempo promedio
    else:
        tiempo_medio = None

    return tiempo_medio

def non_parallel_time():
    tiempos = []

    for i in range(10):
        print("Iter num: " + str(i) + " non parallel")
        eliminar_ficheros()
        try:
            inicio = time.time()  # Iniciar cronómetro
            run_scripts_non_parallel()
            fin = time.time()  # Detener cronómetro
            tiempos.append(fin - inicio)  # Calcular tiempo de ejecución y almacenar
        except subprocess.CalledProcessError as e:
            print(f"Error ejecutando el script: {e}")
            tiempos.append(None)  # Registrar None en caso de error

    tiempos_validos = [t for t in tiempos if t is not None]
    if tiempos_validos:
        tiempo_medio = sum(tiempos_validos) / len(tiempos_validos)  # Calcular el tiempo promedio
    else:
        tiempo_medio = None

    return tiempo_medio

# Ejecutar el script y calcular tiempos
tiempo_medio_parallel = parallel_time()
tiempo_medio_non_parallel = non_parallel_time()

if tiempo_medio_parallel is not None and tiempo_medio_non_parallel is not None:
    print(f"Tiempo promedio de ejecución paralelo: {tiempo_medio_parallel} segundos")
    print(f"Tiempo promedio de ejecución no paralelo: {tiempo_medio_non_parallel} segundos")

    # Crear el gráfico de barras
    categorias = ['No Paralelo', 'Paralelo']
    valores = [tiempo_medio_non_parallel, tiempo_medio_parallel]

    plt.figure(figsize=(10, 5))
    plt.bar(categorias, valores, color=['blue', 'orange'])

    # Añadir títulos y etiquetas
    plt.title('Comparación de Tiempos de Ejecución')
    plt.xlabel('Método de Ejecución')
    plt.ylabel('Tiempo Medio (segundos)')

    # Mostrar los valores encima de las barras
    for i, valor in enumerate(valores):
        plt.text(i, valor + 1, f'{valor:.2f}', ha='center', va='bottom')
    plot_path = os.path.abspath(os.path.join(current_dir, '..', '..', 'TFG', 'results_analysis', 'execution_times.png'))
    plt.savefig(plot_path)
    plt.show()
    # Save the plot on this same directory
    
else:
    print("No se pudo calcular el tiempo promedio debido a errores en la ejecución del script.")
