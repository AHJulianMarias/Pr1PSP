import os  # Importamos el módulo os para poder usar funciones del sistema operativo, como pipe y fork.
import sys  # Importamos sys para manejar la salida estándar.
import json

# Ejecutar en https://www.online-python.com/


def main():
    # Creamos un par de descriptores de archivo utilizando os.pipe().
    # fd[0] se usará para leer, y fd[1] se usará para escribir.
    fd = os.pipe()

    # Creamos un nuevo proceso con fork().
    # pid = os.fork()
    pid = os.fork()
    # Verificamos en qué proceso estamos (padre o hijo) según el valor de pid.
    if pid < 0:
        # Si el valor de pid es menor que 0, significa que hubo un error al crear el proceso.
        print("No se ha podido crear el proceso hijo...")
        sys.exit(1)  # Salimos del programa con un código de error.

    elif pid == 0:

        buffer = os.read(fd[0], 80).decode("utf-8")
        os.close(fd[0])
        filas = 0
        palabras = 0
        # nos llega una cadena con cada fila separada por \n, con lo cual revisamos cada "fila" haciendo un split por \n
        for row in buffer.split("\n"):
            # cada iteracion añade una fila
            filas += 1
            # cada row le hacemos un split segun los espacios en blanco y sumamos su longitud a palabras
            palabras += len(row.split())

        # HECHO CON JSON
        diccionarioHijo = {"filas": filas, "palabras": palabras}
        mensajeHijo = json.dumps(diccionarioHijo)

        os.write(fd[1], mensajeHijo.encode("utf-8"))  # Enviamos el texto
        # Imprimimos el mensaje recibido.
        print(f"El hijo recibe algo del pipe:\n{buffer}")
        # Imprimimos lo que hemos enviado
        print(f"El hijo envia {buffer.upper()} al padre")
        # Cerramos el descriptor de lectura y escritura
        os.close(fd[1])

    else:
        # PADRE

        # fmt:off
        # SI FUESE CON ARCHIVO
        # fileList = []
        # with open("textfile.txt", "r") as txtRead:
        #     for row in txtRead:
        #         fileList.append(row)
        # # Creamos el mensaje que el padre enviará al hijo.
        # mensajePadre = "".join(fileList)
        #Mandamos el texto entero
        mensajePadre = """a
b
c
d
almendra
coliflor
girasol rojo"""



        os.write(fd[1], mensajePadre.encode("utf-8")) 
        print("El padre envía un mensaje al hijo...")

        # Cerramos el descriptor de escritura.
        os.close(fd[1])

        # Esperamos a que el proceso hijo termine.
        os.wait()
        buffer = os.read(fd[0], 80).decode("utf-8")

        #SI LO QUE LLEGA FUESE EL JSON
        jsonLlega = json.loads(buffer)
        numFilas = jsonLlega["filas"]
        numPalabras = jsonLlega["palabras"]

        os.close(fd[0])
        print(f"Al padre le llega un mensaje del hijo:\nNumero de filas:{numFilas}\nNumero de palabras:{numPalabras} ")


# Ejecutamos la función principal.
if __name__ == "__main__":
    main()
