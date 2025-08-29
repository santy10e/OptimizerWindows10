import winreg

THEMES = {
    "Modo Oscuro": {
        "ruta": r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
        "valor": "AppsUseLightTheme",
        "tipo": winreg.REG_DWORD,
        "data": 0,
        "descripcion": "Cambia las aplicaciones a modo oscuro"
    },
    "Modo Claro": {
        "ruta": r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
        "valor": "AppsUseLightTheme",
        "tipo": winreg.REG_DWORD,
        "data": 1,
        "descripcion": "Cambia las aplicaciones a modo claro"
    },
    "Barra de Tareas Oscura": {
        "ruta": r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
        "valor": "ColorPrevalence",
        "tipo": winreg.REG_DWORD,
        "data": 1,
        "descripcion": "Hace que la barra de tareas sea oscura"
    },
    "Barra de Tareas Clara": {
        "ruta": r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
        "valor": "ColorPrevalence",
        "tipo": winreg.REG_DWORD,
        "data": 0,
        "descripcion": "Hace que la barra de tareas sea clara"
    }
}

COLORES_ENFASIS_WINDOWS = [
    "#c50f1f", "#e81123", "#f7630c", "#ffb900", "#fff100",
    "#bad80a", "#70ad47", "#00b294", "#1aebff", "#0078d7",
    "#4262d6", "#6b69d6", "#8e8cd8", "#8764b8", "#b146c2",
    "#c239b3", "#e3008c", "#e74856", "#7a7574", "#5d5a58",
    "#68768a", "#515c6b", "#4c4a48", "#3b3a39", "#1b1b1b"
]

