# estilo.py

try:
    import ttkbootstrap as ttk
    from ttkbootstrap.constants import *
    BOOTSTRAP_ATIVO = True
except ImportError:
    import tkinter.ttk as ttk
    from tkinter import *
    BOOTSTRAP_ATIVO = False

def aplicar_estilo(root):
    if BOOTSTRAP_ATIVO:
        root.style = ttk.Style("flatly")  # ou: darkly, cyborg, journal, etc.
        root.title("SwiftDL")
        root.geometry("600x400")
    else:
        root.title("SwiftDL")
        root.geometry("600x400")

def criar_botao(master, texto, comando, estilo="success"):
    if BOOTSTRAP_ATIVO:
        return ttk.Button(master, text=texto, command=comando, bootstyle=estilo)
    else:
        return ttk.Button(master, text=texto, command=comando)
