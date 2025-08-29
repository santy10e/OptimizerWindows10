# ⚡ Optimizaciones y Tweaks de Windows

Este repositorio contiene un conjunto de **scripts y configuraciones del registro de Windows** para mejorar el rendimiento, personalizar la barra de tareas y desactivar funciones innecesarias.  
El proyecto utiliza Python (`winreg`) para modificar claves de registro y también incluye comandos nativos de Windows.

---

## 📌 Requisitos

- Windows 10/11  
- Python 3.x  
- Permisos de administrador (necesarios para aplicar cambios en el registro y ejecutar algunos comandos)  

---

## 🚀 Optimizaciones Generales

El diccionario `OPTIMIZACIONES` contiene comandos útiles para mejorar el rendimiento y liberar recursos:

| Nombre | Descripción | Comando |
|--------|-------------|---------|
| **Alto Rendimiento** | Configura el plan de energía para máximo rendimiento. | `powercfg -setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c` |
| **Menú de Arranque Clásico** | Restaura el menú de arranque clásico de Windows. | `bcdedit /set {current} bootmenupolicy legacy` |
| **Deshabilitar Último Acceso** | Evita registrar la última vez que se accedió a los archivos. | `fsutil behavior set disablelastaccess 1` |
| **Deshabilitar Hibernación** | Libera espacio en disco al desactivar la hibernación. | `powercfg -h off` |
| **Limpiar Caché DNS** | Borra la caché DNS local. | `ipconfig /flushdns` |
| **Optimizar Unidades** | Desfragmenta HDD y optimiza SSD. | `defrag /C /H /V` |

---

## 🖥️ Opciones de Barra de Tareas

El diccionario `OPCIONES_BARRA_TAREAS` modifica el registro para personalizar y limpiar la barra de tareas:

| Opción | Descripción | Ruta Registro / Clave |
|--------|-------------|------------------------|
| **Noticias e Intereses** | Desactiva el widget de noticias. | `HKLM\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\HideSCANewsAndInterestsButton` |
| **Búsqueda en Barra** | Oculta la barra de búsqueda. | `HKCU\Software\Microsoft\Windows\CurrentVersion\Search\SearchboxTaskbarMode` |
| **Vista de Tareas** | Quita el botón de Vista de Tareas. | `HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced\ShowTaskViewButton` |
| **Personas** | Desactiva la barra de contactos. | `HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced\People\PeopleBand` |
| **Seguimiento de Programas** | Desactiva historial de programas y documentos recientes. | `HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced\Start_TrackProgs` |
| **Deshabilitar Notificaciones** | Apaga las notificaciones del sistema. | `HKCU\Software\Microsoft\Windows\CurrentVersion\PushNotifications\ToastEnabled` |
| **Quitar búsqueda web** | Elimina resultados web en la búsqueda. | `HKCU\Software\Microsoft\Windows\CurrentVersion\Search\BingSearchEnabled` |

> 🔧 Algunas opciones incluyen **comandos extra** o **claves adicionales** para asegurar su correcto funcionamiento.  

---

## ⚠️ Advertencia

- Algunos cambios son irreversibles sin restaurar manualmente los valores del registro.  
- Ejecuta estos scripts **bajo tu propia responsabilidad**.  
- Recomendado crear un **punto de restauración** antes de aplicar los tweaks.  

---

## ✅ Ejecución

Ejecuta el script con permisos de administrador:

```bash
python optimizaciones.py
```

Puedes recorrer los diccionarios `OPTIMIZACIONES` y `OPCIONES_BARRA_TAREAS` para aplicar los cambios que desees.
