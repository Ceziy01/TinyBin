class EnglishTranslator:
    def __init__(self):
        self.translations = {
            "filedialog.title": "Choose icon image",
            "element.close": "Quit",
            "element.add_startup": "Add to startup",
            "element.remove_startup": "Remove from startup",
            "element.clear": "Clear",
            "element.open": "Open in explorer",
            "element.icon_menu": "Icon",
            "element.lang_menu": "Language",
            "element.change_icon": "Change",
            "element.reset_icon": "Reset",
            "tooltip.kb": "KB",
            "tooltip.mb": "MB",
            "tooltip.gb": "GB"
        }

    def filePluralize(self, count: int):
        if count == 1:
            return f"{count} file"
        return f"{count} files"
