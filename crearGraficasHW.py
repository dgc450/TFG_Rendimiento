import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import itertools

# Comprobar argumentos
if len(sys.argv) < 2:
    print("Uso: python crearGraficas_hw.py <apps...> <mainDirectory>")
    sys.exit(1)

applications = sys.argv[1:-1]
mainDirectory = sys.argv[-1]
threads = [1, 2, 4, 8, 16, 24, 32]

# Diccionarios para tasas de fallo
l1_miss_rate = {app: [] for app in applications}
l2_miss_rate = {app: [] for app in applications}
llc_miss_rate = {app: [] for app in applications}
cpi = {app: [] for app in applications}

# Rutas base por aplicación
csv_dirs = {
    "hotspot": f"/home/gimenezd/TFG_nuevo/{mainDirectory}/CSV_hotspotHW",
    "bfs": f"/home/gimenezd/TFG_nuevo/{mainDirectory}/CSV_bfsHW",
    "lavaMD": f"/home/gimenezd/TFG_nuevo/{mainDirectory}/CSV_lavaMDHW",
    "euler3d": f"/home/gimenezd/TFG_nuevo/{mainDirectory}/CSV_cfdHW",
    "backprop": f"/home/gimenezd/TFG_nuevo/{mainDirectory}/CSV_backpropHW",
    "gemm": f"/home/gimenezd/TFG_nuevo/{mainDirectory}/CSV_gemmHW",
    "convolution-3d": f"/home/gimenezd/TFG_nuevo/{mainDirectory}/CSV_convolution-3dHW",
    "jacobi-2d": f"/home/gimenezd/TFG_nuevo/{mainDirectory}/CSV_jacobi-2dHW",
    "spmv": f"/home/gimenezd/TFG_nuevo/{mainDirectory}/CSV_spmvHW"
}

# Procesar CSVs
for application in applications:
    app_prefix = next((prefix for prefix in csv_dirs if application.startswith(prefix)), None)
    if not app_prefix:
        print(f"❌ No se reconoce el directorio CSV para {application}")
        continue
    csv_subdir = csv_dirs[app_prefix]

    for num_threads in threads:
        csv_file = f"{application}_{num_threads}_threads.csv"
        csv_path = os.path.join(csv_subdir, csv_file)

        if not os.path.isfile(csv_path):
            print(f"⚠️ CSV no encontrado: {csv_path}")
            l1_miss_rate[application].append(None)
            l2_miss_rate[application].append(None)
            llc_miss_rate[application].append(None)
            cpi[application].append(None)
            continue

        try:
            df = pd.read_csv(csv_path, sep='\t', on_bad_lines='skip')
            df.columns = df.columns.str.strip()

            # Extraer contadores reales
            retired_inst = df['Hardware Event Count:INST_RETIRED.ANY'].astype(float).sum()
            clk_unhalted = df['Hardware Event Count:CPU_CLK_UNHALTED.THREAD'].astype(float).sum()
            l1_hit = df['Hardware Event Count:MEM_LOAD_RETIRED.L1_HIT'].astype(float).sum()
            l1_miss = df['Hardware Event Count:MEM_LOAD_RETIRED.L1_MISS'].astype(float).sum()
            l2_hit = df['Hardware Event Count:MEM_LOAD_RETIRED.L2_HIT'].astype(float).sum()
            #l2_miss = float(row['Hardware Event Count:MEM_LOAD_RETIRED.L2_MISS'])
            llc_hit = df['Hardware Event Count:MEM_LOAD_RETIRED.L3_HIT'].astype(float).sum()
            llc_miss = df['Hardware Event Count:MEM_LOAD_RETIRED.L3_MISS'].astype(float).sum()

            # Calcular tasas
            l1_total = l1_hit + l1_miss
            llc_total = llc_hit + llc_miss
            l2_total = l2_hit + llc_total

            l1_miss_rate[application].append(l1_miss / l1_total if l1_total else None)
            l2_miss_rate[application].append(llc_total / l2_total if l2_total else None)
            llc_miss_rate[application].append(llc_miss / llc_total if llc_total else None)
            cpi[application].append(clk_unhalted / retired_inst)


        except Exception as e:
            print(f"❌ Error al procesar {csv_file}: {e}")
            l1_miss_rate[application].append(None)
            l2_miss_rate[application].append(None)
            llc_miss_rate[application].append(None)
            cpi[application].append(None)

# Crear carpeta de salida
output_dir = f"/home/gimenezd/TFG_nuevo/{mainDirectory}/graficasHW_{applications[0]}"
os.makedirs(output_dir, exist_ok=True)

# Función para gráficas de línea
def generar_grafica_lineas(y_values, y_label, title, filename):

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
	for app in applications:
		valores = [v if v is not None else 0 for v in y_values[app]]
		color = color_fijo[app]
		plt.plot(threads, valores, marker='o', label=app, color=color)
	plt.title(title)
	plt.xlabel('Número de Hilos')
	plt.ylabel(y_label)
	plt.xticks(threads)
	plt.grid(True)
	plt.legend()
	plt.savefig(os.path.join(output_dir, filename))
	plt.close()

# Crear gráficas
generar_grafica_lineas(l1_miss_rate, 'L1 Miss Rate', 'Comparativa de la tasa de fallos L1', 'l1_miss_rate.png')
generar_grafica_lineas(l2_miss_rate, 'L2 Miss Rate', 'Comparativa de la tasa de fallos L2', 'l2_miss_rate.png')
generar_grafica_lineas(llc_miss_rate, 'LLC Miss Rate', 'Comparativa de la tasa de fallos LLC', 'llc_miss_rate.png')
generar_grafica_lineas(cpi, 'CPI', 'Comparativa de los ciclos por instruccion', "cpi.png")

print(f"✅ Gráficas guardadas en: {output_dir}")


