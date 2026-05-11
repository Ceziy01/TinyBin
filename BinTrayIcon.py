import winshell, json, os, sys
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu, QFileDialog
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon, QPixmap, QPainter

from utils import *

class BinTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, translator, settings, app_dir):
        super().__init__(icon)
        self.translator = translator
        self.settings = settings
        self.app_dir = app_dir
        self.settings_path = os.path.join(app_dir, "settings.json")
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
        
        size = self.base_icon.actualSize(self.geometry().size())
        pixmap = self.base_icon.pixmap(size)
        
        if pixmap.isNull(): return

        result = QPixmap(size)
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
        self.menu.close()
        self.setIconTheme(sysThemeIsDark(), reset = True)
        
    def changeIcon(self, path):
        if not path: return
        self.base_icon = getIcon(path)
        self.setIcon(self.base_icon)

        self.settings["icon_path"] = path
        with open(self.settings_path, "w") as f:
            json.dump(self.settings, f)
            
    def changeIconAction(self):
        path, _ = QFileDialog.getOpenFileName(
            self.menu, 
            self.translator.translate("filedialog.title"), 
            "", 
            "Images (*.png; *.jpg; *.jpeg; *.ico)"
        )
        self.changeIcon(path)
        self.menu.close()

    def addLangAction(self, name: str, language: str):
        self.lang_menu.addAction(name).triggered.connect(lambda: self.setLang(language))

    def startupAction(self):
        name = self.settings["app_name"]
        if appInStartup(name):
            removeFromStartup(name)
        else:
            addToStartup(name)
        self.updateUi()

    def setIconTheme(self, is_dark, reset = False):
        if (self.settings["icon_path"] in ["./assets/bin.png", "./assets/bin_inv.png"]) or reset:
            icon = os.path.join(self.app_dir, "assets/bin.png" if is_dark else "assets/bin_inv.png")
            self.changeIcon(icon)
            self.settings["icon_path"] = icon
            with open(self.settings_path, "w") as file:
                json.dump(self.settings, file)

    def setLang(self, language: str):
        self.translator.loadLang(language)
        self.updateUi()
        self.settings["lang"] = language
        with open(self.settings_path, "w") as file:
            json.dump(self.settings, file)

    def updateUi(self):
        self.exit_action.setText(self.translator.translate("element.close"))
        if appInStartup(self.settings["app_name"]):
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
        
        tooltip_text = f"{self.settings["app_name"]} {self.settings["version"]}\nby Ceziy\n\n{size_str}\n{self.translator.filePluralize(file_count)}"
        self.setToolTip(tooltip_text)