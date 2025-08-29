import tkinter as tk
import tkinter.ttk as ttk

def configurar_estilos(root):
    COLORES = {
        'fondo_oscuro': "#1e1e1e",
        'fondo_claro': "#2d2d2d",
        'acento': "#4ec9b0",
        'acento_oscuro': "#3da89c",
        'texto': "#ffffff",
        'error': "#ff6b6b",
        'exito': "#6bff6b",
        'advertencia': "#ffcc66",
        'fondo_tarjeta': "#252526"
    }

    FUENTES = {
        'titulo': ("Segoe UI", 18, "bold"),
        'subtitulo': ("Segoe UI", 14),
        'app': ("Segoe UI", 11, "bold"),
        'estado': ("Segoe UI", 10),
        'boton': ("Segoe UI", 10, "bold"),
        'tooltip': ("Segoe UI", 9)
    }
    
    estilo = ttk.Style(root)
    estilo.theme_use('clam')
    
    # Estilos base
    estilo.configure('.', background=COLORES['fondo_oscuro'], foreground=COLORES['texto'])
    estilo.configure('TFrame', background=COLORES['fondo_oscuro'])
    estilo.configure('TLabel', background=COLORES['fondo_oscuro'], foreground=COLORES['texto'])
    estilo.configure('TNotebook', background=COLORES['fondo_oscuro'])
    estilo.configure('TNotebook.Tab', 
                    background=COLORES['fondo_claro'], 
                    foreground=COLORES['texto'],
                    font=FUENTES['boton'], 
                    padding=[10, 5])
    
    # Estilos personalizados
    estilo.configure('Card.TFrame', background=COLORES['fondo_tarjeta'], relief='flat', borderwidth=0)
    estilo.configure('Card.TLabel', background=COLORES['fondo_tarjeta'], foreground=COLORES['texto'], font=FUENTES['app'])
    estilo.configure('StatusOn.TLabel', background=COLORES['fondo_tarjeta'], foreground=COLORES['exito'], font=FUENTES['estado'])
    estilo.configure('StatusOff.TLabel', background=COLORES['fondo_tarjeta'], foreground=COLORES['error'], font=FUENTES['estado'])
    
    # Estilos de botones
    estilo.configure('Accent.TButton', 
                    background=COLORES['acento'],
                    foreground=COLORES['fondo_oscuro'],
                    font=FUENTES['boton'],
                    borderwidth=0)
    estilo.configure('Danger.TButton', 
                    background=COLORES['error'],
                    foreground=COLORES['texto'],
                    font=FUENTES['boton'],
                    borderwidth=0)
    estilo.configure('Warning.TButton', 
                    background=COLORES['advertencia'],
                    foreground=COLORES['fondo_oscuro'],
                    font=FUENTES['boton'],
                    borderwidth=0)
    
    # Estados de botones
    estilo.map('Accent.TButton',
               background=[('active', COLORES['acento_oscuro']), ('disabled', '#1a4d45')],
               relief=[('pressed', 'sunken'), ('!pressed', 'flat')])
    estilo.map('Danger.TButton',
               background=[('active', '#cc5555'), ('disabled', '#553333')],
               relief=[('pressed', 'sunken'), ('!pressed', 'flat')])
    estilo.map('Warning.TButton',
               background=[('active', '#e6b800'), ('disabled', '#665c00')],
               relief=[('pressed', 'sunken'), ('!pressed', 'flat')])
    
    return COLORES, FUENTES