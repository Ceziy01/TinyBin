import winshell, json, os, sys, psutil
from ctypes import windll
from send2trash import send2trash
from PyQt6.QtWidgets import QApplication, QWidget, QSystemTrayIcon, QMenu, QFileDialog
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QCursor, QIcon, QPixmap, QPainter
from locales import Translator
from utils import *

class BinTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, translator):
        super().__init__(icon)
        self.translator = translator
        self.base_icon = icon
        self._pulse_icon = None
        self.anim_alphs = [1.0, 0.7, 0.4, 0.7]
        self.anim_alph_index = 0
        
        self.pulse_timer = QTimer()
        self.pulse_timer.setInterval(50)
        self.pulse_timer.timeout.connect(self.pulseStep)
        
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
        
        self.activated.connect(self.trayIconClicked)
        
    def pulseStep(self):
        if self.anim_alph_index >= len(self.anim_alphs):
            self.pulse_timer.stop()
            self.setIcon(self.base_icon)
            self.anim_alph_index = 0
            return

        pixmap = self.base_icon.pixmap(32, 32)

        if pixmap.isNull():
            return

        result = QPixmap(pixmap.size())
        result.fill(Qt.GlobalColor.transparent)

        painter = QPainter(result)
        painter.setOpacity(self.anim_alphs[self.anim_alph_index])
        painter.drawPixmap(0, 0, pixmap)
        painter.end()

        self._pulse_icon = QIcon(result)
        self.setIcon(self._pulse_icon)
        self.anim_alph_index += 1

    def pulseOnce(self):
        if self.pulse_timer.isActive():
            return
        self.anim_alph_index = 0
        self.pulse_timer.start()

    def trayIconClicked(self, reason):
        if reason == self.ActivationReason.DoubleClick:
            openBinInExplorer()

    def resetIconAction(self):
        self.changeIcon("./assets/bin.png")
        with open(settings_path, "w") as file:
            json.dump(settings, file)
        self.menu.close()
        self.setIconTheme(sysThemeIsDark())
        
    def changeIcon(self, file):
        if file:
            self.base_icon = QIcon(file)
            self.setIcon(self.base_icon)
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
            self.changeIcon(icon)
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

    def updateTooltip(self):
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

class BinDragDropWindow(QWidget):
    def __init__(self, tray: BinTrayIcon):
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
            self.tray.updateTooltip()
            
            if left_button_pressed:
                self.move(cursor_pos.x() - 15, cursor_pos.y() - 20)
                self.show()

                if not self.icon_hovered:
                    self.icon_hovered = True
        else:
            self.icon_hovered = False
            self.hide()

    def dragEnterEvent(self, event):
        mime_data = event.mimeData()
        if mime_data and mime_data.hasUrls():
            event.acceptProposedAction()
            event.setDropAction(Qt.DropAction.MoveAction)

    def dropEvent(self, event):
        mime_data = event.mimeData()
        if not(mime_data and mime_data.hasUrls()):
            return
            
        files = [os.path.normpath(url.toLocalFile()) for url in mime_data.urls()]
        
        try:
            tray.pulseOnce()
            #QApplication.processEvents()
            for file in files:
                if "minecraft_bundle" in file:
                    tray.changeIcon(os.path.join(app_dir, "assets/bundle.png"))
                send2trash(file)
        except Exception as e:
            print(f"Хуйня какая-то: {e}")
        
        self.hide()

if __name__ == "__main__":
    app_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    settings_path = os.path.join(app_dir, "settings.json")
    if not os.path.exists(settings_path):
        settings = {
            "app_name": "TinyBin",
            "version": "0.2.1",
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
    
    icon = QIcon(settings["icon_path"])
    tray = BinTrayIcon(icon, translator)
    tray.setVisible(True)
    
    window = BinDragDropWindow(tray)
    window.hide()
    
    sys.exit(app.exec())