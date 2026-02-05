class FrenchTranslator:
    def __init__(self):
        self.translations = {
            "filedialog.title": "Sélectionnez une icône",
            "element.close": "Fermer",
            "element.add_startup": "Ajouter au démarrage",
            "element.remove_startup": "Supprimer du démarrage",
            "element.clear": "Effacer",
            "element.open": "Ouvrir dans l'explorateur",
            "element.icon_menu": "Icône",
            "element.lang_menu": "Langue",
            "element.change_icon": "Changer",
            "element.reset_icon": "Réinitialiser",
            "tooltip.kb": "KB",
            "tooltip.mb": "MB",
            "tooltip.gb": "GB"
        }

    def filePluralize(self, count: int):
        if count == 1:
            return f"{count} fichier"
        return f"{count} fichiers"
