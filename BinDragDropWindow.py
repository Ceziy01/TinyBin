import os
from ctypes import windll
from send2trash import send2trash
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QCursor

from BinTrayIcon import BinTrayIcon
from utils import *

class BinDragDropWindow(QWidget):
    def __init__(self, tray: BinTrayIcon, app_dir: str):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool | Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowOpacity(0.01)
        self.setFixedSize(30, 40)
        self.move(1015, 676)
        self.tray = tray
        self.app_dir = app_dir
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
            self.tray.setIconTheme(current)

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
            self.tray.pulseOnce()
            #QApplication.processEvents()
            for file in files:
                if "minecraft_bundle" in file:
                    self.tray.changeIcon(os.path.join(self.app_dir, "assets/bundle.png"))
                send2trash(file)
        except Exception as e:
            print(f"Хуйня какая-то: {e}")
        
        self.hide()