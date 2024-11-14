# fmt:off
from os import system
import subprocess 
import asyncio
import time


def showNotepad1():
    try:
        # fmt:off
        #tiempo antes de iniciarse
        tiempoInicio = time.time()
        subprocess.run(["Notepad.exe",])
        #tiempo tras iniciarse, al ser sincrona, solo va a llegar a aqui una vez se cierre el proceso del notepad
        tiempoFinal = time.time()

        print(f"Tiempo para ejecutarse {tiempoFinal - tiempoInicio}")
    except subprocess.CalledProcessError as e:

        print(e.output)


async def showNotepad2():
    try:
        tiempoInicio = time.time()
        await asyncio.create_subprocess_exec("notepad.exe")
        #tiempo tras iniciarse, al ser asincrona, va a llegar aqui en cuanto se inicie el proceso del notepad
        tiempoFinal = time.time()
        print(f"Tiempo para ejecutarse {tiempoFinal - tiempoInicio}")
    except subprocess.CalledProcessError as e:

        print(e.output)


#Main con menú para elegir asincrona o sincrona
async def main():
    eleccion = 0
    #Para salir pulsas el 3
    while eleccion != 3:
        eleccion = int(input("""Elige que llamada quieres que sea
1.Síncrona
2.Asíncrona
3.Salir\n"""))
        if eleccion == 1:
            showNotepad1()
        elif eleccion == 2:
            await showNotepad2()
            #presione una tecla para continuar...
            system("Pause")
    print("Terminando programa")
    return


if __name__ == "__main__":
    asyncio.run(main())
