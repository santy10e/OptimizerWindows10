import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
import webbrowser
import time
import winreg
import psutil
import subprocess  # Importación faltante
import re
from tkinter.colorchooser import askcolor

from gui.components import MarcoDesplazable
from gui.styles import configurar_estilos
from core import apps, services, optimizations, utils, task, others

class OptimizadorWindowsPro(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Optimizador Windows Pro")
        self.geometry("850x750")
        self.minsize(750, 650)
        try:
            self.iconbitmap("icon.ico")
        except:
            pass

        
        self.COLORES, self.FUENTES = configurar_estilos(self)
        self.configure(bg=self.COLORES['fondo_oscuro'])
        
        # Variables de estado
        self.cache_estado_apps = {}
        self.ultima_revision_completa = 0
        self.revisando_estado = False
        self.cancelar_solicitado = False
        self.cola_estado = Queue()
        self.tarjetas_apps = {}
        self.tarjetas_inicio = {}
        self.tarjetas_servicios = {}
        self.tarjetas_caracteristicas = {}
        
        # Configuración de idioma
        self.idioma_actual = "es"
        self.textos_ui = self._crear_textos_ui()
        
        self._crear_widgets()
        
        if not utils.es_administrador():
            utils.solicitar_administrador()
        
        self.after(100, self.actualizar_estados_apps)
        self.centrar_ventana()
        self.after(100, self.procesar_cola)

    def _crear_textos_ui(self):
        return {
            "es": {
                "titulo": "Optimizador Windows Pro",
                "subtitulo": "Optimiza tu PC para máximo rendimiento",
                "github": "GitHub",
                "donar": "☕ Donar",
                "aplicaciones": "🛠️ Aplicaciones",
                #"inicio": "🚀 Inicio",
                "servicios": "⚙️ Servicios",
                "herramientas": "🛠️ Herramientas",
                "barra_tareas": "📊 Barra de Tareas",
                "caracteristicas": "🔒 Caracteristicas",
                "estado_listo": "Listo",
                "actualizar_todo": "Actualizar Todo",
                "instalar": "Instalar",
                "desinstalar": "Desinstalar",
                "deshabilitar": "Deshabilitar",
                "comprobando": "Comprobando...",
                "instalado": "Instalado",
                "no_instalado": "No instalado",
                "habilitado": "Habilitado",
                "deshabilitado": "Deshabilitado",
                "ejecutandose": "Ejecutándose",
                "detenido": "Detenido",
                "en_pausa": "En pausa",
                "iniciando": "Iniciando",
                "deteniendose": "Deteniéndose",
                "continuando": "Continuando",
                "pausando": "Pausando",
                "procesando": "Procesando...",
                "confirmar": "Confirmar",
                "error": "Error",
                "exito": "Éxito",
                "advertencia": "Advertencia",
                "optimizacion_completa": "Optimización Completa",
                "resultado_comando": "Resultado del Comando",
                "error_critico": "Error Crítico",
                "aplicar": "Aplicar Cambios",
                
                "otros": "🎨 Otros",
                "apariencia": "Cambiar Apariencia",
                "aplicar_apariencia": "Aplicar",
                "reiniciar_explorer": "Reiniciar Explorer",
                "exito": "Éxito",
                "error": "Error",
                "desconocido":"Desconocido"
            },
            "en": {
                "titulo": "Windows Optimizer Pro",
                "subtitulo": "Optimize your PC for maximum performance",
                "github": "GitHub",
                "donar": "☕ Donate",
                "aplicaciones": "🛠️ Applications",
                #"inicio": "🚀 Startup",
                "servicios": "⚙️ Services",
                "herramientas": "🛠️ Tools",
                "barra_tareas": "📊 Taskbar",
                "caracteristicas": "🔒 Task", 
                
                "estado_listo": "Ready",
                "actualizar_todo": "Update All",
                "instalar": "Install",
                "desinstalar": "Uninstall",
                "deshabilitar": "Disable",
                "comprobando": "Checking...",
                "instalado": "Installed",
                "no_instalado": "Not installed",
                "habilitado": "Enabled",
                "deshabilitado": "Disabled",
                "ejecutandose": "Running",
                "detenido": "Stopped",
                "en_pausa": "Paused",
                "iniciando": "Starting",
                "deteniendose": "Stopping",
                "continuando": "Continuing",
                "pausando": "Pausing",
                "procesando": "Processing...",
                "confirmar": "Confirm",
                "error": "Error",
                "exito": "Success",
                "advertencia": "Warning",
                "optimizacion_completa": "Optimization Complete",
                "resultado_comando": "Command Result",
                "error_critico": "Critical Error",

                "otros": "🎨 Others",
                "apariencia": "Change others",
                "aplicar_apariencia": "Apply",
                "reiniciar_explorer": "Restart Explorer",
                "exito": "Success",
                "error": "Error",
                "desconocido": "Unknown"
                
            }
        }
    
    def _crear_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Encabezado
        self._crear_encabezado()
        
        # Notebook (pestañas)
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=1, column=0, sticky='nsew', padx=20, pady=(0,10))
        
        # Crear pestañas
        self._crear_pestana_apps()
        #self._crear_pestana_inicio()
        self._crear_pestana_servicios()
        self._crear_pestana_herramientas()
        self._crear_pestana_barra_tareas()
        self._crear_pestana_caracteristicas() 
        self._crear_pestana_otros()
        
        # Barra de estado
        self._crear_barra_estado()

    def _crear_encabezado(self):
        marco_encabezado = ttk.Frame(self)
        marco_encabezado.grid(row=0, column=0, sticky='ew', padx=20, pady=15)
        
        # Título
        marco_titulo = ttk.Frame(marco_encabezado)
        marco_titulo.pack(side='left', fill='y')
        
        self.label_titulo = ttk.Label(
            marco_titulo, 
            text=self.textos_ui[self.idioma_actual]["titulo"],
            font=self.FUENTES['titulo'])
        self.label_titulo.pack(side='top', anchor='w')
        
        self.label_subtitulo = ttk.Label(
            marco_titulo,
            text=self.textos_ui[self.idioma_actual]["subtitulo"],
            font=self.FUENTES['subtitulo'])
        self.label_subtitulo.pack(side='top', anchor='w', pady=(5, 0))
        
        # Marco para enlaces
        marco_enlaces = ttk.Frame(marco_encabezado)
        marco_enlaces.pack(side='right', fill='y')
        
        # Botón de cambio de idioma
        self.btn_idioma = ttk.Button(
            marco_enlaces,
            text="ES/EN",
            command=self._cambiar_idioma,
            style='Accent.TButton')
        self.btn_idioma.pack(side='left', padx=5)
        
        # Botón de GitHub
        self.btn_github = ttk.Button(
            marco_enlaces,
            text=self.textos_ui[self.idioma_actual]["github"],
            command=lambda: webbrowser.open("https://github.com/santy10e"),
            style='Accent.TButton')
        self.btn_github.pack(side='left', padx=5)
        
        # Botón de Donación
        self.btn_donar = ttk.Button(
            marco_enlaces,
            text=self.textos_ui[self.idioma_actual]["donar"],
            command=lambda: webbrowser.open("https://coff.ee/torniche"),
            style='Accent.TButton')
        self.btn_donar.pack(side='left', padx=5)

    def _cambiar_idioma(self):
        if self.idioma_actual == "es":
            self.idioma_actual = "en"
        else:
            self.idioma_actual = "es"
        
        textos = self.textos_ui[self.idioma_actual]
        
        # Actualizar textos
        self.label_titulo.config(text=textos["titulo"])
        self.label_subtitulo.config(text=textos["subtitulo"])
        self.btn_github.config(text=textos["github"])
        self.btn_donar.config(text=textos["donar"])
        self.notebook.tab(0, text=textos["aplicaciones"])
        #self.notebook.tab(1, text=textos["inicio"])
        self.notebook.tab(1, text=textos["servicios"])
        self.notebook.tab(2, text=textos["herramientas"])
        self.notebook.tab(3, text=textos["barra_tareas"])
        self.notebook.tab(4, text=textos["privacidad"])  
        self.notebook.tab(5, text=textos["Otros"])
        self.etiqueta_estado.config(text=textos["estado_listo"])
        self.btn_actualizar.config(text=textos["actualizar_todo"])
        
        # Actualizar textos en componentes
        self._actualizar_textos_componentes(textos)
    
    def _actualizar_textos_componentes(self, textos):
        # Actualizar aplicaciones
        for nombre_app, datos in self.tarjetas_apps.items():
            datos['btn_instalar'].config(text=textos["instalar"])
            datos['btn_desinstalar'].config(text=textos["desinstalar"])
            self._actualizar_estado_app_ui(nombre_app, datos['estado'].cget("text"), textos)
        
        # Actualizar servicios
        for nombre_servicio, datos in self.tarjetas_servicios.items():
            datos['btn_deshabilitar'].config(text=textos["deshabilitar"])
            self._actualizar_estado_servicio_ui(nombre_servicio, datos['estado'].cget("text"), textos)
        
        # Actualizar barra de tareas
        self._actualizar_textos_barra_tareas(textos)
        
        # Actualizar privacidad
        self._actualizar_textos_privacidad(textos)
        
        # Actualizar botones de apariencia
        for widget in self.winfo_children():
            if isinstance(widget, ttk.Notebook):
                for pestana in widget.winfo_children():
                    if textos["otros"] in widget.tab(pestana, "text"):
                        for tarjeta in pestana.winfo_children():
                            if isinstance(tarjeta, tk.Canvas):
                                for marco in tarjeta.winfo_children():
                                    if isinstance(marco, ttk.Frame):
                                        for hijo in marco.winfo_children():
                                            if isinstance(hijo, ttk.Frame):
                                                for btn in hijo.winfo_children():
                                                    if isinstance(btn, ttk.Button) and btn.cget("text") == self.textos_ui[self.idioma_actual]["aplicar_apariencia"]:
                                                        btn.config(text=textos["aplicar_apariencia"])
    
    def _actualizar_estado_app_ui(self, nombre_app, estado_actual, textos):
        if estado_actual in [self.textos_ui["es"]["instalado"], self.textos_ui["en"]["instalado"]]:
            nuevo_estado = textos["instalado"]
        elif estado_actual in [self.textos_ui["es"]["no_instalado"], self.textos_ui["en"]["no_instalado"]]:
            nuevo_estado = textos["no_instalado"]
        elif estado_actual in [self.textos_ui["es"]["comprobando"], self.textos_ui["en"]["comprobando"]]:
            nuevo_estado = textos["comprobando"]
        elif estado_actual in [self.textos_ui["es"]["procesando"], self.textos_ui["en"]["procesando"]]:
            nuevo_estado = textos["procesando"]
        else:
            nuevo_estado = estado_actual
        
        if nombre_app in self.tarjetas_apps:
            self.tarjetas_apps[nombre_app]['estado'].config(text=nuevo_estado)
    
    def _actualizar_estado_servicio_ui(self, nombre_servicio, estado_actual, textos):
        estados = {
            'ejecutandose': textos["ejecutandose"],
            'detenido': textos["detenido"],
            'en_pausa': textos["en_pausa"],
            'iniciando': textos["iniciando"],
            'deteniendose': textos["deteniendose"],
            'continuando': textos["continuando"],
            'pausando': textos["pausando"],
            'comprobando': textos["comprobando"]
        }
        
        nuevo_estado = estados.get(estado_actual.lower(), estado_actual)
        
        if nombre_servicio in self.tarjetas_servicios:
            self.tarjetas_servicios[nombre_servicio]['estado'].config(text=nuevo_estado)
    
    def _actualizar_textos_barra_tareas(self, textos):
        for nombre_opcion in optimizations.OPCIONES_BARRA_TAREAS:
            for widget in self.winfo_children():
                if isinstance(widget, ttk.Notebook):
                    for pestana in widget.winfo_children():
                        if textos["barra_tareas"] in widget.tab(pestana, "text"):
                            for tarjeta in pestana.winfo_children():
                                if isinstance(tarjeta, tk.Canvas):
                                    for marco in tarjeta.winfo_children():
                                        if isinstance(marco, ttk.Frame):
                                            for hijo in marco.winfo_children():
                                                if isinstance(hijo, ttk.Frame) and nombre_opcion in [lbl['text'] for lbl in hijo.winfo_children() if isinstance(lbl, ttk.Label)]:
                                                    for btn in hijo.winfo_children():
                                                        if isinstance(btn, ttk.Button):
                                                            if btn.cget("state") == 'disabled':
                                                                btn.config(text=textos["deshabilitado"])
                                                            else:
                                                                btn.config(text=textos["deshabilitar"])
    
    def _actualizar_textos_privacidad(self, textos):
        for nombre_opcion in task.OPCIONES_PRIVACIDAD:
            for widget in self.winfo_children():
                if isinstance(widget, ttk.Notebook):
                    for pestana in widget.winfo_children():
                        if textos["privacidad"] in widget.tab(pestana, "text"):
                            for tarjeta in pestana.winfo_children():
                                if isinstance(tarjeta, tk.Canvas):
                                    for marco in tarjeta.winfo_children():
                                        if isinstance(marco, ttk.Frame):
                                            for hijo in marco.winfo_children():
                                                if isinstance(hijo, ttk.Frame) and nombre_opcion in [lbl['text'] for lbl in hijo.winfo_children() if isinstance(lbl, ttk.Label)]:
                                                    for btn in hijo.winfo_children():
                                                        if isinstance(btn, ttk.Button):
                                                            if btn.cget("state") == 'disabled':
                                                                btn.config(text=textos["deshabilitado"])
                                                            else:
                                                                btn.config(text=textos["deshabilitar"])

    def _crear_pestana_apps(self):
        pestana = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(pestana, text=self.textos_ui[self.idioma_actual]["aplicaciones"])
        
        marco_desplazable = MarcoDesplazable(pestana)
        marco_desplazable.pack(fill='both', expand=True)
        
        for i, (nombre_app, app_id) in enumerate(apps.APPS.items()):
            self._crear_tarjeta_app(marco_desplazable.marco_desplazable, nombre_app, i)
    
    def _crear_tarjeta_app(self, padre, nombre_app, fila):
        tarjeta = ttk.Frame(padre, style='Card.TFrame', padding=15)
        tarjeta.grid(row=fila, column=0, sticky='ew', pady=5, padx=5)
        tarjeta.grid_columnconfigure(1, weight=1)
        
        # Nombre de la app
        etiqueta_nombre = ttk.Label(tarjeta, text=nombre_app, style='Card.TLabel')
        etiqueta_nombre.grid(row=0, column=0, sticky='w', padx=(0, 20))
        
        # Estado
        etiqueta_estado = ttk.Label(tarjeta, text=self.textos_ui[self.idioma_actual]["comprobando"], style='Card.TLabel')
        etiqueta_estado.grid(row=0, column=1, sticky='w')
        
        # Botones
        marco_botones = ttk.Frame(tarjeta, style='TFrame')
        marco_botones.grid(row=0, column=2, sticky='e')
        
        btn_instalar = ttk.Button(marco_botones, 
                               text=self.textos_ui[self.idioma_actual]["instalar"], 
                               command=lambda n=nombre_app: self._confirmar_accion(n, "install"),
                               style='Accent.TButton')
        btn_instalar.pack(side='left', padx=5)
        
        btn_desinstalar = ttk.Button(marco_botones, 
                                 text=self.textos_ui[self.idioma_actual]["desinstalar"], 
                                 command=lambda n=nombre_app: self._confirmar_accion(n, "uninstall"),
                                 style='Danger.TButton')
        btn_desinstalar.pack(side='left', padx=5)
        
        # Guardar referencia
        self.tarjetas_apps[nombre_app] = {
            'marco': tarjeta,
            'estado': etiqueta_estado,
            'btn_instalar': btn_instalar,
            'btn_desinstalar': btn_desinstalar
        }
    
    # def _crear_pestana_inicio(self):
    #     pestana = ttk.Frame(self.notebook, style='TFrame')
    #     self.notebook.add(pestana, text=self.textos_ui[self.idioma_actual]["inicio"])
        
    #     marco_desplazable = MarcoDesplazable(pestana)
    #     marco_desplazable.pack(fill='both', expand=True)
        
    #     # No se crean tarjetas ya que hemos eliminado todos los elementos del menú de inicio
    #     label_vacio = ttk.Label(marco_desplazable.marco_desplazable, 
    #                            text="No hay elementos configurados para iniciar con el sistema",
    #                            style='Card.TLabel')
    #     label_vacio.pack(pady=20)
    
    ###################################################################################################
    ####SERVICIOS###################################################################################################
    def _crear_pestana_servicios(self):
        pestana = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(pestana, text=self.textos_ui[self.idioma_actual]["servicios"])
        
        marco_desplazable = MarcoDesplazable(pestana)
        marco_desplazable.pack(fill='both', expand=True)
        
        for i, (nombre_servicio, desc_servicio) in enumerate(services.SERVICIOS_WIN10.items()):
            self._crear_tarjeta_servicio(marco_desplazable.marco_desplazable, nombre_servicio, desc_servicio, i)
    
    def _crear_tarjeta_servicio(self, padre, nombre_servicio, desc_servicio, fila):
        tarjeta = ttk.Frame(padre, style='Card.TFrame', padding=15)
        tarjeta.grid(row=fila, column=0, sticky='ew', pady=5, padx=5)
        tarjeta.grid_columnconfigure(1, weight=1)
        
        # Descripción del servicio
        etiqueta_desc = ttk.Label(tarjeta, text=desc_servicio['nombre'], style='Card.TLabel')
        etiqueta_desc.grid(row=0, column=0, sticky='w', padx=(0, 20))
        
        # Descripcion
        icono_info = ttk.Label(tarjeta, 
                             text=f"ℹ️",
                             style='Card.TLabel',
                             cursor='question_arrow')
        icono_info.grid(row=0, column=1, sticky='w')
        
        #tooltip
        self._crear_tooltip(icono_info, desc_servicio['descripcion'])
        
        # Estado
        etiqueta_estado = ttk.Label(tarjeta, text=self.textos_ui[self.idioma_actual]["comprobando"], style='Card.TLabel')
        etiqueta_estado.grid(row=0, column=2, sticky='w')
        
        # Botones
        marco_botones = ttk.Frame(tarjeta, style='TFrame')
        marco_botones.grid(row=0, column=3, sticky='e')
        
        btn_deshabilitar = ttk.Button(marco_botones, 
                               text=self.textos_ui[self.idioma_actual]["deshabilitar"], 
                               command=lambda n=nombre_servicio: self._deshabilitar_servicio(n),
                               style='Danger.TButton')
        btn_deshabilitar.pack(side='left', padx=5)
        
        # Guardar referencia
        self.tarjetas_servicios[nombre_servicio] = {
            'marco': tarjeta,
            'estado': etiqueta_estado,
            'btn_deshabilitar': btn_deshabilitar
        }
        
        # Comprobar estado inicial
        self._verificar_estado_servicio(nombre_servicio)
    
    def _verificar_estado_servicio(self, nombre_servicio):
        try:
            servicio = psutil.win_service_get(nombre_servicio)
            estado = servicio.status()
            self._actualizar_estado_servicio(nombre_servicio, estado)
        except Exception as e:
            print(f"Error comprobando servicio {nombre_servicio}: {str(e)}")
            self._actualizar_estado_servicio(nombre_servicio, "desconocido")
    
    def _actualizar_estado_servicio(self, nombre_servicio, estado):
        texto_estado = {
            'running': self.textos_ui[self.idioma_actual]["ejecutandose"],
            'stopped': self.textos_ui[self.idioma_actual]["detenido"],
            'paused': self.textos_ui[self.idioma_actual]["en_pausa"],
            'start_pending': self.textos_ui[self.idioma_actual]["iniciando"],
            'stop_pending': self.textos_ui[self.idioma_actual]["deteniendose"],
            'continue_pending': self.textos_ui[self.idioma_actual]["continuando"],
            'pause_pending': self.textos_ui[self.idioma_actual]["pausando"],
        }.get(estado.lower(), estado.capitalize())
        
        estilo = 'StatusOn.TLabel' if estado.lower() == 'running' else 'StatusOff.TLabel'
        
        if nombre_servicio in self.tarjetas_servicios:
            self.tarjetas_servicios[nombre_servicio]['estado'].config(text=texto_estado, style=estilo)
    
    def _deshabilitar_servicio(self, nombre_servicio):
        confirmar = messagebox.askyesno(
            self.textos_ui[self.idioma_actual]["confirmar"],
            f"¿Seguro que quieres deshabilitar el servicio {nombre_servicio}?\n\nEsto puede afectar alguna funcionalidad del sistema.",
            icon='warning'
        )
        if confirmar:
            try:
                # Detener el servicio
                subprocess.run(["sc", "stop", nombre_servicio], check=True, timeout=30)
                
                # Deshabilitar inicio automático
                subprocess.run(["sc", "config", nombre_servicio, "start=", "disabled"], check=True, timeout=30)
                
                self._actualizar_estado_servicio(nombre_servicio, "stopped")
                messagebox.showinfo(self.textos_ui[self.idioma_actual]["exito"], f"El servicio {nombre_servicio} ha sido deshabilitado")
            except subprocess.CalledProcessError as e:
                messagebox.showerror(self.textos_ui[self.idioma_actual]["error"], f"No se pudo deshabilitar el servicio {nombre_servicio}:\n\n{e.stderr}")
            except Exception as e:
                messagebox.showerror(self.textos_ui[self.idioma_actual]["error"], f"Error inesperado deshabilitando servicio:\n\n{str(e)}")
    
    ####################################################################################################
    #### BARRA DE TAREAS ####################################################################################################
    
    def _crear_pestana_barra_tareas(self):
        pestana = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(pestana, text=self.textos_ui[self.idioma_actual]["barra_tareas"])
        
        marco_desplazable = MarcoDesplazable(pestana)
        marco_desplazable.pack(fill='both', expand=True)
        
        for i, (nombre_opcion, datos_opcion) in enumerate(optimizations.OPCIONES_BARRA_TAREAS.items()):
            self._crear_tarjeta_opcion_barra(marco_desplazable.marco_desplazable, nombre_opcion, datos_opcion, i)
    
    def _crear_tarjeta_opcion_barra(self, padre, nombre_opcion, datos_opcion, fila):
        tarjeta = ttk.Frame(padre, style='Card.TFrame', padding=15)
        tarjeta.grid(row=fila, column=0, sticky='ew', pady=5, padx=5)
        tarjeta.grid_columnconfigure(1, weight=1)
        
        # Nombre de la opción
        etiqueta_nombre = ttk.Label(tarjeta, text=nombre_opcion, style='Card.TLabel')
        etiqueta_nombre.grid(row=0, column=0, sticky='w', padx=(0, 20))
        
        # Descripción (tooltip)
        etiqueta_desc = ttk.Label(tarjeta, 
                             text="ℹ️",
                             style='Card.TLabel',
                             cursor='question_arrow')
        etiqueta_desc.grid(row=0, column=1, sticky='w')
        
        # Tooltip
        self._crear_tooltip(etiqueta_desc, datos_opcion['descripcion'])
        
        # Botón deshabilitar
        btn_deshabilitar = ttk.Button(tarjeta, 
                               text=self.textos_ui[self.idioma_actual]["deshabilitar"], 
                               command=lambda n=nombre_opcion, d=datos_opcion: self._deshabilitar_opcion_barra(n, d),
                               style='Danger.TButton')
        btn_deshabilitar.grid(row=0, column=2, sticky='e')
        
        # Comprobar estado inicial
        self._verificar_estado_opcion_barra(nombre_opcion, datos_opcion, btn_deshabilitar)
    
    def _crear_tooltip(self, widget, texto):
        tooltip = tk.Toplevel(self)
        tooltip.withdraw()
        tooltip.overrideredirect(True)
        
        label = tk.Label(tooltip, 
                       text=texto,
                       bg="#ffffe0",
                       fg="black",
                       relief='solid',
                       borderwidth=1,
                       font=self.FUENTES['tooltip'],
                       wraplength=300,
                       justify='left')
        label.pack()
        
        def entrar(evento):
            x, y, _, _ = widget.bbox("insert")
            x += widget.winfo_rootx() + 25
            y += widget.winfo_rooty() + 25
            
            tooltip.geometry(f"+{x}+{y}")
            tooltip.deiconify()
        
        def salir(evento):
            tooltip.withdraw()
        
        widget.bind("<Enter>", entrar)
        widget.bind("<Leave>", salir)
    
    def _verificar_estado_opcion_barra(self, nombre_opcion, datos_opcion, btn_deshabilitar):
        try:
            # Verificar el estado principal
            clave = winreg.OpenKey(winreg.HKEY_CURRENT_USER, datos_opcion['ruta'])
            try:
                valor, _ = winreg.QueryValueEx(clave, datos_opcion['valor'])
                if valor == datos_opcion['data']:
                    # Verificar configuraciones adicionales para Noticias e Intereses
                    if 'registros_extra' in datos_opcion:
                        todos_deshabilitados = True
                        for reg_extra in datos_opcion['registros_extra']:
                            try:
                                clave_extra = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_extra['ruta'])
                                valor_extra, _ = winreg.QueryValueEx(clave_extra, reg_extra['nombre'])
                                if valor_extra != reg_extra['dato']:
                                    todos_deshabilitados = False
                                winreg.CloseKey(clave_extra)
                            except:
                                todos_deshabilitados = False
                        
                        if todos_deshabilitados:
                            btn_deshabilitar.config(state='disabled', text=self.textos_ui[self.idioma_actual]["deshabilitado"])
                        else:
                            btn_deshabilitar.config(state='normal', text=self.textos_ui[self.idioma_actual]["deshabilitar"])
                    else:
                        btn_deshabilitar.config(state='disabled', text=self.textos_ui[self.idioma_actual]["deshabilitado"])
                else:
                    btn_deshabilitar.config(state='normal', text=self.textos_ui[self.idioma_actual]["deshabilitar"])
            except WindowsError:
                btn_deshabilitar.config(state='normal', text=self.textos_ui[self.idioma_actual]["deshabilitar"])
            winreg.CloseKey(clave)
        except Exception as e:
            print(f"Error comprobando estado de {nombre_opcion}: {str(e)}")
            btn_deshabilitar.config(state='normal', text=self.textos_ui[self.idioma_actual]["deshabilitar"])
    
    def _deshabilitar_opcion_barra(self, nombre_opcion, datos_opcion):
        confirmar = messagebox.askyesno(
            self.textos_ui[self.idioma_actual]["confirmar"],
            f"¿Seguro que quieres deshabilitar {nombre_opcion} en la barra de tareas?\n\nEl Explorador de Windows se reiniciará para aplicar los cambios.",
            icon='warning'
        )
        if confirmar:
            try:
                # Aplicar el cambio principal en el registro
                clave = winreg.CreateKey(winreg.HKEY_CURRENT_USER, datos_opcion['ruta'])
                winreg.SetValueEx(clave, datos_opcion['valor'], 0, datos_opcion['tipo'], datos_opcion['data'])
                winreg.CloseKey(clave)
                
                # Ejecutar cambios adicionales si existen (usando winreg en lugar de comandos)
                if 'registros_extra' in datos_opcion:
                    for reg_extra in datos_opcion['registros_extra']:
                        try:
                            clave_extra = winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_extra['ruta'])
                            winreg.SetValueEx(clave_extra, reg_extra['nombre'], 0, reg_extra['tipo'], reg_extra['dato'])
                            winreg.CloseKey(clave_extra)
                        except Exception as e:
                            print(f"Error aplicando registro extra: {str(e)}")
                
                # Reiniciar el Explorador de Windows para aplicar cambios
                utils.reiniciar_explorer()
                
                # Actualizar estado del botón
                self._actualizar_estado_boton(nombre_opcion)
                
                messagebox.showinfo(self.textos_ui[self.idioma_actual]["exito"], 
                                f"{nombre_opcion} ha sido deshabilitado completamente.\n\nEl Explorador de Windows se ha reiniciado para aplicar los cambios.")
                
            except Exception as e:
                messagebox.showerror(self.textos_ui[self.idioma_actual]["error"], f"No se pudo deshabilitar {nombre_opcion}: {str(e)}")
    
    def _actualizar_estado_boton(self, nombre_opcion):
        """Actualiza el estado del botón en la interfaz"""
        for widget in self.winfo_children():
            if isinstance(widget, ttk.Notebook):
                for pestana in widget.winfo_children():
                    if self.textos_ui[self.idioma_actual]["barra_tareas"] in widget.tab(pestana, "text"):
                        for tarjeta in pestana.winfo_children():
                            if isinstance(tarjeta, tk.Canvas):
                                for marco in tarjeta.winfo_children():
                                    if isinstance(marco, ttk.Frame):
                                        for hijo in marco.winfo_children():
                                            if isinstance(hijo, ttk.Frame) and nombre_opcion in [lbl['text'] for lbl in hijo.winfo_children() if isinstance(lbl, ttk.Label)]:
                                                for btn in hijo.winfo_children():
                                                    if isinstance(btn, ttk.Button):
                                                        btn.config(state='disabled', text=self.textos_ui[self.idioma_actual]["deshabilitado"])
                                                        return
    
    #####################################################################################################
    #### PESTAÑA HERRAMIENTAS #####################################################################################################
    
    def _crear_pestana_herramientas(self):
        pestana = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(pestana, text=self.textos_ui[self.idioma_actual]["herramientas"])
        
        marco_desplazable = MarcoDesplazable(pestana)
        marco_desplazable.pack(fill='both', expand=True)
        
        # Sección OneDrive
        marco_onedrive = ttk.Frame(marco_desplazable.marco_desplazable, style='Card.TFrame', padding=15)
        marco_onedrive.pack(fill='x', pady=10)
        
        ttk.Label(marco_onedrive, 
                 text="Administrador de OneDrive", 
                 style='Card.TLabel', 
                 font=self.FUENTES['subtitulo']).pack(anchor='w')
        
        ttk.Label(marco_onedrive, 
                 text="Desinstala completamente OneDrive y elimina todos sus componentes",
                 style='Card.TLabel').pack(anchor='w', pady=(5, 15))
        
        self.btn_onedrive = ttk.Button(marco_onedrive, 
                                     text="Desinstalar OneDrive", 
                                     command=self._desinstalar_onedrive,
                                     style='Danger.TButton')
        self.btn_onedrive.pack(side='left', padx=5)
        
        # Sección optimización
        marco_optimizar = ttk.Frame(marco_desplazable.marco_desplazable, style='Card.TFrame', padding=15)
        marco_optimizar.pack(fill='x', pady=10)
        
        ttk.Label(marco_optimizar, 
                 text="Optimización Avanzada", 
                 style='Card.TLabel', 
                 font=self.FUENTES['subtitulo']).pack(anchor='w')
        
        ttk.Label(marco_optimizar,
                 text="Aplica configuraciones avanzadas para mejorar el rendimiento",
                 style='Card.TLabel').pack(anchor='w', pady=(5, 15))
        
        ttk.Button(marco_optimizar, 
                  text="Optimizar Sistema", 
                  command=self._abrir_optimizacion_avanzada,
                  style='Accent.TButton').pack(side='left', padx=5)
        
        # Comandos personalizados
        marco_comandos = ttk.Frame(marco_desplazable.marco_desplazable, style='Card.TFrame', padding=15)
        marco_comandos.pack(fill='x', pady=10)
        
        ttk.Label(marco_comandos, 
                 text="Comandos Personalizados",
                 style='Card.TLabel', 
                 font=self.FUENTES['subtitulo']).pack(anchor='w')
        
        self.entrada_comando = ttk.Entry(marco_comandos, width=50)
        self.entrada_comando.pack(side='left', padx=5, pady=5, fill='x', expand=True)
        
        ttk.Button(marco_comandos, 
                  text="Ejecutar", 
                  command=self._ejecutar_comando_personalizado,
                  style='Accent.TButton').pack(side='left', padx=5)
    
    def _abrir_optimizacion_avanzada(self):
        ventana_optimizacion = tk.Toplevel(self)
        ventana_optimizacion.title("Optimización Avanzada")
        ventana_optimizacion.geometry("600x500")
        ventana_optimizacion.resizable(False, False)
        ventana_optimizacion.configure(bg=self.COLORES['fondo_oscuro'])
        
        # Marco principal
        marco_principal = ttk.Frame(ventana_optimizacion, style='TFrame')
        marco_principal.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Título
        ttk.Label(marco_principal,
                 text="Optimizaciones Avanzadas",
                 style='TLabel',
                 font=self.FUENTES['titulo']).pack(pady=(0, 20))
        
        # Marco desplazable
        canvas = tk.Canvas(marco_principal, bg=self.COLORES['fondo_oscuro'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(marco_principal, orient='vertical', command=canvas.yview)
        
        marco_desplazable = ttk.Frame(canvas, style='TFrame')
        marco_desplazable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0, 0), window=marco_desplazable, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Crear tarjetas para cada optimización
        for i, (nombre_opt, datos_opt) in enumerate(optimizations.OPTIMIZACIONES.items()):
            self._crear_tarjeta_optimizacion(marco_desplazable, nombre_opt, datos_opt, i)
    
    def _crear_tarjeta_optimizacion(self, padre, nombre_opt, datos_opt, fila):
        tarjeta = ttk.Frame(padre, style='Card.TFrame', padding=15)
        tarjeta.grid(row=fila, column=0, sticky='ew', pady=5, padx=5)
        tarjeta.grid_columnconfigure(1, weight=1)
        
        # Nombre de la optimización
        etiqueta_nombre = ttk.Label(tarjeta, text=nombre_opt, style='Card.TLabel')
        etiqueta_nombre.grid(row=0, column=0, sticky='w', padx=(0, 20))
        
        # Descripción (tooltip)
        etiqueta_desc = ttk.Label(tarjeta, 
                             text="ℹ️",
                             style='Card.TLabel',
                             cursor='question_arrow')
        etiqueta_desc.grid(row=0, column=1, sticky='w')
        
        # Tooltip
        self._crear_tooltip(etiqueta_desc, datos_opt['descripcion'])
        
        # Botón aplicar
        btn_aplicar = ttk.Button(tarjeta, 
                             text="Aplicar", 
                             command=lambda n=nombre_opt, c=datos_opt['comando']: self._aplicar_optimizacion(n, c),
                             style='Accent.TButton')
        btn_aplicar.grid(row=0, column=2, sticky='e')
    
    def _aplicar_optimizacion(self, nombre_opt, comando):
        confirmar = messagebox.askyesno(
            self.textos_ui[self.idioma_actual]["confirmar"],
            f"¿Seguro que quieres aplicar la optimización '{nombre_opt}'?",
            icon='warning'
        )
        if confirmar:
            try:
                resultado = subprocess.run(comando, shell=True, capture_output=True, text=True, timeout=30)
                
                if resultado.returncode == 0:
                    messagebox.showinfo(self.textos_ui[self.idioma_actual]["exito"], 
                                      f"Optimización '{nombre_opt}' aplicada correctamente.\n\nSalida:\n{resultado.stdout}")
                else:
                    messagebox.showerror(self.textos_ui[self.idioma_actual]["error"], 
                                       f"No se pudo aplicar la optimización '{nombre_opt}':\n\n{resultado.stderr}")
            except subprocess.TimeoutExpired:
                messagebox.showerror(self.textos_ui[self.idioma_actual]["error"], 
                                   f"La optimización '{nombre_opt}' excedió el tiempo de ejecución.")
            except Exception as e:
                messagebox.showerror(self.textos_ui[self.idioma_actual]["error"], 
                                   f"Error inesperado aplicando '{nombre_opt}':\n\n{str(e)}")
    
    def _desinstalar_onedrive(self):
        confirmar = messagebox.askyesno(
            self.textos_ui[self.idioma_actual]["confirmar"],
            "¿Seguro que quieres desinstalar completamente OneDrive?\n\nEsto detendrá el servicio y eliminará todos los componentes.",
            icon='warning'
        )
        if confirmar:
            self.btn_onedrive.config(state='disabled')
            threading.Thread(
                target=self._ejecutar_desinstalacion_onedrive,
                daemon=True
            ).start()
    
    def _ejecutar_desinstalacion_onedrive(self):
        try:
            self._encolar_actualizacion("Desinstalando OneDrive...", self.COLORES['advertencia'])
            
            # Detener proceso OneDrive
            subprocess.run(["taskkill", "/f", "/im", "OneDrive.exe"], check=True)
            
            # Comandos de desinstalación
            comandos = [
                r'if (Test-Path "$env:SystemRoot\SysWOW64\OneDriveSetup.exe") { & "$env:SystemRoot\SysWOW64\OneDriveSetup.exe" /uninstall }',
                r'if (Test-Path "$env:SystemRoot\System32\OneDriveSetup.exe") { & "$env:SystemRoot\System32\OneDriveSetup.exe" /uninstall }',
                r'Remove-Item -Recurse -Force -ErrorAction SilentlyContinue "$env:LocalAppData\Microsoft\OneDrive"',
                r'Remove-Item -Recurse -Force -ErrorAction SilentlyContinue "$env:ProgramData\Microsoft OneDrive"',
                r'Remove-Item -Recurse -Force -ErrorAction SilentlyContinue "$env:SystemDrive\OneDriveTemp"',
                r'Remove-Item -Recurse -Force -ErrorAction SilentlyContinue "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\OneDriveSetup.exe"',
                r'Get-AppxPackage *OneDrive* | Remove-AppxPackage -ErrorAction SilentlyContinue',
                r'Get-AppxProvisionedPackage -Online | Where-Object {$_.PackageName -like "*OneDrive*"} | Remove-AppxProvisionedPackage -Online -ErrorAction SilentlyContinue'
            ]
            
            for cmd in comandos:
                subprocess.run(["powershell", "-Command", cmd], 
                              timeout=30,
                              creationflags=subprocess.CREATE_NO_WINDOW)
            
            self._encolar_actualizacion("OneDrive desinstalado completamente", self.COLORES['exito'])
            
            # Actualizar UI
            if "OneDrive" in self.tarjetas_apps:
                self._encolar_actualizacion_unica("OneDrive")
            
            if "OneDrive" in self.tarjetas_inicio:
                self._verificar_estado_app_inicio("OneDrive", apps.APPS_INICIO["OneDrive"])
            
        except Exception as e:
            self._encolar_actualizacion(f"Error desinstalando OneDrive: {str(e)}", self.COLORES['error'])
        finally:
            self.btn_onedrive.config(state='normal')
    
    def _optimizar_sistema(self):
        confirmar = messagebox.askyesno(
            self.textos_ui[self.idioma_actual]["confirmar"],
            "¿Seguro que quieres aplicar optimizaciones al sistema?\n\nAlgunos cambios pueden requerir reinicio.",
            icon='warning'
        )
        if not confirmar:
            return
            
        try:
            self._encolar_actualizacion("Iniciando optimización del sistema...", self.COLORES['advertencia'])
            
            # Ejecutar cada optimización
            for nombre, datos_opt in optimizations.OPTIMIZACIONES.items():
                self._encolar_actualizacion(f"Aplicando: {nombre}...", self.COLORES['advertencia'])
                resultado = subprocess.run(datos_opt['comando'], shell=True, capture_output=True, text=True)
                
                if resultado.returncode != 0:
                    raise subprocess.CalledProcessError(resultado.returncode, datos_opt['comando'], resultado.stderr)
            
            self._encolar_actualizacion("Optimización completada con éxito", self.COLORES['exito'])
            
            # Mostrar resumen
            messagebox.showinfo(self.textos_ui[self.idioma_actual]["optimizacion_completa"],
                              "Todas las optimizaciones configuradas han sido aplicadas.\n\nAlgunos cambios pueden requerir reinicio.")
            
        except subprocess.CalledProcessError as e:
            self._encolar_actualizacion(f"Error de optimización: {e.stderr}", self.COLORES['error'])
            messagebox.showerror(self.textos_ui[self.idioma_actual]["error"], 
                               f"No se pudo completar la optimización:\n\n{e.stderr}")
        except Exception as e:
            self._encolar_actualizacion(f"Error inesperado: {str(e)}", self.COLORES['error'])
            messagebox.showerror(self.textos_ui[self.idioma_actual]["error"], 
                               f"Ocurrió un error inesperado:\n\n{str(e)}")
    
    def _ejecutar_comando_personalizado(self):
        comando = self.entrada_comando.get().strip()
        if not comando:
            messagebox.showwarning("Comando Vacío", "Por favor ingresa un comando para ejecutar")
            return
            
        confirmar = messagebox.askyesno(
            self.textos_ui[self.idioma_actual]["confirmar"],
            f"¿Seguro que quieres ejecutar el siguiente comando?\n\n{comando}",
            icon='warning'
        )
        if not confirmar:
            return
            
        try:
            self._encolar_actualizacion(f"Ejecutando: {comando}", self.COLORES['advertencia'])
            
            resultado = subprocess.run(comando, shell=True, 
                                  capture_output=True, text=True,
                                  timeout=30)
            
            salida = f"Salida:\n{resultado.stdout}"
            if resultado.stderr:
                salida += f"\n\nErrores:\n{resultado.stderr}"
            
            self._encolar_actualizacion("Comando ejecutado", self.COLORES['exito'])
            messagebox.showinfo(self.textos_ui[self.idioma_actual]["resultado_comando"], salida)
            
        except subprocess.TimeoutExpired:
            self._encolar_actualizacion("Comando excedió el tiempo", self.COLORES['error'])
            messagebox.showerror(self.textos_ui[self.idioma_actual]["error"], "El comando excedió el tiempo máximo de ejecución")
        except Exception as e:
            self._encolar_actualizacion(f"Error en comando: {str(e)}", self.COLORES['error'])
            messagebox.showerror(self.textos_ui[self.idioma_actual]["error"], f"No se pudo ejecutar el comando:\n\n{str(e)}")
    
    ####################################################################
    ### CARACTERISTICAS##########################################
    
    def _crear_pestana_caracteristicas(self):
        """Crear pestaña de opciones de características y tareas de Windows"""
        pestana = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(pestana, text=self.textos_ui[self.idioma_actual]["caracteristicas"])
        
        marco_desplazable = MarcoDesplazable(pestana)
        marco_desplazable.pack(fill='both', expand=True)
        
        for i, (nombre_opcion, datos_opcion) in enumerate(task.CARACTERISTICAS_OPCIONALES.items()):
            self._crear_tarjeta_caracteristicas(marco_desplazable.marco_desplazable, nombre_opcion, datos_opcion, i)

    def _crear_tarjeta_caracteristicas(self, padre, nombre_opcion, datos_opcion, fila):
        tarjeta = ttk.Frame(padre, style='Card.TFrame', padding=15)
        tarjeta.grid(row=fila, column=0, sticky='ew', pady=5, padx=5)
        tarjeta.grid_columnconfigure(1, weight=1)
        
        # Nombre de la opción
        etiqueta_nombre = ttk.Label(tarjeta, text=datos_opcion['nombre'], style='Card.TLabel')
        etiqueta_nombre.grid(row=0, column=0, sticky='w', padx=(0, 20))
        
        # Descripción (tooltip)
        etiqueta_desc = ttk.Label(tarjeta, 
                            text="ℹ️",
                            style='Card.TLabel',
                            cursor='question_arrow')
        etiqueta_desc.grid(row=0, column=1, sticky='w')
        
        # Tooltip
        self._crear_tooltip(etiqueta_desc, datos_opcion['descripcion'])
        
        #Estado
        etiqueta_estado = ttk.Label(tarjeta, text=self.textos_ui[self.idioma_actual]["comprobando"], style='Card.TLabel')
        etiqueta_estado.grid(row=0, column=2, sticky='w')
        
        # Botones
        marco_botones = ttk.Frame(tarjeta, style='TFrame')
        marco_botones.grid(row=0, column=3, sticky='e')
        
        btn_deshabilitar = ttk.Button(marco_botones,
                               text=self.textos_ui[self.idioma_actual]["deshabilitar"], 
                               command=lambda c=nombre_opcion, n=datos_opcion["nombre"] : self._deshabilitar_caracteristica(c,n),
                               style='Danger.TButton')
        btn_deshabilitar.pack(side='left', padx=5)
        
        # Guardar referencia
        self.tarjetas_caracteristicas[nombre_opcion] = {
            'marco': tarjeta,
            'estado': etiqueta_estado,
            'btn_deshabilitar': btn_deshabilitar
        }
        
        # Comprobar estado inicial
        self._verificar_estado_caracteristicas(nombre_opcion, datos_opcion["nombre"])
        
    import subprocess

    def _verificar_estado_caracteristicas(self, nombre_opcion, nombre_legible):
        try:
            # Ejecutar comando PowerShell para obtener estado
            cmd = [
                "powershell", "-Command",
                f"Get-WindowsOptionalFeature -Online -FeatureName '{nombre_opcion}' | Select-Object -ExpandProperty State"
            ]
            resultado = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            salida = resultado.stdout.strip().lower()
            error = resultado.stderr.strip().lower()

            #print(f"[DEBUG] PowerShell stdout para {nombre_opcion}:\n{salida}")
            #print(f"[DEBUG] PowerShell stderr para {nombre_opcion}:\n{error}")

            if "not found" in error or "cannot find" in error or salida == "":
                estado = self.textos_ui[self.idioma_actual].get("no_encontrado", "No encontrado")
                estilo = 'Card.TLabel'
            else:
                if salida == "enabled":
                    estado = self.textos_ui[self.idioma_actual]["habilitado"]
                    estilo = 'StatusOn.TLabel'
                elif salida == "disabled":
                    estado = self.textos_ui[self.idioma_actual]["deshabilitado"]
                    estilo = 'StatusOff.TLabel'
                else:
                    estado = self.textos_ui[self.idioma_actual]["desconocido"]
                    estilo = 'Card.TLabel'

        except Exception as e:
            estado = self.textos_ui[self.idioma_actual]["desconocido"]
            estilo = 'Card.TLabel'
            print(f"[ERROR] Característica {nombre_opcion} ({nombre_legible}): {e}")
            return

        if nombre_opcion in self.tarjetas_caracteristicas:
            self.tarjetas_caracteristicas[nombre_opcion]['estado'].config(text=estado, style=estilo)



        #clave = nombre_opcion
        #datos = datos_opcion
    def _deshabilitar_caracteristica(self, nombre_opcion, nombre_legible):
        estado_actual = self.tarjetas_caracteristicas[nombre_opcion]["estado"].cget("text")

        if estado_actual == self.textos_ui[self.idioma_actual]["desconocido"]:
            messagebox.showwarning(
                self.textos_ui[self.idioma_actual]["advertencia"],
                f"No se puede deshabilitar la característica \"{nombre_legible}\" porque su estado es desconocido."
            )
            return

        try:
            resultado = subprocess.run(
                ["dism", "/Online", "/Disable-Feature", f"/FeatureName:{nombre_opcion}", "/NoRestart"],
                capture_output=True, text=True, timeout=30
            )

            print(f"[DEBUG] Código de salida: {resultado.returncode}")
            print(f"[DEBUG] STDOUT:\n{resultado.stdout}")
            print(f"[DEBUG] STDERR:\n{resultado.stderr}")

            if resultado.returncode == 0 or resultado.returncode == 3010:
                self.tarjetas_caracteristicas[nombre_opcion]["estado"].config(
                    text=self.textos_ui[self.idioma_actual]["deshabilitado"],
                    style='StatusOff.TLabel'
                )
                if resultado.returncode == 3010:
                    messagebox.showinfo(
                        self.textos_ui[self.idioma_actual]["exito"],
                        f"Característica \"{nombre_legible}\" deshabilitada.\n\n⚠️ Se requiere reiniciar el sistema para aplicar los cambios."
                    )
                else:
                    messagebox.showinfo(
                        self.textos_ui[self.idioma_actual]["exito"],
                        f"Característica \"{nombre_legible}\" deshabilitada con éxito."
                    )
            else:
                raise subprocess.CalledProcessError(resultado.returncode, resultado.args, output=resultado.stdout, stderr=resultado.stderr)

        except subprocess.CalledProcessError as e:
            messagebox.showerror(
                self.textos_ui[self.idioma_actual]["error"],
                f"No se pudo deshabilitar la característica \"{nombre_legible}\".\n\nCódigo: {e.returncode}\n\n{e.stderr}"
            )



    
    ########################################################################################################################################################################################### 
    
    def _confirmar_accion(self, nombre_app, accion):
        confirmar = messagebox.askyesno(
            self.textos_ui[self.idioma_actual]["confirmar"],
            f"¿Seguro que quieres {accion} {nombre_app}?",
            icon='warning' if accion == "uninstall" else 'question'
        )
        if confirmar:
            self._alternar_app(nombre_app, accion)
    
    def _alternar_app(self, nombre_app, accion):
        app_id = apps.APPS[nombre_app]
        
        # Deshabilitar botones durante operación
        self._establecer_estado_botones_app(nombre_app, False)
        self.tarjetas_apps[nombre_app]['estado'].config(text=self.textos_ui[self.idioma_actual]["procesando"], style='Card.TLabel')
        
        # Configurar comando y mensajes
        if accion == "install":
            cmd = f"""
            Get-AppxPackage -AllUsers *{app_id}* | Foreach {{
                Add-AppxPackage -DisableDevelopmentMode -Register "$($_.InstallLocation)\AppXManifest.xml"
            }}
            """
            mensaje_exito = f"{nombre_app} instalado con éxito"
            mensaje_error = f"Error instalando {nombre_app}"
        else:
            cmd = f"""
            Get-AppxPackage *{app_id}* | Remove-AppxPackage -ErrorAction SilentlyContinue
            Get-AppxProvisionedPackage -Online | Where-Object {{$_.PackageName -like '*{app_id}*'}} | Remove-AppxProvisionedPackage -Online -ErrorAction SilentlyContinue
            """
            mensaje_exito = f"{nombre_app} desinstalado con éxito"
            mensaje_error = f"Error desinstalando {nombre_app}"
        
        # Ejecutar en hilo separado
        threading.Thread(
            target=self._ejecutar_comando_con_reintentos,
            args=(cmd, nombre_app, mensaje_exito, mensaje_error, 3),
            daemon=True
        ).start()
    
    def _ejecutar_comando_con_reintentos(self, cmd, nombre_app, mensaje_exito, mensaje_error, max_reintentos):
        reintentos = 0
        while reintentos < max_reintentos:
            if self.cancelar_solicitado:
                self._encolar_actualizacion("Operación cancelada", self.COLORES['advertencia'])
                self._encolar_estado_botones(True)
                return
            
            try:
                resultado = subprocess.run(["powershell", "-Command", cmd], 
                                      check=True, 
                                      stdout=subprocess.PIPE, 
                                      stderr=subprocess.PIPE,
                                      timeout=60,
                                      creationflags=subprocess.CREATE_NO_WINDOW)
                
                if resultado.returncode == 0:
                    self._encolar_actualizacion(mensaje_exito, self.COLORES['exito'])
                    # Forzar actualización de estado
                    self.cache_estado_apps.pop(nombre_app, None)
                    self._encolar_actualizacion_unica(nombre_app)
                    time.sleep(2)
                    self._encolar_actualizacion_unica(nombre_app)
                    return
        
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
                print(f"Intento {reintentos+1} fallido: {str(e)}")
                reintentos += 1
                if reintentos < max_reintentos:
                    time.sleep(3)
                    continue
        
        # Si falla después de reintentos
        self._encolar_actualizacion(mensaje_error, self.COLORES['error'])
        self._encolar_actualizacion_unica(nombre_app)
    
    def _actualizar_app_unica(self, nombre_app):
        """Actualizar estado de una sola app"""
        time.sleep(1)
        
        # Invalidar caché
        if nombre_app in self.cache_estado_apps:
            del self.cache_estado_apps[nombre_app]
        
        # Comprobar estado actual
        if nombre_app == "Cortana":
            esta_instalado = utils.verificar_estado_cortana()
        else:
            esta_instalado = utils.verificar_estado_app(apps.APPS[nombre_app])
        
        # Actualizar UI
        self._actualizar_estado_app_ui(nombre_app, esta_instalado)
        self._establecer_estado_botones_app(nombre_app, True)
        
        # Actualizar caché
        self.cache_estado_apps[nombre_app] = (esta_instalado, time.time())
    
    def actualizar_estados_apps(self, forzar_revision_completa=False):
        """Actualizar estados de todas las apps"""
        if self.revisando_estado:
            return
            
        self.revisando_estado = True
        self.cancelar_solicitado = False
        self.btn_actualizar.config(state='disabled')
        
        tiempo_actual = time.time()
        
        if forzar_revision_completa or (tiempo_actual - self.ultima_revision_completa > 300):
            self._revision_completa_estados()
            self.ultima_revision_completa = tiempo_actual
        else:
            self._revision_rapida_estados()
    
    def _revision_completa_estados(self):
        """Realizar comprobación completa de estados"""
        self._encolar_actualizacion("Comprobando todos los estados...", self.COLORES['advertencia'])
        
        threading.Thread(
            target=self._ejecutar_revision_completa,
            daemon=True
        ).start()
    
    def _ejecutar_revision_completa(self):
        """Ejecutar comprobación completa en segundo plano"""
        total_apps = len(apps.APPS)
        completadas = 0
        
        with ThreadPoolExecutor(max_workers=5) as ejecutor:
            futuros = {ejecutor.submit(self._verificar_estado_app_unica, nombre_app): nombre_app 
                      for nombre_app in apps.APPS.keys()}
            
            for futuro in as_completed(futuros):
                if self.cancelar_solicitado:
                    self._encolar_actualizacion("Comprobación cancelada", self.COLORES['advertencia'])
                    break
                
                nombre_app = futuros[futuro]
                try:
                    futuro.result()
                except:
                    pass
                
                completadas += 1
                progreso = int((completadas / total_apps) * 100)
                self._encolar_progreso(progreso, f"Comprobando ({completadas}/{total_apps})")
        
        if not self.cancelar_solicitado:
            self._encolar_actualizacion("Comprobación completada", self.COLORES['exito'])
        
        self._encolar_estado_botones(True)
        self._encolar_estado_revision(False)
    
    def _revision_rapida_estados(self):
        """Actualizar solo estados cambiados"""
        self._encolar_actualizacion("Actualizando estados desde caché...", self.COLORES['advertencia'])
        
        apps_a_verificar = []
        tiempo_actual = time.time()
        
        for nombre_app in apps.APPS.keys():
            if (nombre_app not in self.cache_estado_apps or 
                tiempo_actual - self.cache_estado_apps[nombre_app][1] > 30):
                apps_a_verificar.append(nombre_app)
        
        total_apps = len(apps_a_verificar)
        if total_apps == 0:
            self._encolar_actualizacion("Estados actualizados (desde caché)", self.COLORES['exito'])
            self._encolar_estado_revision(False)
            self._encolar_estado_botones(True)
            return
        
        threading.Thread(
            target=self._ejecutar_revision_rapida,
            args=(apps_a_verificar, total_apps),
            daemon=True
        ).start()
    
    def _ejecutar_revision_rapida(self, apps_a_verificar, total_apps):
        """Ejecutar comprobación rápida en segundo plano"""
        completadas = 0
        
        with ThreadPoolExecutor(max_workers=3) as ejecutor:
            futuros = {ejecutor.submit(self._verificar_estado_app_unica, nombre_app): nombre_app 
                      for nombre_app in apps_a_verificar}
            
            for futuro in as_completed(futuros):
                if self.cancelar_solicitado:
                    self._encolar_actualizacion("Actualización cancelada", self.COLORES['advertencia'])
                    break
                
                nombre_app = futuros[futuro]
                try:
                    futuro.result()
                except:
                    pass
                
                completadas += 1
                progreso = int((completadas / total_apps) * 100)
                self._encolar_progreso(progreso, f"Actualizando ({completadas}/{total_apps})")
        
        if not self.cancelar_solicitado:
            self._encolar_actualizacion("Estados actualizados", self.COLORES['exito'])
        
        self._encolar_estado_botones(True)
        self._encolar_estado_revision(False)
    
    def _verificar_estado_app_unica(self, nombre_app):
        """Comprobar estado de una sola app"""
        tiempo_actual = time.time()
        
        if (not self.cancelar_solicitado and 
            nombre_app in self.cache_estado_apps and 
            tiempo_actual - self.cache_estado_apps[nombre_app][1] < 5):
            estado_cache = self.cache_estado_apps[nombre_app][0]
            self._actualizar_estado_app_ui(nombre_app, estado_cache)
            return estado_cache
        
        max_reintentos = 3
        reintentos = 0
        esta_instalado = False
        
        while reintentos <= max_reintentos and not self.cancelar_solicitado:
            try:
                if nombre_app == "Cortana":
                    esta_instalado = utils.verificar_estado_cortana()
                else:
                    esta_instalado = utils.verificar_estado_app(apps.APPS[nombre_app])
                break
                    
            except Exception as e:
                print(f"Intento {reintentos} fallido para {nombre_app}: {e}")
                reintentos += 1
                if reintentos <= max_reintentos:
                    time.sleep(1)
        
        self.cache_estado_apps[nombre_app] = (esta_instalado, tiempo_actual)
        self._actualizar_estado_app_ui(nombre_app, esta_instalado)
        return esta_instalado
    
    def _actualizar_estado_app_ui(self, nombre_app, esta_instalado):
        """Actualizar estado de la app en la UI"""
        estado = self.textos_ui[self.idioma_actual]["instalado"] if esta_instalado else self.textos_ui[self.idioma_actual]["no_instalado"]
        estilo = 'StatusOn.TLabel' if esta_instalado else 'StatusOff.TLabel'
        
        if nombre_app in self.tarjetas_apps:
            self.tarjetas_apps[nombre_app]['estado'].config(text=estado, style=estilo)
    
    def _establecer_estado_botones_app(self, nombre_app, habilitado):
        """Habilitar/deshabilitar botones de la app"""
        estado = 'normal' if habilitado else 'disabled'
        if nombre_app in self.tarjetas_apps:
            self.tarjetas_apps[nombre_app]['btn_instalar'].config(state=estado)
            self.tarjetas_apps[nombre_app]['btn_desinstalar'].config(state=estado)
    
    def _encolar_actualizacion(self, mensaje, color=None):
        """Encolar actualización de estado"""
        if color is None:
            color = self.COLORES['texto']
        self.cola_estado.put(("actualizar", mensaje, color))
    
    def _encolar_progreso(self, valor, texto=""):
        """Encolar actualización de progreso"""
        self.cola_estado.put(("progreso", valor, texto))
    
    def _encolar_reiniciar_progreso(self):
        """Encolar reinicio de progreso"""
        self.cola_estado.put(("reiniciar_progreso",))
    
    def _encolar_actualizacion_estado_ui(self, nombre_app, esta_instalado):
        """Encolar actualización de estado en UI"""
        self.cola_estado.put(("actualizar_estado_ui", nombre_app, esta_instalado))
    
    def _encolar_estado_botones(self, habilitado):
        """Encolar cambio de estado de botones"""
        self.cola_estado.put(("habilitar_botones", habilitado))
    
    def _encolar_estado_revision(self, estado):
        """Encolar cambio de estado de comprobación"""
        self.cola_estado.put(("estado_revision", estado))
    
    def _encolar_actualizacion_unica(self, nombre_app):
        """Encolar actualización de una sola app"""
        self.cola_estado.put(("actualizar_unica", nombre_app))
    
    def procesar_cola(self):
        """Procesar operaciones encoladas"""
        while not self.cola_estado.empty():
            tarea = self.cola_estado.get()
            
            if tarea[0] == "actualizar":
                self.actualizar_estado(tarea[1], tarea[2])
            elif tarea[0] == "progreso":
                self.actualizar_progreso(tarea[1], tarea[2])
            elif tarea[0] == "reiniciar_progreso":
                self.actualizar_progreso(0, "")
            elif tarea[0] == "actualizar_estado_ui":
                self._actualizar_estado_app_ui(tarea[1], tarea[2])
            elif tarea[0] == "habilitar_botones":
                self.btn_actualizar.config(state='normal' if tarea[1] else 'disabled')
            elif tarea[0] == "estado_revision":
                self.revisando_estado = tarea[1]
            elif tarea[0] == "actualizar_unica":
                self._actualizar_app_unica(tarea[1])
        
        self.after(100, self.procesar_cola)
    
    def actualizar_estado(self, mensaje, color=None):
        """Actualizar barra de estado"""
        if color is None:
            color = self.COLORES['texto']
        self.etiqueta_estado.config(foreground=color)
        self.etiqueta_estado.config(text=mensaje)
    
    def actualizar_progreso(self, valor, texto=""):
        """Actualizar barra de progreso"""
        if hasattr(self, 'barra_progreso'):
            self.barra_progreso['value'] = valor
            if texto and hasattr(self, 'etiqueta_progreso'):
                self.etiqueta_progreso.config(text=texto)
    
    def centrar_ventana(self):
        """Centrar ventana en pantalla"""
        self.update_idletasks()
        ancho = self.winfo_width()
        alto = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def _crear_barra_estado(self):
        """Crear barra de estado en la parte inferior"""
        marco_estado = ttk.Frame(self, style='TFrame', padding=(10, 5))
        marco_estado.grid(row=2, column=0, sticky='ew', padx=20, pady=(0, 10))
        
        # Etiqueta de estado
        self.etiqueta_estado = ttk.Label(marco_estado, 
                                    text=self.textos_ui[self.idioma_actual]["estado_listo"], 
                                    style='TLabel',
                                    font=self.FUENTES['estado'])
        self.etiqueta_estado.pack(side='left', anchor='w')
        
        # Barra de progreso (inicialmente oculta)
        marco_progreso = ttk.Frame(marco_estado, style='TFrame')
        marco_progreso.pack(side='right', anchor='e')
        
        self.barra_progreso = ttk.Progressbar(marco_progreso, 
                                        orient='horizontal', 
                                        mode='determinate',
                                        length=150)
        self.barra_progreso.pack(side='left', padx=(10, 5))
        
        self.etiqueta_progreso = ttk.Label(marco_progreso, 
                                    text="", 
                                    style='TLabel',
                                    font=self.FUENTES['tooltip'])
        self.etiqueta_progreso.pack(side='left')
        
        # Ocultar elementos de progreso inicialmente
        self.barra_progreso.grid_remove()
        self.etiqueta_progreso.grid_remove()
        
        # Botón de actualización
        self.btn_actualizar = ttk.Button(marco_estado,
                                    text=self.textos_ui[self.idioma_actual]["actualizar_todo"],
                                    command=lambda: self.actualizar_estados_apps(forzar_revision_completa=True),
                                    style='Accent.TButton')
        self.btn_actualizar.pack(side='right', padx=(10, 0))
        
    ############################################################################################################################ç
    ####OTHER############################################################################################################################
    def _crear_pestana_otros(self):
        pestana = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(pestana, text=self.textos_ui[self.idioma_actual]["otros"])

        marco_desplazable = MarcoDesplazable(pestana)
        marco_desplazable.pack(fill='both', expand=True)

        self._crear_seccion_apariencia(marco_desplazable.marco_desplazable)
        self._crear_seccion_herramientas_adicionales(marco_desplazable.marco_desplazable)

    def _crear_seccion_apariencia(self, padre):
        marco = ttk.Frame(padre, style='Card.TFrame', padding=15)
        marco.pack(fill='x', pady=10, padx=5)
        self._crear_circulo_cromatico(padre)
        ttk.Label(marco, 
                text=self.textos_ui[self.idioma_actual]["apariencia"], 
                style='Card.TLabel',
                font=self.FUENTES['subtitulo']).pack(anchor='w')

        for i, (nombre_opcion, datos_opcion) in enumerate(others.THEMES.items()):
            self._crear_tarjeta_apariencia(marco, nombre_opcion, datos_opcion, i)

    def _crear_tarjeta_apariencia(self, padre, nombre_opcion, datos_opcion, fila):
        tarjeta = ttk.Frame(padre, style='Card.TFrame', padding=10)
        tarjeta.pack(fill='x', pady=5, padx=5)  # Cambiado de .grid() a .pack()

        contenedor = ttk.Frame(tarjeta, style='Card.TFrame')
        contenedor.pack(fill='x')

        ttk.Label(contenedor, text=nombre_opcion, style='Card.TLabel').pack(side='left', padx=(0, 20))

        etiqueta_desc = ttk.Label(contenedor, text="ℹ️", style='Card.TLabel', cursor='question_arrow')
        etiqueta_desc.pack(side='left')
        self._crear_tooltip(etiqueta_desc, datos_opcion['descripcion'])

        btn_aplicar = ttk.Button(
            contenedor, 
            text=self.textos_ui[self.idioma_actual]["aplicar_apariencia"],
            command=lambda n=nombre_opcion, d=datos_opcion: self._aplicar_apariencia(n, d),
            style='Accent.TButton'
        )
        btn_aplicar.pack(side='right')

    def _aplicar_apariencia(self, nombre_opcion, datos_opcion):
        try:
            clave = winreg.CreateKey(winreg.HKEY_CURRENT_USER, datos_opcion['ruta'])
            winreg.SetValueEx(clave, datos_opcion['valor'], 0, datos_opcion['tipo'], datos_opcion['data'])
            winreg.CloseKey(clave)

            messagebox.showinfo(
                self.textos_ui[self.idioma_actual]["exito"], 
                f"Apariencia '{nombre_opcion}' aplicada.\n\nPuede que necesites reiniciar las aplicaciones o el Explorador para ver los cambios."
            )
        except Exception as e:
            messagebox.showerror(
                self.textos_ui[self.idioma_actual]["error"], 
                f"No se pudo aplicar la apariencia '{nombre_opcion}': {str(e)}"
            )
            
    #############################################################################################################################ç
    #paleta cromatica
    

    def _crear_circulo_cromatico(self, padre):
        marco_colores = ttk.Frame(padre, style='Card.TFrame')
        marco_colores.pack(pady=(10, 10), fill='x')

        ttk.Label(marco_colores, text="🎨 Color de énfasis (tipo Windows)", style='Card.TLabel').pack(anchor='w', pady=(0, 5))

        paleta_frame = ttk.Frame(marco_colores)
        paleta_frame.pack()

        for i, color_hex in enumerate(others.COLORES_ENFASIS_WINDOWS):
            btn_color = tk.Button(
                paleta_frame,
                bg=color_hex,
                width=3,
                height=1,
                relief='flat',
                command=lambda c=color_hex: self._aplicar_color_enfasis(c, c)
            )
            btn_color.grid(row=i // 8, column=i % 8, padx=2, pady=2)


    def _aplicar_color_enfasis(self, nombre_color, hex_color):
        try:
            r = int(hex_color[1:3], 16)
            g = int(hex_color[3:5], 16)
            b = int(hex_color[5:7], 16)
            bgr_dword = (b << 16) | (g << 8) | r

            claves = [
                (r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize", "ColorPrevalence", winreg.REG_DWORD, 1),
                (r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize", "AutoColorization", winreg.REG_DWORD, 0),
                (r"Software\Microsoft\Windows\DWM", "AccentColor", winreg.REG_DWORD, bgr_dword),
                (r"Software\Microsoft\Windows\DWM", "ColorizationColor", winreg.REG_DWORD, bgr_dword),
                (r"Software\Microsoft\Windows\DWM", "ColorPrevalence", winreg.REG_DWORD, 1),
                (r"Software\Microsoft\Windows\CurrentVersion\Explorer\Accent", "AccentColorMenu", winreg.REG_DWORD, bgr_dword),
            ]

            for ruta, valor, tipo, data in claves:
                clave = winreg.CreateKey(winreg.HKEY_CURRENT_USER, ruta)
                winreg.SetValueEx(clave, valor, 0, tipo, data)
                winreg.CloseKey(clave)

            messagebox.showinfo("Éxito", f"Color de énfasis '{nombre_color}' aplicado correctamente.\n\nPuedes reiniciar el Explorador para ver todos los cambios.")
        
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo aplicar el color de énfasis:\n{e}")


    def _aplicar_apariencia(self, nombre_opcion, datos_opcion):
        try:
            clave = winreg.CreateKey(winreg.HKEY_CURRENT_USER, datos_opcion['ruta'])
            winreg.SetValueEx(clave, datos_opcion['valor'], 0, datos_opcion['tipo'], datos_opcion['data'])
            winreg.CloseKey(clave)

            messagebox.showinfo(
                self.textos_ui[self.idioma_actual]["exito"], 
                f"Apariencia '{nombre_opcion}' aplicada.\n\nPuede que necesites reiniciar las aplicaciones o el Explorador para ver los cambios."
            )
        except Exception as e:
            messagebox.showerror(
                self.textos_ui[self.idioma_actual]["error"], 
                f"No se pudo aplicar la apariencia '{nombre_opcion}': {str(e)}"
            )



   
    
    ########################################################################################

    def _crear_seccion_herramientas_adicionales(self, padre):
        marco = ttk.Frame(padre, style='Card.TFrame', padding=15)
        marco.pack(fill='x', pady=10, padx=5)

        ttk.Label(marco, 
                text="Herramientas Adicionales", 
                style='Card.TLabel',
                font=self.FUENTES['subtitulo']).pack(anchor='w')

        self.btn_reiniciar_explorer = ttk.Button(
            marco, 
            text=self.textos_ui[self.idioma_actual]["reiniciar_explorer"],
            command=self._reiniciar_explorer,
            style='Warning.TButton'
        )
        self.btn_reiniciar_explorer.pack(side='left', padx=5, pady=10)

    def _reiniciar_explorer(self):
        try:
            subprocess.run(["taskkill", "/f", "/im", "explorer.exe"], check=True)
            time.sleep(1)
            subprocess.Popen("explorer.exe")
            messagebox.showinfo(
                self.textos_ui[self.idioma_actual]["exito"], 
                "Explorador de Windows reiniciado correctamente"
            )
        except Exception as e:
            messagebox.showerror(
                self.textos_ui[self.idioma_actual]["error"], 
                f"Error reiniciando explorer.exe: {str(e)}"
            )
