class ChineseTranslator:
    def __init__(self):
        self.translations = {
            "filedialog.title": "选择图标",
            "element.close": "关闭",
            "element.add_startup": "添加到启动项",
            "element.remove_startup": "从启动项中移除",
            "element.clear": "清除",
            "element.open": "在资源管理器中打开",
            "element.icon_menu": "图标",
            "element.lang_menu": "语言",
            "element.change_icon": "更改",
            "element.reset_icon": "重置",
            "tooltip.kb": "KB",
            "tooltip.mb": "MB",
            "tooltip.gb": "GB"
        }
    
    def filePluralize(self, count: int):
        return f"{count} 个文件"