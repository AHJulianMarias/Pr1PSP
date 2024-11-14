import os  # Importamos el módulo os para poder usar funciones del sistema operativo, como pipe y fork.
import sys  # Importamos sys para manejar la salida estándar.

# Ejecutar en https://www.online-python.com/


def main():
    # Creamos un par de descriptores de archivo utilizando os.pipe().
    # fd[0] se usará para leer, y fd[1] se usará para escribir.
    fd = os.pipe()

    # Creamos el mensaje que el padre enviará al hijo.

    # Creamos un nuevo proceso con fork().
    pid = os.fork()

    # Verificamos en qué proceso estamos (padre o hijo) según el valor de pid.
    if pid < 0:
        # Si el valor de pid es menor que 0, significa que hubo un error al crear el proceso.
        print("No se ha podido crear el proceso hijo...")
        sys.exit(1)  # Salimos del programa con un código de error.

    elif pid == 0:
        buffer = os.read(fd[0], 80).decode("utf-8")
        os.write(fd[1], buffer.upper().encode("utf-8"))  # Enviamos el texto
        # Imprimimos el mensaje recibido.
        print(f"El hijo recibe algo del pipe: {buffer}")
        # Imprimimos lo que hemos enviado
        print(f"El hijo envia {buffer.upper()} al padre")
        # Cerramos el descriptor de lectura y escritura
        os.close(fd[0])
        os.close(fd[1])

    else:
        saludoPadre = "mensaje en minusculas"
        os.write(
            fd[1], saludoPadre.encode("utf-8")
        )  # escribimos el texto en minusculas
        print("El padre envía un mensaje al hijo...")

        # Cerramos el descriptor de escritura.
        os.close(fd[1])

        # Esperamos a que el proceso hijo termine.
        os.wait()
        buffer = os.read(fd[0], 80).decode("utf-8")
        os.close(fd[0])
        print(f"Al padre le llega {buffer} del hijo")


# Ejecutamos la función principal.
if __name__ == "__main__":
    main()
