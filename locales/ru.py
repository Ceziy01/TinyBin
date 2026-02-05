class RussianTranslator:
    def __init__(self):
        self.translations = {
            "filedialog.title": "Выберите иконку",
            "element.close": "Закрыть",
            "element.add_startup": "Добавить в автозагрузку",
            "element.remove_startup": "Удалить из автозагрузки",
            "element.clear": "Очистить",
            "element.open": "Открыть в проводнике",
            "element.icon_menu": "Иконка",
            "element.lang_menu": "Язык",
            "element.change_icon": "Сменить",
            "element.reset_icon": "Сбросить",
            "tooltip.kb": "КБ",
            "tooltip.mb": "МБ",
            "tooltip.gb": "ГБ"
        }
    
    def filePluralize(self, count: int):
        if count % 10 == 1 and count % 100 != 11:
            return f"{count} файл"
        elif 2 <= count % 10 <= 4 and not (12 <= count % 100 <= 14):
            return f"{count} файла"
        return f"{count} файлов"