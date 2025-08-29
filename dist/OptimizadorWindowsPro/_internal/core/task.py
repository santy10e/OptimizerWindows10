CARACTERISTICAS_OPCIONALES = {
    "Internet-Explorer-Optional-amd64": {
        "nombre": "Internet Explorer 11",
        "seguro": True,
        "descripcion": "Navegador obsoleto. Se puede desactivar con seguridad."
    },
    "WindowsMediaPlayer": {
        "nombre": "Reproductor de Windows Media",
        "seguro": True,
        "descripcion": "Reproductor clásico. Desactívalo si usas otro."
    },
    "Xps-Viewer": {
        "nombre": "Visor de archivos XPS",
        "seguro": True,
        "descripcion": "Visualizador de archivos XPS. Muy poco usado."
    },
    "Xps-Services": {
        "nombre": "Servicios de impresión XPS",
        "seguro": True,
        "descripcion": "Servicio de impresión XPS. Innecesario para la mayoría."
    },
    "WorkFolders-Client": {
        "nombre": "Carpetas de trabajo",
        "seguro": True,
        "descripcion": "Solo útil en entornos corporativos."
    },
    "Printing-PrintToPDFServices-Features": {
    "nombre": "Microsoft Imprimir en PDF",
    "seguro": True,
    "descripcion": "Desactiva solo si no necesitas imprimir en PDF."
    },
    "FaxServicesClientPackage": {
        "nombre": "Fax y escáner de Windows",
        "seguro": True,
        "descripcion": "Innecesario si no usas fax físico ni escáner vía software de Microsoft."
    },
    "MSRDC-Infrastructure": {
        "nombre": "Compresión diferencial remota",
        "seguro": True,
        "descripcion": "Sin uso práctico en la mayoría de usuarios domésticos."
    },
    "MicrosoftWindowsPowerShellV2Root": {
        "nombre": "PowerShell 2.0 (versión antigua)",
        "seguro": True,
        "descripcion": "Versión antigua. Puede tener vulnerabilidades de seguridad."
    },
    "LegacyComponents": {
        "nombre": "Componentes heredados (DirectPlay)",
        "seguro": True,
        "descripcion": "Tecnología antigua para juegos retro. Desactiva si no usas."
    }
}


TAREAS_SEGUNDO_PLANO = {
    "Application Experience": {
        "ruta": "Microsoft\\Windows\\Application Experience",
        "seguro": True,
        "descripcion": "Envía datos sobre compatibilidad de apps. Innecesario en la mayoría de sistemas."
    },
    "Customer Experience Improvement Program": {
        "ruta": "Microsoft\\Windows\\Customer Experience Improvement Program",
        "seguro": True,
        "descripcion": "Telemetría voluntaria. Puede ser desactivado sin problema."
    },
    "DiskDiagnostic": {
        "ruta": "Microsoft\\Windows\\DiskDiagnostic",
        "seguro": True,
        "descripcion": "Analiza discos en busca de fallos. Poco útil si ya usas otras herramientas."
    },
    "Windows Defender": {
        "ruta": "Microsoft\\Windows\\Windows Defender",
        "seguro": True,
        "descripcion": "Desactívalo solo si usas un antivirus externo."
    },
    "Update Orchestrator": {
        "ruta": "Microsoft\\Windows\\UpdateOrchestrator",
        "seguro": False,
        "descripcion": "Gestiona actualizaciones de Windows. No se recomienda desactivar."
    },
    "Windows Error Reporting": {
        "ruta": "Microsoft\\Windows\\Windows Error Reporting",
        "seguro": True,
        "descripcion": "Envía reportes de errores. Desactivarlo evita envíos automáticos."
    },
    "Maps": {
        "ruta": "Microsoft\\Windows\\Maps",
        "seguro": True,
        "descripcion": "Actualiza automáticamente los mapas offline. Innecesario en la mayoría de PCs."
    },
    "Windows Feedback": {
        "ruta": "Microsoft\\Windows\\Feedback",
        "seguro": True,
        "descripcion": "Permite enviar sugerencias a Microsoft. Se puede desactivar sin consecuencias."
    }
}
