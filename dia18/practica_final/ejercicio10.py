import os
import tkinter as tk


def abrir_calculadora():
    os.system("calc.exe")


ventana = tk.Tk()
ventana.title("Abrir calculadora")
ventana.geometry("300x140")

etiqueta = tk.Label(
    ventana,
    text="Presiona el botón para abrir la calculadora",
)
etiqueta.pack(pady=(20, 10))

boton = tk.Button(
    ventana,
    text="Abrir calculadora",
    command=abrir_calculadora,
)
boton.pack()

ventana.mainloop()
