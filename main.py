"""Entrada da aplicação, inclusive para o executável Windows."""
import tkinter as tk
from tkinter import messagebox

from interface import TaskManagerApp
from service import TaskService
from storage import Storage, StorageError


def main():
    try:
        service = TaskService(Storage())
    except StorageError as erro:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("TaskManager — erro ao iniciar", str(erro), parent=root)
        root.destroy()
        return
    app = TaskManagerApp(service)
    app.mainloop()


if __name__ == "__main__":
    main()
