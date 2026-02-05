class ItalianTranslator:
    def __init__(self):
        self.translations = {
            "filedialog.title": "Seleziona un'icona",
            "element.close": "Chiudi",
            "element.add_startup": "Aggiungi all'avvio",
            "element.remove_startup": "Rimuovi dall'avvio",
            "element.clear": "Pulisci",
            "element.open": "Apri in Esplora file",
            "element.icon_menu": "Icona",
            "element.lang_menu": "Lingua",
            "element.change_icon": "Cambia",
            "element.reset_icon": "Reimposta",
            "tooltip.kb": "KB",
            "tooltip.mb": "MB",
            "tooltip.gb": "GB"
        }

    def filePluralize(self, count: int):
        return f"{count} file"
