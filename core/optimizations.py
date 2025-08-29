import winreg

OPTIMIZACIONES = {
    "Alto Rendimiento": {
        "comando": "powercfg -setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c",
        "descripcion": "Configura el plan de energía para máximo rendimiento."
    },
    "Menú de Arranque Clásico": {
        "comando": "bcdedit /set {current} bootmenupolicy legacy",
        "descripcion": "Restaura el menú de arranque clásico de Windows."
    },
    "Deshabilitar Último Acceso": {
        "comando": "fsutil behavior set disablelastaccess 1",
        "descripcion": "Desactiva el registro del último acceso a archivos."
    },
    "Deshabilitar Hibernación": {
        "comando": "powercfg -h off",
        "descripcion": "Desactiva la hibernación liberando espacio en disco."
    },
    "Limpiar Cache DNS": {
        "comando": "ipconfig /flushdns",
        "descripcion": "Borra la caché DNS local."
    },
    "Optimizar Unidades": {
        "comando": "defrag /C /H /V",
        "descripcion": "Desfragmenta HDD y optimiza SSD."
    }
    
}

OPCIONES_BARRA_TAREAS = {
    "Noticias e Intereses": {
        "hive": winreg.HKEY_LOCAL_MACHINE,  # <- Esto indica HKLM
        "ruta": r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer",
        "valor": "HideSCANewsAndInterestsButton",
        "tipo": winreg.REG_DWORD,
        "data": 1,
        "descripcion": "Desactiva el widget de Noticias e Intereses.",
        "registros_extra": [
            {
                "hive": winreg.HKEY_CURRENT_USER,  # o HKEY_LOCAL_MACHINE si lo deseas
                "ruta": r"Software\Microsoft\Windows\CurrentVersion\Feeds", 
                "nombre": "ShellFeedsTaskbarViewMode", 
                "tipo": winreg.REG_DWORD, 
                "dato": 2
            },
            {
                "hive": winreg.HKEY_CURRENT_USER,
                "ruta": r"Software\Microsoft\Windows\CurrentVersion\Feeds", 
                "nombre": "ShellFeedsTaskbarOpenOnHover", 
                "tipo": winreg.REG_DWORD, 
                "dato": 0
            }
        ]
    },
    "Búsqueda en Barra": {
        "ruta": r"Software\Microsoft\Windows\CurrentVersion\Search",
        "valor": "SearchboxTaskbarMode",
        "tipo": winreg.REG_DWORD,
        "data": 0,
        "descripcion": "Desactiva la barra de búsqueda."
    },
    "Vista de Tareas": {
        "ruta": r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
        "valor": "ShowTaskViewButton",
        "tipo": winreg.REG_DWORD,
        "data": 0,
        "descripcion": "Oculta el botón de Vista de Tareas."
    },
    "Personas": {
        "ruta": r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced\People",
        "valor": "PeopleBand",
        "tipo": winreg.REG_DWORD,
        "data": 0,
        "descripcion": "Desactiva la barra de contactos."
    },
    "Desactiva el seguimiento de programa": {
        "ruta": r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
        "valor": "Start_TrackProgs",
        "tipo": winreg.REG_DWORD,
        "data": 0,
        "descripcion": "Desactiva el seguimiento de programas usados recientemente.",
        "comandos_extra": [
            r'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" /v "Start_TrackDocs" /t REG_DWORD /d 0 /f'
        ]
    },
    "Deshabilitar notificaciones": {
        "ruta": r"Software\Microsoft\Windows\CurrentVersion\PushNotifications",
        "valor": "ToastEnabled",
        "tipo": winreg.REG_DWORD,
        "data": 0,
        "descripcion": "Desactiva todas las notificaciones del sistema.",
        "comandos_extra": [
            r'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Notifications\Settings" /v "NOC_GLOBAL_SETTING_TOASTS_ENABLED" /t REG_DWORD /d 0 /f',
            r'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager" /v "SubscribedContent-338393Enabled" /t REG_DWORD /d 0 /f',
            r'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager" /v "SubscribedContent-353694Enabled" /t REG_DWORD /d 0 /f',
            r'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager" /v "SubscribedContent-353696Enabled" /t REG_DWORD /d 0 /f'
        ]
    },
    "Quitar búsqueda web en barra de tareas": {
    "ruta": r"Software\Microsoft\Windows\CurrentVersion\Search",
    "valor": "BingSearchEnabled",
    "tipo": winreg.REG_DWORD,
    "data": 0,
    "descripcion": "Desactiva los resultados web en la búsqueda de la barra de tareas.",
    "registros_extra": [
        {
            "hive": winreg.HKEY_CURRENT_USER,
            "ruta": r"Software\Microsoft\Windows\CurrentVersion\Search",
            "nombre": "CortanaConsent",
            "tipo": winreg.REG_DWORD,
            "dato": 0
        }
    ]
    },


}