from enum import StrEnum

class TextType(StrEnum):
    CODE = "code"
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType , url = ""):
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

