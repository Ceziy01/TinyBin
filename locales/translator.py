from .en import EnglishTranslator
from .ru import RussianTranslator
from .be import BelarusianTranslator
from .de import GermanTranslator
from .fr import FrenchTranslator
from .it import ItalianTranslator
from .pl import PolishTranslator
from .es import SpanishTranslator
from .pt import PortugueseTranslator
from .zh import ChineseTranslator
from .ja import JapaneseTranslator
from .ko import KoreanTranslator

class Translator:
    def __init__(self, language: str):
        self.language = language
        self.translator = None
        self.loadLang(language)

    def loadLang(self, language: str):
        match language:
            case "ru": self.translator = RussianTranslator()
            case "en": self.translator = EnglishTranslator()
            case "be": self.translator = BelarusianTranslator()
            case "fr": self.translator = FrenchTranslator()
            case "de": self.translator = GermanTranslator()
            case "pl": self.translator = PolishTranslator()
            case "it": self.translator = ItalianTranslator()
            case "es": self.translator = SpanishTranslator()
            case "pt": self.translator = PortugueseTranslator()
            case "zh": self.translator = ChineseTranslator()
            case "ja": self.translator = JapaneseTranslator()
            case "ko": self.translator = KoreanTranslator()
            case _: raise ValueError(f"Language '{language}' doesnt exist")
        self.language = language

    def translate(self, key: str):
        if self.translator is None:
            raise RuntimeError("Translator err")
        return self.translator.translations.get(key)

    def filePluralize(self, count: int):
        if self.translator is None:
            raise RuntimeError("Translator err")
        return self.translator.filePluralize(count)