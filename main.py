import json, os, sys, psutil
from PyQt6.QtWidgets import QApplication
from BinDragDropWindow import BinDragDropWindow
from BinTrayIcon import BinTrayIcon
from locales import Translator
from utils import *

if __name__ == "__main__":
    app_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    settings_path = os.path.join(app_dir, "settings.json")
    if not os.path.exists(settings_path):
        settings = {
            "app_name": "TinyBin",
            "version": "0.2.2",
            "lang": "en",
            "icon_path": os.path.join(app_dir, "assets/bin.png")
        }
        with open(settings_path, "w") as file:
            json.dump(settings, file)
    else:
        with open(settings_path) as file:
            settings = json.load(file)
    
    process_name = f"{settings["app_name"]}.exe"
    running_processes = []
    
    for proc in psutil.process_iter(["name"]):
        try:
            if proc.info["name"] == process_name:
                running_processes.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    if len(running_processes) > 1:
        sys.exit()
    
    os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
    
    translator = Translator(settings["lang"])
    app = QApplication(sys.argv)

    icon = getIcon(settings["icon_path"])
    tray = BinTrayIcon(icon, translator, settings, app_dir)
    tray.setVisible(True)
    
    window = BinDragDropWindow(tray, app_dir)
    window.hide()
    
    sys.exit(app.exec())