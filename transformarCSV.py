import subprocess
import os
import sys

# Comprobar si se pasó el array de ejecutables como argumento
if len(sys.argv) < 2:
    print("Por favor, proporciona un array de ejecutables.")
    sys.exit(1)

# Se pueden cambiar el numero de threads y tambien las aplicaciones a ejecutar
threads = [1,2,4,8,16,24,32]
applications = sys.argv[1:-1]

# El directorio donde se van a guardar los resultados
mainDirectory = sys.argv[-1]

# Ejecutable de Vtune
# TODO
vtune_path = "/opt/ohpc/pub/utils/vtune/2025.0.0/vtune/2025.0/bin64/vtune"

csv_dir_hotspot = os.path.join(mainDirectory, "CSV_hotspot")
os.makedirs(csv_dir_hotspot, exist_ok=True)
csv_dir_bfs = os.path.join(mainDirectory, "CSV_bfs")
os.makedirs(csv_dir_bfs, exist_ok=True)
csv_dir_lavaMD = os.path.join(mainDirectory, "CSV_lavaMD")
os.makedirs(csv_dir_lavaMD, exist_ok=True)
csv_dir_cfd = os.path.join(mainDirectory, "CSV_cfd")
os.makedirs(csv_dir_cfd, exist_ok=True)
csv_dir_backprop = os.path.join(mainDirectory, "CSV_backprop")
os.makedirs(csv_dir_backprop, exist_ok=True)
csv_dir_gemm = os.path.join(mainDirectory, "CSV_gemm")
os.makedirs(csv_dir_gemm, exist_ok=True)
csv_dir_convolution3d = os.path.join(mainDirectory, "CSV_convolution-3d")
os.makedirs(csv_dir_convolution3d, exist_ok=True)
csv_dir_jacobi2d = os.path.join(mainDirectory, "CSV_jacobi-2d")
os.makedirs(csv_dir_jacobi2d, exist_ok=True)
csv_dir_spmv = os.path.join(mainDirectory, "CSV_spmv")
os.makedirs(csv_dir_spmv, exist_ok=True)

for application in applications:
	result_dir = f"{mainDirectory}/Resultados_{application}"
	
	for num_threads in threads:
	    result_dir_threads = f"{result_dir}/Resultados_{num_threads}_threads"
	    csv_file = f"{application}_{num_threads}_threads.csv"
	    if application.startswith("hotspot"):
	    	csv_path = os.path.join(csv_dir_hotspot, csv_file)
	    elif application.startswith("bfs"):
	    	csv_path = os.path.join(csv_dir_bfs, csv_file)
	    elif application.startswith("lavaMD"):
	    	csv_path = os.path.join(csv_dir_lavaMD, csv_file)
	    elif application.startswith("euler3d"):
	    	csv_path = os.path.join(csv_dir_cfd, csv_file)
	    elif application.startswith("backprop"):
	    	csv_path = os.path.join(csv_dir_backprop, csv_file)
	    elif application.startswith("gemm"):
	    	csv_path = os.path.join(csv_dir_gemm, csv_file)
	    elif application.startswith("convolution-3d"):
	    	csv_path = os.path.join(csv_dir_convolution3d, csv_file)
	    elif application.startswith("jacobi-2d"):
	    	csv_path = os.path.join(csv_dir_jacobi2d, csv_file)
	    elif application.startswith("spmv"):
	    	csv_path = os.path.join(csv_dir_spmv, csv_file)

	    # Construir el comando a ejecutar
	    command = [
    		vtune_path,
    		"-report", "summary",
    		"-r", result_dir_threads,
    		"-format", "csv",
    		"-report-output", csv_path,
	    ]
	    
	    # Ejecutar el comando
	    result = subprocess.run(command, capture_output=True, text=True)
	    
	    # Imprimir la salida y errores (si los hay)
	    print(f"Generando CSV para {application} con {num_threads} threads")
	    print("Output:")
	    print(result.stdout)
	    if result.stderr:
	    	print("Errors:")
	    	print(result.stderr)
	    print("\n")
