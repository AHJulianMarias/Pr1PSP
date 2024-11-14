import psutil


for proc in psutil.process_iter(["name", "pid", "memory_percent"]):
    print(f"NAME: {proc.info["name"]} \t PID: {proc.info["pid"]}")


nombreBorrar = input("Introduce el nombre del proceso que deseas borrar\n")

procKilled = False
for proc in psutil.process_iter(["name", "pid", "memory_percent"]):
    if nombreBorrar == proc.info["name"]:
        try:
            proc.kill()
            procKilled = True
        except psutil.AccessDenied:
            print("No tienes permisos parar cerrar este proceso")
        except psutil.NoSuchProcess:
            print("El proceso ya no existe")
        except psutil.Error as e:
            print(f"Error desconocido {e}")

if procKilled:
    print(f"El proceso {nombreBorrar} se ha cerrado correctamente.")
else:
    print(f"El proceso {nombreBorrar} no existe.")
