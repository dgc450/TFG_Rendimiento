import subprocess
import os
import sys

# Comprobar si se pasó el array de ejecutables como argumento
if len(sys.argv) < 2:
    print("Por favor, proporciona un array de ejecutables.")
    sys.exit(1)


# Definir el directorio de trabajo de la aplicación
# TODO : Cambiar estos path en Triton
app_working_dir_hotspot = "/home/gimenezd/TFG_nuevo/gpu-rodinia-master/openmp/hotspot"
app_working_dir_bfs = "/home/gimenezd/TFG_nuevo/gpu-rodinia-master/openmp/bfs"
app_working_dir_lavaMD = "/home/gimenezd/TFG_nuevo/gpu-rodinia-master/openmp/lavaMD"
app_working_dir_cfd = "/home/gimenezd/TFG_nuevo/gpu-rodinia-master/openmp/cfd"
app_working_dir_backprop = "/home/gimenezd/TFG_nuevo/gpu-rodinia-master/openmp/backprop"
app_working_dir_gemm = "/home/gimenezd/TFG_nuevo/PolyBench-ACC-master/OpenMP/linear-algebra/kernels/gemm"
app_working_dir_convolution3d = "/home/gimenezd/TFG_nuevo/PolyBench-ACC-master/OpenMP/stencils/convolution-3d"
app_working_dir_jacobi2d = "/home/gimenezd/TFG_nuevo/PolyBench-ACC-master/OpenMP/stencils/jacobi-2d-imper"
app_working_dir_spmv = "/home/gimenezd/TFG_nuevo/heterogeneous-spmv-main/spmv-csr"
# Se pueden cambiar el numero de threads y tambien las aplicaciones a ejecutar
threads = [1,2,4,8,16,24,32]
applications = sys.argv[1:-1]

# El directorio donde se van a guardar los resultados
mainDirectory = sys.argv[-1]


# Ejecutable de Vtune
# TODO
vtune_path = "/opt/ohpc/pub/utils/vtune/2025.0.0/vtune/2025.0/bin64/vtune"



for application in applications:
	# Setup de las aplicaciones
	if application.startswith("hotspot"):
		executable_path = f"{app_working_dir_hotspot}/{application}"
		result_dir_hotspot = os.path.join(mainDirectory, f"Resultados_{application}")
		app_params = ["1024", "1024", "90000"]
		data_paths = ["../../data/hotspot/temp_1024", "../../data/hotspot/power_1024", "output.out"]
		
	elif application.startswith("bfs"):
		executable_path = f"{app_working_dir_bfs}/{application}"
		result_dir_bfs = os.path.join(mainDirectory, f"Resultados_{application}")
	
	elif application.startswith("lavaMD"):
		executable_path = f"{app_working_dir_lavaMD}/{application}"
		result_dir_lavaMD = os.path.join(mainDirectory, f"Resultados_{application}")
		app_params1 = ["-cores"]
		app_params2 = ["-boxes1d","60"]
		
	elif application.startswith("euler3d"):
		executable_path = f"{app_working_dir_cfd}/{application}"
		result_dir_cfd = os.path.join(mainDirectory, f"Resultados_{application}")
		data_paths = ["../../data/cfd/fvcorr.domn.193K"]
		
	elif application.startswith("backprop"):
		executable_path = f"{app_working_dir_backprop}/{application}"
		result_dir_backprop = os.path.join(mainDirectory, f"Resultados_{application}")
		app_params1 = ["200000000"]
	
	elif application.startswith("gemm"):
		executable_path = f"{app_working_dir_gemm}/{application}"
		result_dir_gemm = os.path.join(mainDirectory, f"Resultados_{application}")
	
	elif application.startswith("convolution-3d"):
		executable_path = f"{app_working_dir_convolution3d}/{application}"
		result_dir_convolution3d = os.path.join(mainDirectory, f"Resultados_{application}")
	
	elif application.startswith("jacobi-2d"):
		executable_path = f"{app_working_dir_jacobi2d}/{application}"
		result_dir_jacobi2d = os.path.join(mainDirectory, f"Resultados_{application}")
	
	elif application.startswith("spmv"):
		executable_path = f"{app_working_dir_spmv}/{application}"
		result_dir_spmv = os.path.join(mainDirectory, f"Resultados_{application}")
		app_params = ["50000"]
		data_paths = ["../matrices/matriz_grande.csr"]	

	# Ejecucion de los benchmarks con Vtune
	for num_threads in threads:
	    print(f"Comienza bucle de {application} con {num_threads} threads")
	    # Construir el comando a ejecutar
	    if application.startswith("hotspot"):
	    	result_dir_threads = f"{result_dir_hotspot}/Resultados_{num_threads}_threads"
	    	command = [
    			vtune_path,
    			"-collect", "memory-access",
    			"-knob", "analyze-openmp=true",
    			"-result-dir", result_dir_threads,
    			"--app-working-dir", app_working_dir_hotspot,
    			"--", executable_path,
	    	] + app_params + [str(num_threads)] + data_paths
	    
	    elif application.startswith("bfs"):
	    	result_dir_threads = f"{result_dir_bfs}/Resultados_{num_threads}_threads"
	    	command = [
    			vtune_path,
    			"-collect", "memory-access",
    			"-knob", "analyze-openmp=true",
    			"-result-dir", result_dir_threads,
    			"--app-working-dir", app_working_dir_bfs,
    			"--", executable_path,
    			str(num_threads),
    			"../../data/bfs/graph16M.txt"
	    	]
	    
	    elif application.startswith("lavaMD"):
	    	result_dir_threads = f"{result_dir_lavaMD}/Resultados_{num_threads}_threads"
	    	command = [
    			vtune_path,
    			"-collect", "memory-access",
    			"-knob", "analyze-openmp=true",
    			"-result-dir", result_dir_threads,
    			"--app-working-dir", app_working_dir_hotspot,
    			"--", executable_path,
	    	] + app_params1 + [str(num_threads)] + app_params2
	    	
	    elif application.startswith("euler3d"):
	    	result_dir_threads = f"{result_dir_cfd}/Resultados_{num_threads}_threads"
	    	command = [
    			vtune_path,
    			"-collect", "memory-access",
    			"-knob", "analyze-openmp=true",
    			"-result-dir", result_dir_threads,
    			"--app-working-dir", app_working_dir_cfd,
    			"--", executable_path,
	    	] + data_paths + [str(num_threads)]
	    	
	    elif application.startswith("backprop"):
	    	result_dir_threads = f"{result_dir_backprop}/Resultados_{num_threads}_threads"
	    	command = [
    			vtune_path,
    			"-collect", "memory-access",
    			"-knob", "analyze-openmp=true",
    			"-result-dir", result_dir_threads,
    			"--app-working-dir", app_working_dir_backprop,
    			"--", executable_path,
	    	] + app_params1 + [str(num_threads)]
	    	
	    elif application.startswith("gemm"):
	    	result_dir_threads = f"{result_dir_gemm}/Resultados_{num_threads}_threads"
	    	command = [
    			vtune_path,
    			"-collect", "memory-access",
    			"-knob", "analyze-openmp=true",
    			"-result-dir", result_dir_threads,
    			"--app-working-dir", app_working_dir_gemm,
    			"--", executable_path,
	    	] + [str(num_threads)]
	    	
	    elif application.startswith("convolution-3d"):
	    	result_dir_threads = f"{result_dir_convolution3d}/Resultados_{num_threads}_threads"
	    	command = [
    			vtune_path,
    			"-collect", "memory-access",
    			"-knob", "analyze-openmp=true",
    			"-result-dir", result_dir_threads,
    			"--app-working-dir", app_working_dir_convolution3d,
    			"--", executable_path,
	    	] + [str(num_threads)]
	    	
	    elif application.startswith("jacobi-2d"):
	    	result_dir_threads = f"{result_dir_jacobi2d}/Resultados_{num_threads}_threads"
	    	command = [
    			vtune_path,
    			"-collect", "memory-access",
    			"-knob", "analyze-openmp=true",
    			"-result-dir", result_dir_threads,
    			"--app-working-dir", app_working_dir_jacobi2d,
    			"--", executable_path,
	    	] + [str(num_threads)]
	    	
	    elif application.startswith("spmv"):
	    	result_dir_threads = f"{result_dir_spmv}/Resultados_{num_threads}_threads"
	    	command = [
    			vtune_path,
    			"-collect", "memory-access",
    			"-knob", "analyze-openmp=true",
    			"-result-dir", result_dir_threads,
    			"--app-working-dir", app_working_dir_spmv,
    			"--", executable_path,
	    	] + data_paths + app_params + [str(num_threads)]

	    # Ejecutar el comando
	    result = subprocess.run(command, capture_output=True, text=True)
	    
	    # Imprimir la salida y errores (si los hay)
	    print(f"Running with {num_threads} threads")
	    print("Output:")
	    print(result.stdout)
	    if result.stderr:
	    	print("Errors:")
	    	print(result.stderr)
	    print("\n")
