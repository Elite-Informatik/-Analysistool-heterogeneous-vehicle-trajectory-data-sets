import os
from json import dump, load


class TextProvider:
    INSTANCE = None
    PATH = 'dictionary/texts.json'

    def __init__(self, language: str):
        with open(os.path.join(os.getcwd(), self.PATH)) as json:
            self.texts = load(json)
        self.language = language

    @classmethod
    def create(cls, language: str):
        if cls.INSTANCE is not None:
            raise Exception("TextProvider is a singleton")
        cls.INSTANCE = TextProvider(language)

    @classmethod
    def get_text(cls, text: str):
        if cls.INSTANCE is None:
            raise Exception("Singelton not initialized")
        return cls.INSTANCE.texts[cls.INSTANCE.language][text]

    @classmethod
    def add_text(cls, identifyer: str, language: str, text: str):
        if cls.INSTANCE is None:
            raise Exception("Singelton not initialized")
        cls.INSTANCE.texts[language][identifyer] = text
        with open(os.path.join(os.getcwd(), cls.INSTANCE.PATH), 'w') as json:
            dump(cls.INSTANCE.texts, json, sort_keys=True, indent=3)
