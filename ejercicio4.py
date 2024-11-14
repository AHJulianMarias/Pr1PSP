import subprocess
import win32clipboard

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


with open("readme.txt", "r") as txtFile:
    contenidoTxt = txtFile.read()


# abres clipboard, consigues ver lo que tienes actualmente en el portapapeles
win32clipboard.OpenClipboard()
datosPrevios = win32clipboard.GetClipboardData()
# vacias portapapeles
win32clipboard.EmptyClipboard()
# llenas portapapeles
win32clipboard.SetClipboardText(contenidoTxt)
win32clipboard.CloseClipboard()
# cierras y vuelves a ver lo que hay actualmente
win32clipboard.OpenClipboard()
datosPosteriores = win32clipboard.GetClipboardData()
win32clipboard.CloseClipboard()
# si es son los mismos datos que al inicios es porque no se ha realizado bien el cambio
if datosPrevios == datosPosteriores:
    print("No se ha realizado ningun cambio en el portapapeles")
else:
    print("Se realizaron cambios en el portapapeles")
