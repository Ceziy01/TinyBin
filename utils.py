import ctypes, winreg, os, sys, winshell, subprocess
from ctypes import wintypes

class BinInfo(ctypes.Structure):
    _fields_ = [
        ('cbSize', wintypes.DWORD),
        ('i64Size', ctypes.c_longlong),
        ('i64NumItems', ctypes.c_longlong),
    ]
    
def sysThemeIsDark():
    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
    )
    value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
    return value == 0
    
def appInStartup(name:str):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_READ)
        _, _ = winreg.QueryValueEx(key, name)
        winreg.CloseKey(key)
        return True
    except FileNotFoundError:
        return False
    
def addToStartup(name:str):
    path = f"{os.path.dirname(os.path.abspath(sys.argv[0]))}\\{name}.exe"
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, name, 0, winreg.REG_SZ, path)
    winreg.CloseKey(key)

def removeFromStartup(name:str):
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
    winreg.DeleteValue(key, name)
    winreg.CloseKey(key)

def getBinSize():
    bin_info = BinInfo()
    bin_info.cbSize = ctypes.sizeof(BinInfo)
    ctypes.windll.shell32.SHQueryRecycleBinW(None, ctypes.byref(bin_info))
    return (bin_info.i64Size) / 1024

def openBinInExplorer():
    #os.system("start shell:RecycleBinFolder -WindowStyle Hidden")
    subprocess.Popen(
        ["explorer", "shell:RecycleBinFolder"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        shell=False
    )
    
def clearBin():
    bin = winshell.recycle_bin()
    if list(bin):
        bin.empty()