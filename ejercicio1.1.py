import psutil


listaProcesos = []
procesosInput = ""
while procesosInput != "0":
    procesosInput = input(
        "Introduce el nombre del proceso, introduce 0 cuando quieras parar de introducir nombres procesos\n"
    )
    if procesosInput != "0":
        listaProcesos.append(procesosInput)

if len(listaProcesos) == 0:
    print("No has incluido ningun nombre en la lista")
    quit()


for proceso in listaProcesos:
    ejecucion = False
    for proc in psutil.process_iter(["name", "pid", "memory_percent"]):
        # para que fuese mas preciso se tendría que poner == pero el nombre del proceso en la lista tendria que ser identico
        try:
            if proceso.lower() in proc.info["name"].lower():
                print(
                    f"El proceso {proc.info["name"]} se está ejecutando con pid {proc.info["pid"]} y realizando un uso de memoria de {proc.info["memory_percent"]}"
                )
                ejecucion = True
        # Dificil de comprobar ya que no he tenido ninguna excepcion durante las pruebas
        except psutil.AccessDenied:
            print(f"Acceso denegado al proceso {proc.info["name"]}")
        except psutil.NoSuchProcess:
            print(f"El proceso {proceso} no existe")
        except psutil.Error as e:
            print(f"Error desconocido {e}")
    if not ejecucion:
        print(f"El proceso {proceso} no se esta ejecutando")
