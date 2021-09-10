from tkinter import filedialog, Tk
from tkinter.filedialog import askopenfilename
from tkinter import * 


class Gestor:
    def __init__(self):
        print("entra a gestor")

    def CargarArchivo(self): 
        Tk().withdraw()
        archivo = filedialog.askopenfile(initialdir="./Archivos Prueba", title="Seleccione un archivo",filetypes=(("Archivos pxla",".pxla"),("ALL files",".txt")))
        if archivo is None:
            print('No se selecciono ni un archivo\n')
            return None
        else:
           
            texto = archivo.read()
            print(texto)
            archivo.close()
            print("Lectura Exitosa")