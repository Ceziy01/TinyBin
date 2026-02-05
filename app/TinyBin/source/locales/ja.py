class JapaneseTranslator:
    def __init__(self):
        self.translations = {
            "filedialog.title": "アイコンを選択",
            "element.close": "閉じる",
            "element.add_startup": "スタートアップに追加",
            "element.remove_startup": "スタートアップから削除",
            "element.clear": "クリア",
            "element.open": "エクスプローラーで開く",
            "element.icon_menu": "アイコン",
            "element.lang_menu": "言語",
            "element.change_icon": "変更",
            "element.reset_icon": "リセット",
            "tooltip.kb": "KB",
            "tooltip.mb": "MB",
            "tooltip.gb": "GB"
        }
    
    def filePluralize(self, count: int):
        return f"{count} 個のファイル"