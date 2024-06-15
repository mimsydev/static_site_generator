from textnode import TextNode, TextType
import unittest
from texttotextnodes import text_to_textnodes

class TestTTT(unittest.TestCase):
    def setUp(self) -> None:
        self.test_text="This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev) and another ![otherimage](https://other.image.com)"
        self.text_nodes= [ TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, 
                         "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("otherimage", TextType.IMAGE, "https://other.image.com"),
            ]

    def test_ttt(self) -> None:
        self.assertEqual(text_to_textnodes(self.test_text), self.text_nodes)
