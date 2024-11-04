import winshell, json, os, sys, ctypes, winreg
from ctypes import windll, wintypes
from send2trash import send2trash
from PyQt6.QtWidgets import QApplication, QWidget, QSystemTrayIcon, QMenu, QFileDialog
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QCursor, QIcon

def initFile(path, content, mode = "w"):
    if not os.path.exists(path):
        if "b" in mode:
            with open(path, mode) as file:
                file.write(content)
        else:
            with open(path, mode, encoding = "utf-8") as file:
                file.write(content)

def genAssets():
    icon_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00 \x00\x00\x00 \x08\x06\x00\x00\x00szz\xf4\x00\x00\x00\x01sRGB\x00\xae\xce\x1c\xe9\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00\tpHYs\x00\x00\x0e\xc4\x00\x00\x0e\xc4\x01\x95+\x0e\x1b\x00\x00\x00\x96IDATXG\xed\x97\xe1\n\x80 \x0c\x84\xb5\xf7\x7f\x83\xfe\xf5\xa2V0\xa1\xc8\xdb\xa6\x19k\xb0\x0fb?\xd6\xf28\xaf\xc2\\JI\x96,T\xcd\xe8u@{s\xa6*\xe2\xce\x81\xe9\xb4\x04|\xad\xe8\xb6=\xbf\xde\x82\xdaP\x07\n\xc0>\xc7\xdc\x81\x10\xe0N\xc0z\\(\xb5\\\x0f\xd2\xfb\x16p\x89F=n&2\x10\x02B@\x08\xf0\'\xa0\xf95#\xb8\x1ed\xc4\x81\xa9""\x03\x1a\x01\xf0w\xa9\xa0\xcenT\x1fH\xe7\x827\x8b_\x81\xd9\x90\x1c8\x07\x87\xd2M\x88\xf3\xe6\'#\xe3\x10\xa6\xb4\x03\xef\xb0&\xfd[z\x16\xee\x00\x00\x00\x00IEND\xaeB`\x82'
    inv_icon_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00 \x00\x00\x00 \x08\x06\x00\x00\x00szz\xf4\x00\x00\x00\x01sRGB\x00\xae\xce\x1c\xe9\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00\tpHYs\x00\x00\x0e\xc4\x00\x00\x0e\xc4\x01\x95+\x0e\x1b\x00\x00\x00\x8aIDATXG\xed\x96\xe1\n\x80 \x0c\x84\xad\xf7\x7f\x83\xfe\xf5\xa2e1\xa1h\x9bs\t%\xbb\x0fd\xa0\xe8\x8e\xf3@Sx&\xaaV6\xaa5\xcc\xe7\xceT\xe3\xc2Ye\xb5\xd9\xcb\xad\xe7\xaf\xaf\xe0p\xa2\x87\x1b\xea9\x9f;\x00\x01\xc3\tX\xf2\x90\x02\xa5\xad\xb9\xe0\xd2\xcb\xcd\x15\xa45m\x0f2\x00\x01\x10\x00\x01\xe3\t\xd0>\x9b\xad\x1f\xdc\x13\x8f\x03]E \x03\x16\x01\xe2Kf\xa0\xec]\xa9>\xa8\xdd\xd9\x9b\xe6W\xc4>\xd6\xd0x\x854\x872\x1a)\xed\x08\xcc\x15\xfb;\x9bb\x84\x00\x00\x00\x00IEND\xaeB`\x82'
    settings_data = "{\"app_name\": \"TinyBin\", \"icon_path\":\"./bin.png\", \"version\": \"v0.1.2\", \"lang\": \"./eng.json\"}"
    rus_data = "{\"filedialog.title\": \"Выберите иконку\", \"element.close\": \"Закрыть\", \"element.add_startup\": \"Добавить в автозагрузку\", \"element.remove_startup\": \"Удалить из автозагрузки\", \"element.clear\": \"Очистить\", \"element.open\": \"Открыть в проводнике\", \"element.icon_menu\": \"Иконка\", \"element.lang_menu\": \"Язык\", \"element.change_icon\": \"Сменить\", \"element.reset_icon\": \"Сбросить\", \"tooltip.kb\": \"КБ\", \"tooltip.mb\": \"МБ\", \"tooltip.gb\": \"ГБ\", \"tooltip.f1\": \"файл\", \"tooltip.f2\": \"файла\", \"tooltip.f3\": \"файлов\"}"
    eng_data = "{\"filedialog.title\": \"Choose icon image\", \"element.close\": \"Quit\", \"element.add_startup\": \"Add to startup\", \"element.remove_startup\": \"Remove from stratup\", \"element.clear\": \"Clear\", \"element.open\": \"Open in explorer\", \"element.icon_menu\": \"Icon\", \"element.lang_menu\": \"Language\", \"element.change_icon\": \"Change\", \"element.reset_icon\": \"Reset\", \"tooltip.kb\": \"KB\", \"tooltip.mb\": \"MB\", \"tooltip.gb\": \"GB\", \"tooltip.f1\": \"files\", \"tooltip.f2\": \"files\", \"tooltip.f3\": \"files\"}"
    initFile("./bin.png", icon_data, "wb")
    initFile("./bin_inv.png", inv_icon_data, "wb")
    initFile("./settings.json", settings_data)
    initFile("./rus.json", rus_data)
    initFile("./eng.json", eng_data)

def sysThemeIsDark():
    registry = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
    value, _ = winreg.QueryValueEx(registry, "AppsUseLightTheme")
    return value == 0

def translatable(key:str):
    try: return translation[key]
    except: return "wrong key"

class BinInfo(ctypes.Structure):
    _fields_ = [
        ('cbSize', wintypes.DWORD),
        ('i64Size', ctypes.c_longlong),
        ('i64NumItems', ctypes.c_longlong),
    ]

class TrashTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        super().__init__(icon, parent)
        self.parent = parent
        self.menu = QMenu(parent)
        self.menu.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.exit_action = self.menu.addAction(translatable("element.close"))
        self.exit_action.triggered.connect(sys.exit)
        self.startup_action = self.menu.addAction(translatable("element.remove_startup" if self.isInStartup(settings["app_name"]) else "element.add_startup"))
        self.startup_action.triggered.connect(self.startupAction)
        self.clear_bin = self.menu.addAction(translatable("element.clear"))
        self.clear_bin.triggered.connect(self.clearBin)
        self.open_bin = self.menu.addAction(translatable("element.open"))
        self.open_bin.triggered.connect(lambda: os.system("start shell:RecycleBinFolder"))
        self.icon_menu = self.menu.addMenu(translatable("element.icon_menu"))
        self.change_icon = self.icon_menu.addAction(translatable("element.change_icon"))
        self.change_icon.triggered.connect(self.changeIcon)
        self.reset_icon = self.icon_menu.addAction(translatable("element.reset_icon"))
        self.reset_icon.triggered.connect(self.resetIcon)
        self.lang_menu = self.menu.addMenu(translatable("element.lang_menu"))
        self.rus_lang = self.lang_menu.addAction("Русский")
        self.rus_lang.triggered.connect(lambda: self.setLang("./rus.json"))
        self.eng_lang = self.lang_menu.addAction("English")
        self.eng_lang.triggered.connect(lambda: self.setLang("./eng.json"))
        self.tooltip_timer = QTimer(self)
        self.tooltip_timer.timeout.connect(self.formatTooltip)
        self.tooltip_timer.start(100)
        self.theme_timer = QTimer(self)
        self.theme_timer.timeout.connect(self.setIconTheme)
        self.theme_timer.start(100)
        self.setContextMenu(self.menu)
    
    def startupAction(self):
        if self.isInStartup(settings["app_name"]):
            self.removeFromStartup(settings["app_name"])
            self.startup_action.setText(translatable("element.add_startup"))
        else:
            self.addToStartup(settings["app_name"])
            self.startup_action.setText(translatable("element.remove_startup"))
        self.menu.update()
        
    def isInStartup(self, name):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_READ)
            value, regtype = winreg.QueryValueEx(key, name)
            winreg.CloseKey(key)
            return True
        except FileNotFoundError:
            return False
        
    def addToStartup(self, name):
        path = f"{os.path.dirname(os.path.abspath(sys.argv[0]))}\\{settings["app_name"]}.exe"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, name, 0, winreg.REG_SZ, path)
        winreg.CloseKey(key)
    
    def removeFromStartup(self, name):
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, name)
        winreg.CloseKey(key)
    
    def setIconTheme(self):
        if settings["icon_path"] in ["./bin.png", "./bin_inv.png"]:
            icon = "./bin.png" if sysThemeIsDark() else "./bin_inv.png"
            self.setIcon(QIcon(icon))                
            settings["icon_path"] = icon
            with open("./settings.json", "w") as file:
                json.dump(settings, file)
                
    def setLang(self, file): 
        settings["lang"] = file
        with open("./settings.json", "w") as file:
            json.dump(settings, file)
        with open(settings["lang"], "r+", encoding = "UTF-8") as file:
            global translation
            translation = json.load(file)
        self.exit_action.setText(translatable("element.close"))
        self.startup_action.setText(translatable("element.remove_startup" if self.isInStartup(settings["app_name"]) else "element.add_startup"))
        self.clear_bin.setText(translatable("element.clear"))
        self.open_bin.setText(translatable("element.open"))
        self.icon_menu.setTitle(translatable("element.icon_menu"))
        self.change_icon.setText(translatable("element.change_icon"))
        self.reset_icon.setText(translatable("element.reset_icon"))
        self.lang_menu.setTitle(translatable("element.lang_menu"))
        self.menu.update()
        self.menu.close()
        
    def formatTooltip(self):
        bin_size = self.getBinSize()
        if bin_size < float(1024):
            bin_size = f"{bin_size:.2f} {translatable("tooltip.kb")}"
        elif bin_size >= 1024 and bin_size < (1024 ** 2):
            bin_size = f"{bin_size / 1024:.2f} {translatable("tooltip.mb")}"
        else:
            bin_size = f"{bin_size / (1024 ** 2):.2f} {translatable("tooltip.gb")}"
    
        file_count = len(list(winshell.recycle_bin()))
        file_word = self.getWordForm(file_count, translatable("tooltip.f1"), translatable("tooltip.f2"), translatable("tooltip.f3")) 
        self.setToolTip(f"{settings["app_name"]} {settings["version"]}\nby Ceziy\n\n{bin_size}\n{file_count} {file_word}")
      
    def getWordForm(self, n, f1, f2, f3):
        n %= 100
        n1 = n % 10
        if n >= 10 and n <= 20:
            return f3
        elif n1 >= 1 and n1 <= 4:
            if n1 == 1:
                return f1
            return f2
        return f3   
    
    def getBinSize(self):
        bin_info = BinInfo()
        bin_info.cbSize = ctypes.sizeof(BinInfo)
        ctypes.windll.shell32.SHQueryRecycleBinW(None, ctypes.byref(bin_info))
        return (bin_info.i64Size) / 1024
    
    def resetIcon(self):
        self.setIcon(QIcon("./bin.png"))
        settings["icon_path"] = "./bin.png"
        with open("./settings.json", "w") as file:
            json.dump(settings, file)
        self.menu.close()
    
    def changeIcon(self):
        file, _ = QFileDialog.getOpenFileName(self.menu, translatable("filedialog.title"), "", "Images (*.png; *.jpg; *.jpeg; *.ico)")
        if file:
            self.setIcon(QIcon(file))
            settings["icon_path"] = file
            with open("./settings.json", "w") as file:
                json.dump(settings, file)
        self.menu.close()
            
    def clearBin(self):
        if len(list(winshell.recycle_bin())) != 0:
            winshell.recycle_bin().empty()
        self.menu.close()
        
class DragDropWindow(QWidget):
    def __init__(self, tray):
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

    def onMousePosition(self):
        cursor_pos = QCursor.pos()
        cx = cursor_pos.x()
        cy = cursor_pos.y()
        self.icon_rect = tray.geometry().getRect()
        self.menu_rect = tray.menu.geometry().getRect()
        self.lang_menu_rect = tray.lang_menu.geometry().getRect()
        x1 = self.icon_rect[0]
        y1 = self.icon_rect[1]
        x2 = x1 + self.icon_rect[2]
        y2 = y1 + self.icon_rect[3]
        tray.menu.move(self.menu_rect[0], y1 - self.menu_rect[3])
        tray.lang_menu.move(self.lang_menu_rect[0], y1 - self.lang_menu_rect[3])
        if cx >= x1 and cx <= x2 and cy >= y1 and cy <= y2 and windll.user32.GetKeyState(0x01) > 1:
            self.move(x1, y1)
            self.show()
        else:
            self.hide()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            event.setDropAction(Qt.DropAction.MoveAction)
    
    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            files = [i.toLocalFile().replace("/", "\\") for i in event.mimeData().urls()]
            send2trash(files)
            self.hide()

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
    genAssets()
    with open("./settings.json") as file:
        settings = json.load(file)
    with open(settings["lang"], "r+", encoding = "UTF-8") as file:
        translation = json.load(file)
    app = QApplication(sys.argv)
    icon = QIcon(settings["icon_path"]) 
    tray = TrashTrayIcon(icon)
    tray.setVisible(True)
    window = DragDropWindow(tray)
    window.show()
    sys.exit(app.exec())