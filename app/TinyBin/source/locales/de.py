class GermanTranslator:
    def __init__(self):
        self.translations = {
            "filedialog.title": "Wählen Sie ein Symbol",
            "element.close": "Schließen",
            "element.add_startup": "Zum Autostart hinzufügen",
            "element.remove_startup": "Vom Autostart entfernen",
            "element.clear": "Leeren",
            "element.open": "Im Explorer öffnen",
            "element.icon_menu": "Symbol",
            "element.lang_menu": "Sprache",
            "element.change_icon": "Ändern",
            "element.reset_icon": "Zurücksetzen",
            "tooltip.kb": "KB",
            "tooltip.mb": "MB",
            "tooltip.gb": "GB"
        }

    def filePluralize(self, count: int):
        if count == 1:
            return f"{count} Datei"
        return f"{count} Dateien"
