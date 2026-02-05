class BelarusianTranslator:
    def __init__(self):
        self.translations = {
            "filedialog.title": "Выберыце значок",
            "element.close": "Зачыніць",
            "element.add_startup": "Дадаць у аўтазагрузку",
            "element.remove_startup": "Выдаліць з аўтазагрузкі",
            "element.clear": "Ачысціць",
            "element.open": "Адкрыць у правадыры",
            "element.icon_menu": "Значок",
            "element.lang_menu": "Мова",
            "element.change_icon": "Змяніць",
            "element.reset_icon": "Скід",
            "tooltip.kb": "КБ",
            "tooltip.mb": "МБ",
            "tooltip.gb": "ГБ"
        }
    
    def filePluralize(self, count: int):
        if count % 10 == 1 and count % 100 != 11:
            return f"{count} файл"
        elif 2 <= count % 10 <= 4 and not (12 <= count % 100 <= 14):
            return f"{count} файлы"
        else:
            return f"{count} файлаў"
