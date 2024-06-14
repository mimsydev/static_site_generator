import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def setUp(self):
        self.node1 = TextNode("This is a text node", TextType.BOLD,"")
        self.node2 = TextNode("This is a text node", TextType.BOLD,"")
        self.node3 = TextNode("This is a second node", TextType.ITALIC, "https://www.mimsydev.com")
        self.node3_printed = "TextNode(\"This is a second node\", \"italic\", \"https://www.mimsydev.com\")"


    def test_eq(self):
        self.assertEqual(self.node1, self.node2)

    def test_not_eq(self):
        self.assertNotEqual(self.node1, self.node3)

    def test_print(self):
        self.assertEqual(self.node3.__repr__(),self.node3_printed) 


if __name__ == "__main__":
    unittest.main()
