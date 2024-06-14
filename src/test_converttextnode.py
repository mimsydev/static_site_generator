import unittest
from textnode import TextNode, TextType
from converttextnode import text_node_to_html_node

class TestConvertTextNode(unittest.TestCase):
    def setUp(self):
        self.text_type_text = TextNode("This is some raw text", TextType.TEXT)
        self.text_type_bold = TextNode("This is some bold text", TextType.BOLD)
        self.text_type_italic = TextNode("This is some italic text", TextType.ITALIC)
        self.text_type_code = TextNode("This is some code text", TextType.CODE)
        self.text_type_link = TextNode("This is a link",TextType.LINK, "https://localhost:8888")
        self.text_type_image = TextNode("This is some alt text", TextType.IMAGE, "https://localhost:8888")
        self.expected_text = "This is some raw text"
        self.expected_bold = "<b>This is some bold text</b>"
        self.expected_italic = "<i>This is some italic text</i>"
        self.expected_code = "<code>This is some code text</code>"
        self.expected_link = "<a href=\"https://localhost:8888\">This is a link</a>"
        self.expected_image = "<img alt=\"This is some alt text\" src=\"https://localhost:8888\">"

    def test_text(self):
        self.assertEqual(text_node_to_html_node(self.text_type_text).to_html(), self.expected_text)

    def test_bold(self):
        self.assertEqual(text_node_to_html_node(self.text_type_bold).to_html(), self.expected_bold)

    def test_italic(self):
        self.assertEqual(text_node_to_html_node(self.text_type_italic).to_html(), self.expected_italic)

    def test_code(self):
        self.assertEqual(text_node_to_html_node(self.text_type_code).to_html(), self.expected_code)

    def test_link(self):
        self.assertEqual(text_node_to_html_node(self.text_type_link).to_html(), self.expected_link)

    def test_image(self):
        self.assertEqual(text_node_to_html_node(self.text_type_image).to_html(), self.expected_image)
