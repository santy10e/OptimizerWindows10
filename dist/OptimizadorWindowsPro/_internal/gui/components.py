import tkinter as tk
from tkinter import ttk

class MarcoDesplazable(ttk.Frame):
    def __init__(self, contenedor, *args, **kwargs):
        super().__init__(contenedor, *args, **kwargs)
        self.contenedor = contenedor
        
        # Acceder a los colores a través de la ventana principal
        self.colores = contenedor.winfo_toplevel().COLORES
        
        self.canvas = tk.Canvas(self, bg=self.colores['fondo_oscuro'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        
        self.marco_desplazable = ttk.Frame(self.canvas)
        self.marco_desplazable.bind(
            "<Configure>", 
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.marco_desplazable, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.canvas.bind_all("<MouseWheel>", self._desplazar_con_rueda)
    
    def _desplazar_con_rueda(self, evento):
        self.canvas.yview_scroll(int(-1*(evento.delta/120)), "units")