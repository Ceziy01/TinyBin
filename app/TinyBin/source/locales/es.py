class SpanishTranslator:
    def __init__(self):
        self.translations = {
            "filedialog.title": "Seleccione un icono",
            "element.close": "Cerrar",
            "element.add_startup": "Agregar al inicio",
            "element.remove_startup": "Quitar del inicio",
            "element.clear": "Limpiar",
            "element.open": "Abrir en el explorador",
            "element.icon_menu": "Icono",
            "element.lang_menu": "Idioma",
            "element.change_icon": "Cambiar",
            "element.reset_icon": "Restablecer",
            "tooltip.kb": "KB",
            "tooltip.mb": "MB",
            "tooltip.gb": "GB"
        }

    def filePluralize(self, count: int):
        if count == 1:
            return f"{count} archivo"
        return f"{count} archivos"
