import sys
from pathlib import Path
from tkinter import ttk

# Agregar directorio raíz al path para resolver importaciones
sys.path.insert(0, str(Path(__file__).parent))

from gui.app import OptimizadorWindowsPro

if __name__ == "__main__":
    try:
        app = OptimizadorWindowsPro()
        app.mainloop()
    except Exception as e:
        import tkinter.messagebox as messagebox
        messagebox.showerror("Error Crítico", f"No se pudo iniciar la aplicación:\n\n{str(e)}")