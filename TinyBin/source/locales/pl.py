class PolishTranslator:
    def __init__(self):
        self.translations = {
            "filedialog.title": "Wybierz ikonę",
            "element.close": "Zamknij",
            "element.add_startup": "Dodaj do autostartu",
            "element.remove_startup": "Usuń z autostartu",
            "element.clear": "Wyczyść",
            "element.open": "Otwórz w eksploratorze",
            "element.icon_menu": "Ikona",
            "element.lang_menu": "Język",
            "element.change_icon": "Zmień",
            "element.reset_icon": "Resetuj",
            "tooltip.kb": "KB",
            "tooltip.mb": "MB",
            "tooltip.gb": "GB"
        }
    
    def filePluralize(self, count: int):
        if count == 1:
            return f"{count} plik"
        elif 2 <= count % 10 <= 4 and not (12 <= count % 100 <= 14):
            return f"{count} pliki"
        return f"{count} plików"
