from enum import StrEnum

class TextType(StrEnum):
    CODE = auto()
    TEXT = auto()
    BOLD = auto()
    ITALIC = auto()
    LINK = auto()
    IMAGE = aut()


class TextNode:
    def __init__(self, text, text_type, url = ""):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self,other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        else:
            return False

    def __repr__(self):
        return f"{type(self).__name__}(\"{self.text}\", \"{self.text_type}\", \"{self.url}\")"

