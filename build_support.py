"""Coleta bibliotecas Tcl/Tk inclusive nas instalações Python com zipfs."""
from pathlib import Path
import tkinter as tk


def bibliotecas_tk():
    root = tk.Tk()
    root.withdraw()
    dados = []
    try:
        for origem, destino in ((root.tk.eval("info library"), "_tcl_data"),
                                (root.tk.eval("set tk_library"), "_tk_data")):
            if not origem.startswith("//zipfs:"):
                continue  # O hook padrão atende instalações com arquivos físicos.
            pasta = Path(__file__).resolve().parent / "build" / "tk-libraries" / destino
            copiar_virtual(root.tk, origem, pasta)
            dados.append((str(pasta), destino))
    finally:
        root.destroy()
    return dados


def copiar_virtual(interpreter, origem, destino):
    destino.mkdir(parents=True, exist_ok=True)
    entradas = interpreter.call("glob", "-nocomplain", "-directory", origem, "*")
    for entrada in entradas:
        caminho = str(entrada)
        alvo = destino / str(interpreter.call("file", "tail", caminho))
        if interpreter.call("file", "isdirectory", caminho):
            copiar_virtual(interpreter, caminho, alvo)
        else:
            canal = interpreter.call("open", caminho, "rb")
            try:
                alvo.write_bytes(interpreter.call("read", canal))
            finally:
                interpreter.call("close", canal)
