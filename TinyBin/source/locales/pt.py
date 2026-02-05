class PortugueseTranslator:
    def __init__(self):
        self.translations = {
            "filedialog.title": "Selecione um ícone",
            "element.close": "Fechar",
            "element.add_startup": "Adicionar à inicialização",
            "element.remove_startup": "Remover da inicialização",
            "element.clear": "Limpar",
            "element.open": "Abrir no explorador",
            "element.icon_menu": "Ícone",
            "element.lang_menu": "Idioma",
            "element.change_icon": "Alterar",
            "element.reset_icon": "Redefinir",
            "tooltip.kb": "KB",
            "tooltip.mb": "MB",
            "tooltip.gb": "GB"
        }

    def filePluralize(self, count: int):
        if count == 1:
            return f"{count} arquivo"
        return f"{count} arquivos"
