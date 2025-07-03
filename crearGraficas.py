import subprocess
import os
import pandas as pd
import matplotlib.pyplot as plt
import itertools
import sys

# Comprobar si se pasó el array de ejecutables como argumento
if len(sys.argv) < 2:
    print("Por favor, proporciona un array de ejecutables.")
    sys.exit(1)

applications = sys.argv[1:-1]
# El directorio donde se van a guardar los resultados
mainDirectory = sys.argv[-1]

# Definir el directorio donde se encuentran los csv
# TODO : Cambiar estos path en Triton
csv_files_dir_hotspot = f"/home/gimenezd/TFG_nuevo/{mainDirectory}/CSV_hotspot"
csv_files_dir_bfs = f"/home/gimenezd/TFG_nuevo/{mainDirectory}/CSV_bfs"
csv_files_dir_lavaMD = f"/home/gimenezd/TFG_nuevo/{mainDirectory}/CSV_lavaMD"
csv_files_dir_cfd = f"/home/gimenezd/TFG_nuevo/{mainDirectory}/CSV_cfd"
csv_files_dir_backprop = f"/home/gimenezd/TFG_nuevo/{mainDirectory}/CSV_backprop"
csv_files_dir_gemm = f"/home/gimenezd/TFG_nuevo/{mainDirectory}/CSV_gemm"
csv_files_dir_convolution3d = f"/home/gimenezd/TFG_nuevo/{mainDirectory}/CSV_convolution-3d"
csv_files_dir_jacobi2d = f"/home/gimenezd/TFG_nuevo/{mainDirectory}/CSV_jacobi-2d"
csv_files_dir_spmv = f"/home/gimenezd/TFG_nuevo/{mainDirectory}/CSV_spmv"
# Aplicaciones e hilos
threads = [1,2,4,8,16,24,32]

# Diccionarios con las métricas
elapsed_times = {app: [] for app in applications}
L1_bounds = {app: [] for app in applications}
L2_bounds = {app: [] for app in applications}
L3_bounds = {app: [] for app in applications}
DRAM_bounds = {app: [] for app in applications}
llc_misses = {app: [] for app in applications}
memory_bandwidth = {app: [] for app in applications}

# Leer los CSV y extraer el Elapsed Time
for application in applications:
    for num_threads in threads:
        if application.startswith("hotspot"):
            csv_file = f"{application}_{num_threads}_threads.csv"
            csv_path = os.path.join(csv_files_dir_hotspot, csv_file)
        elif application.startswith("bfs"):
            csv_file = f"{application}_{num_threads}_threads.csv"
            csv_path = os.path.join(csv_files_dir_bfs, csv_file)
        elif application.startswith("lavaMD"):
            csv_file = f"{application}_{num_threads}_threads.csv"
            csv_path = os.path.join(csv_files_dir_lavaMD, csv_file)
        elif application.startswith("euler3d"):
            csv_file = f"{application}_{num_threads}_threads.csv"
            csv_path = os.path.join(csv_files_dir_cfd, csv_file)
        elif application.startswith("backprop"):
            csv_file = f"{application}_{num_threads}_threads.csv"
            csv_path = os.path.join(csv_files_dir_backprop, csv_file)
        elif application.startswith("gemm"):
            csv_file = f"{application}_{num_threads}_threads.csv"
            csv_path = os.path.join(csv_files_dir_gemm, csv_file)
        elif application.startswith("convolution-3d"):
            csv_file = f"{application}_{num_threads}_threads.csv"
            csv_path = os.path.join(csv_files_dir_convolution3d, csv_file)
        elif application.startswith("jacobi-2d"):
            csv_file = f"{application}_{num_threads}_threads.csv"
            csv_path = os.path.join(csv_files_dir_jacobi2d, csv_file)
        elif application.startswith("spmv"):
            csv_file = f"{application}_{num_threads}_threads.csv"
            csv_path = os.path.join(csv_files_dir_spmv, csv_file)
        
        # Leer el CSV usando pandas y gestionar errores
        try:
            df = pd.read_csv(csv_path, on_bad_lines='skip', sep='\t')  # Ignorar las líneas malas y separa con tabuladores si se necesita
                  
            # Extraer los valores que buscamos dentro de los CSV
            elapsed_time = df.loc[df['Metric Name'] == 'Elapsed Time', 'Metric Value'].values[0]
            elapsed_times[application].append(float(elapsed_time))  # Guardar el valor

            L1_bound = df.loc[df['Metric Name'] == 'L1 Bound', 'Metric Value'].values[0]
            L1_bounds[application].append(float(L1_bound))  # Guardar el valor

            L2_bound = df.loc[df['Metric Name'] == 'L2 Bound', 'Metric Value'].values[0]
            L2_bounds[application].append(float(L2_bound))  # Guardar el valor

            L3_bound = df.loc[df['Metric Name'] == 'L3 Bound', 'Metric Value'].values[0]
            L3_bounds[application].append(float(L3_bound))  # Guardar el valor

            DRAM_bound = df.loc[df['Metric Name'] == 'DRAM Bound', 'Metric Value'].values[0]
            DRAM_bounds[application].append(float(DRAM_bound))  # Guardar el valor
            
            memory_bw = df.loc[df['Metric Name'] == 'DRAM Bound', 'Metric Value'].values[0]
            memory_bandwidth[application].append(float(memory_bw))
            
            llc_miss = df.loc[df['Metric Name'] == 'LLC Miss Count', 'Metric Value'].values[0]
            llc_misses[application].append(float(llc_miss))
            
        except Exception as e:
            print(f"Error al procesar {csv_file}: {e}")

# Verificar si se recogieron valores válidos
for app in applications:
    for metric, metric_data in [('Elapsed Time', elapsed_times), ('LLC Misses', llc_misses), ('Memory Bandwidth', memory_bandwidth)]:
        if len(metric_data[app]) != len(threads):
            print(f"Advertencia: {app} no tiene suficientes datos de {metric} para todos los threads.")

# Crear la carpeta para almacenar las gráficas
app_name = applications[0]
output_dir = f"/home/gimenezd/TFG_nuevo/{mainDirectory}/graficas_{app_name}"
os.makedirs(output_dir, exist_ok=True)  # Crear el directorio si no existe

# Función para generar y guardar una gráfica
def generar_grafica(y_values, y_label, title, filename):
	colores_default = itertools.cycle(['blue', 'red', 'purple', 'cyan', 'brown', 'magenta'])

	color_fijo = {}
	for app in applications:
		if app.endswith('GCC'):
            		color_fijo[app] = 'green'
		elif app.endswith('AVX'):
			color_fijo[app] = 'orange'
		else:
			color_fijo[app] = next(colores_default)

	plt.figure(figsize=(10, 6))
	for application in applications:
		if len(y_values[application]) == len(threads):
			color = color_fijo[application]
			plt.plot(threads, y_values[application], marker='o', label=application, color=color)
		else:
			print(f"No hay suficientes datos para graficar {application}.")
	plt.title(title)
	plt.xlabel('Número de Hilos')
	plt.ylabel(y_label)
	plt.xticks(threads)  # Asegurarse de que los valores del eje x correspondan al número de hilos
	plt.legend(title='Aplicación')
	plt.grid(True)
	plt.savefig(os.path.join(output_dir, filename))
	plt.close()

# Generar y guardar las cuatro gráficas
generar_grafica(elapsed_times, 'Elapsed Time (s)', 'Comparativa de Elapsed Time', 'comparativa_elapsed_time.png')
generar_grafica(llc_misses, 'LLC Misses', 'Comparativa de LLC Misses', 'comparativa_llc_misses.png')
generar_grafica(memory_bandwidth, 'Memory Bandwidth (GB/s)', 'Comparativa de Memory Bandwidth', 'comparativa_memory_bandwidth.png')
generar_grafica(L1_bounds, 'L1 Bound (%)', 'Comparativa de bloqueo de L1', 'l1_bound.png')
generar_grafica(L2_bounds, 'L2 Bound (%)', 'Comparativa de bloqueo de L2', 'l2_bound.png')
generar_grafica(L3_bounds, 'L3 Bound (%)', 'Comparativa de bloqueo de L3', 'l3_bound.png')
generar_grafica(DRAM_bounds, 'DRAM Bound (%)', 'Comparativa de bloqueo de DRAM', 'dram_bound.png')


print(f"Gráficas guardadas en: {output_dir}")
