import ctypes
import subprocess
import time
import winreg
import psutil
from tkinter import ttk

def es_administrador():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def solicitar_administrador():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", __file__, None, None, 1)
    exit()

def reiniciar_explorer():
    try:
        subprocess.run(["taskkill", "/f", "/im", "explorer.exe"], check=True)
        time.sleep(1)
        subprocess.Popen("explorer.exe")
    except Exception as e:
        print(f"Error reiniciando explorer.exe: {str(e)}")

def verificar_estado_app(app_id):
    try:
        cmd = f"""
        $instalado = [bool](Get-AppxPackage -AllUsers *{app_id}*)
        $provisionado = [bool](Get-AppxProvisionedPackage -Online | Where-Object {{$_.PackageName -like '*{app_id}*'}})
        $instalado -or $provisionado
        """
        resultado = subprocess.run(["powershell", "-Command", cmd], 
                              capture_output=True, 
                              text=True, 
                              timeout=15,
                              creationflags=subprocess.CREATE_NO_WINDOW)
        return "True" in resultado.stdout.strip()
    except Exception:
        return False

def verificar_estado_cortana():
    try:
        clave = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                           r"SOFTWARE\Policies\Microsoft\Windows\Windows Search")
        valor, _ = winreg.QueryValueEx(clave, "AllowCortana")
        return valor == 1
    except Exception:
        return False