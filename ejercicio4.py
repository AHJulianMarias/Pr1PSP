import subprocess
import threading
import time
import win32clipboard

datosPrevios = ""
datosPosteriores = ""
parar = False


# Funcion que descarga el archivo del servidor FTP
def descargarReadme():
    global datosPrevios
    p1 = subprocess.Popen(
        "ftp",
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    # He cambiado el ftp, le he pedido una lista de publicos a chatgpt y he usado este
    comandos = [
        b"verbose\n",
        b"open ftp.freebsd.org\n",
        b"anonymous\n",
        b"a@a.c\n",
        b"ls\n",
        b"get /pub/FreeBSD/README.TXT\n",
    ]  # Descarga el archivo 'readme.txt' desde el servidor.

    # Iteramos sobre cada comando en la lista y lo enviamos al proceso FTP.
    for cmd in comandos:
        p1.stdin.write(cmd)  # Escribimos el comando en la entrada estándar del proceso.
    # 5 segundos para ver si conseguimos respuesta
    respuesta = p1.communicate(timeout=5)
    # respuesta[1] es stdErr, si tiene contenido es por que ha habido un error asi que devolvemos False
    if respuesta[1] != b"":
        print("Error al descargar el archivo")
        return False
    return True


# cierras y vuelves a ver lo que hay actualmente


def pasarAPortapapeles():

    # Abrimos archivo
    with open("readme.txt", "r") as txtFile:
        contenidoTxt = txtFile.read()
    global datosPosteriores
    global datosPrevios
    # abres clipboard, consigues ver lo que tienes actualmente en el portapapeles
    win32clipboard.OpenClipboard()
    datosPrevios = win32clipboard.GetClipboardData()
    # vacias portapapeles
    win32clipboard.EmptyClipboard()
    # llenas portapapeles
    win32clipboard.SetClipboardText(contenidoTxt)
    win32clipboard.CloseClipboard()
    win32clipboard.OpenClipboard()
    datosPosteriores = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()


def checkPortapapeles():
    global parar
    global datosPrevios
    global datosPosteriores
    # si es son los mismos datos que al inicios es porque no se ha realizado bien el cambio
    # se va a iterar mientras parar sea False, solamente es True cuando sales del menú del main
    while not parar:
        if datosPrevios != datosPosteriores:
            print("Se realizaron cambios en el portapapeles")
            datosPrevios = datosPosteriores
        time.sleep(2)


def main():
    global parar
    descargado1vez = False
    eleccion = 0
    # Para salir pulsas el 2
    while eleccion != "3":
        # fmt:off
        eleccion = input("""Elige:
1.Descargar archivo del servidor FTP.
2.Copiar fichero descargado del servidor FTP al portapapeles.                            
3.Salir.\n""")
        if eleccion == "1":
            #Si no has descargado no podras utilizar la opción 2
            descargado1vez = descargarReadme()
        elif eleccion == "2":
            if descargado1vez:
                pasarAPortapapeles()
            else:
                print("Tienes que usar la opcion 1 por lo menos una vez antes de usar esta opción.")
    print("Terminando programa")
    parar = True
    return


if __name__ == "__main__":
    # desde el inicio se ejecuta el checker
    t = threading.Thread(target=checkPortapapeles)
    t.start()
    main()
    # una vez se cierre el main, se deberia parar el hilo, asi que esperamos a que termine
    t.join()
