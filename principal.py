import subprocess
import os
import sys

if len(sys.argv) < 2 or sys.argv[2] != "--outputdir":
    print("Por favor, proporcione el nombre del benchmark y de un directorio.")
    print("Formato: benchmark --outputdir fecha")
    print("Ejemplo: backprop --outputdir 05-02")
    sys.exit(1)

benchmark = sys.argv[1]
mainDirectory = sys.argv[3]
os.makedirs(mainDirectory, exist_ok=True)

# Ruta a los tres scripts
script_transformar_csv = "/home/gimenezd/TFG_nuevo/transformarCSV.py"
script_ejecutar_benchmarks = "/home/gimenezd/TFG_nuevo/ejecutarBenchmarks.py"
script_crear_graficas = "/home/gimenezd/TFG_nuevo/crearGraficas.py"
script_transformar_csvHW = "/home/gimenezd/TFG_nuevo/transformarCSVHW.py"
script_crear_graficasHW = "/home/gimenezd/TFG_nuevo/crearGraficasHW.py"
script_ejecutar_benchmarksHW = "/home/gimenezd/TFG_nuevo/ejecutarBenchmarksHW.py"
# Arrays de benchmarks
benchmarks = {
	"hotspot" : ["hotspot1","hotspot4","hotspot8","hotspotGCC","hotspotAVX"],
	"lavaMD" : ["lavaMD","lavaMDGCC","lavaMDAVX"],
	"bfs" : ["bfs","bfsGCC","bfsAVX"],
	"cfd" : ["euler3d_cpu1","euler3d_cpu4","euler3d_cpu8","euler3d_cpuGCC","euler3d_cpuAVX"],
	"backprop" : ["backprop","backpropGCC","backpropAVX"],
	"gemm" : ["gemm_acc","gemmGCC","gemmAVX"],
	"convolution3d" : ["convolution-3d_acc","convolution-3dGCC","convolution-3dAVX"],
	"jacobi2d" : ["jacobi-2d-imper_acc","jacobi-2d-imperGCC","jacobi-2d-imperAVX"],
        "spmv" : ["spmv","spmvGCC","spmvAVX"],
}

if benchmark not in benchmarks:
	print(f"Nombre del benchmark no valido: {benchmark}")
	print("Benchmarks disponibles: ",", ".join(benchmarks.keys()))

seleccion = benchmarks[benchmark]

# Ejecutar el primer script (hotspotAuto.py)
print("Ejecutando 'ejecutarBenchmarks.py'...")
subprocess.run(["python3", script_ejecutar_benchmarks] + seleccion + [mainDirectory], check=True)

# Ejecutar el primer script (hotspotAuto.py)
#print("Ejecutando 'ejecutarBenchmarksHW.py'...")
#subprocess.run(["python3", script_ejecutar_benchmarksHW] + seleccion + [mainDirectory], check=True)

# Ejecutar el segundo script (transformarCSV.py)
print("Ejecutando 'transformarCSV.py'...")
subprocess.run(["python3", script_transformar_csv] + seleccion + [mainDirectory], check=True)

# Ejecutar el segundo script (transformarCSV.py)
print("Ejecutando 'transformarCSVHW.py'...")
subprocess.run(["python3", script_transformar_csvHW] + seleccion + [mainDirectory], check=True)

# Ejecutar el tercer script (crearGraficas.py)
print("Ejecutando 'crearGraficas.py'...")
subprocess.run(["python3", script_crear_graficas] + seleccion + [mainDirectory], check=True)

# Ejecutar el tercer script (crearGraficas.py)
print("Ejecutando 'crearGraficasHW.py'...")
subprocess.run(["python3", script_crear_graficasHW] + seleccion + [mainDirectory], check=True)


print("Todos los scripts se han ejecutado correctamente.")
