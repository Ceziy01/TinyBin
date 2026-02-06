import winshell, json, os, sys, psutil
from ctypes import windll
from send2trash import send2trash
from PyQt6.QtWidgets import QApplication, QWidget, QSystemTrayIcon, QMenu, QFileDialog
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QCursor, QIcon
from locales import Translator
from utils import *

class TrashTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, translator):
        super().__init__(icon)
        self.translator = translator
        self.menu = QMenu(None)
        self.menu.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        
        self.exit_action = self.menu.addAction("")
        self.exit_action.triggered.connect(sys.exit)
        
        self.startup_action = self.menu.addAction("")
        self.startup_action.triggered.connect(self.startupAction)
        
        self.clear_bin = self.menu.addAction("")
        self.clear_bin.triggered.connect(clearBin)
        
        self.open_bin = self.menu.addAction("")
        self.open_bin.triggered.connect(openBinInExplorer)
        
        self.icon_menu = self.menu.addMenu("")
        self.change_icon = self.icon_menu.addAction("")
        self.change_icon.triggered.connect(self.changeIconAction)
        
        self.reset_icon = self.icon_menu.addAction("")
        self.reset_icon.triggered.connect(self.resetIconAction)
        
        self.lang_menu = self.menu.addMenu("")
        self.addLangAction("Русский", "ru")
        self.addLangAction("Беларусская", "be")
        self.addLangAction("English", "en")
        self.addLangAction("Français", "fr")
        self.addLangAction("Deutsche", "de")
        self.addLangAction("Español", "es")
        self.addLangAction("Português", "pt")
        self.addLangAction("Polski", "pl")
        self.addLangAction("Italiano", "it")
        self.addLangAction("中文", "zh")
        self.addLangAction("日本語", "ja")
        self.addLangAction("한국어", "ko")
        
        self.setContextMenu(self.menu)
        self.updateUi()
        
        self.activated.connect(self.trayiconclicked)

    def trayiconclicked(self, reason):
        if reason == self.ActivationReason.DoubleClick:
            openBinInExplorer()

    def resetIconAction(self):
        self.setIcon(QIcon("./assets/bin.png"))
        settings["icon_path"] = "./assets/bin.png"
        with open("./settings.json", "w") as file:
            json.dump(settings, file)
        self.menu.close()
        self.setIconTheme(sysThemeIsDark())
        
    def changeIcon(self, file):
        if file:
            self.setIcon(QIcon(file))
            settings["icon_path"] = file
            with open("./settings.json", "w") as file:
                json.dump(settings, file)
            

    def changeIconAction(self):
        file, _ = QFileDialog.getOpenFileName(
            self.menu, 
            self.translator.translate("filedialog.title"), 
            "", 
            "Images (*.png; *.jpg; *.jpeg; *.ico)"
        )
        self.changeIcon(file)
        self.menu.close()

    def addLangAction(self, name: str, language: str):
        self.lang_menu.addAction(name).triggered.connect(lambda: self.setLang(language))

    def startupAction(self):
        name = settings["app_name"]
        if appInStartup(name):
            removeFromStartup(name)
        else:
            addToStartup(name)
        self.updateUi()

    def setIconTheme(self, is_dark):
        if settings["icon_path"] in ["./assets/bin.png", "./assets/bin_inv.png"]:
            icon = "./assets/bin.png" if is_dark else "./assets/bin_inv.png"
            self.setIcon(QIcon(icon))
            settings["icon_path"] = icon
            with open("./settings.json", "w") as file:
                json.dump(settings, file)

    def setLang(self, language: str):
        self.translator.loadLang(language)
        self.updateUi()
        settings["lang"] = language
        with open("./settings.json", "w") as file:
            json.dump(settings, file)

    def updateUi(self):
        self.exit_action.setText(self.translator.translate("element.close"))
        if appInStartup(settings["app_name"]):
            startup_text = self.translator.translate("element.remove_startup")
        else:
            startup_text = self.translator.translate("element.add_startup")
        self.startup_action.setText(startup_text)
        
        self.clear_bin.setText(self.translator.translate("element.clear"))
        self.open_bin.setText(self.translator.translate("element.open"))
        self.change_icon.setText(self.translator.translate("element.change_icon"))
        self.reset_icon.setText(self.translator.translate("element.reset_icon"))
        self.lang_menu.setTitle(self.translator.translate("element.lang_menu"))
        self.icon_menu.setTitle(self.translator.translate("element.icon_menu"))
        
        self.menu.update()

    def setTooltip(self):
        bin_size = getBinSize()
        if bin_size < 1024:  
            size_str = f"{bin_size:.2f} {self.translator.translate("tooltip.kb")}"
        elif bin_size < 1048576:
            size_str = f"{bin_size / 1024:.2f} {self.translator.translate("tooltip.mb")}"
        else:
            size_str = f"{bin_size / 1048576:.2f} {self.translator.translate("tooltip.gb")}"
        
        file_count = len(list(winshell.recycle_bin()))
        
        tooltip_text = f"{settings["app_name"]} {settings["version"]}\nby Ceziy\n\n{size_str}\n{self.translator.filePluralize(file_count)}"
        self.setToolTip(tooltip_text)

class DragDropWindow(QWidget):
    def __init__(self, tray: TrashTrayIcon):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool | Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowOpacity(0.01)
        self.setFixedSize(30, 40)
        self.move(1015, 676)
        self.tray = tray
        self.setAcceptDrops(True)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.onMousePosition)
        self.timer.start(100)
        
        self.icon_hovered = False
        
        self.last_theme = sysThemeIsDark()

        self.theme_timer = QTimer(self)
        self.theme_timer.timeout.connect(self.checkTheme)
        self.theme_timer.start(1000)
        
    def checkTheme(self):
        current = sysThemeIsDark()
        if current != self.last_theme:
            self.last_theme = current
            tray.setIconTheme(current)

    def onMousePosition(self):
        cursor_pos = QCursor.pos()
 
        icon_rect = self.tray.geometry()
        left_button_pressed = windll.user32.GetKeyState(1) > 1
        
        if icon_rect.contains(cursor_pos):
            self.tray.setTooltip()
            
            if left_button_pressed:
                self.move(cursor_pos.x() - 15, cursor_pos.y() - 20)
                self.show()

                if not self.icon_hovered:
                    self.icon_hovered = True
        else:
            self.icon_hovered = False
            self.hide()

    def dragEnterEvent(self, event):
        if event.mimeData() and event.mimeData().hasUrls():
            event.acceptProposedAction()
            event.setDropAction(Qt.DropAction.MoveAction)

    def dropEvent(self, event):
        if event.mimeData() and event.mimeData().hasUrls():
            files = []
            for url in event.mimeData().urls():
                file_path = url.toLocalFile().replace("/", "\\")
                files.append(file_path)
            
            if files:
                try:
                    for file in files:
                        send2trash(file)
                        if "minecraft_bundle" in file: tray.changeIcon("./assets/bundle.png")
                except Exception as e:
                    print(f"Хуйня какая-то: {e}")
            
            self.hide()


if __name__ == "__main__":
    if not os.path.exists("./settings.json"):
        settings = {
            "app_name": "TinyBin",
            "version": "0.2.1",
            "lang": "en",
            "icon_path": "./assets/bin.png"
        }
        with open("./settings.json", "w") as file:
            json.dump(settings, file)
    else:
        with open("./settings.json") as file:
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
    
    icon = QIcon(settings["icon_path"])
    tray = TrashTrayIcon(icon, translator)
    tray.setVisible(True)
    
    window = DragDropWindow(tray)
    window.hide()
    
    sys.exit(app.exec())