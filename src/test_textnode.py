import unittest

from textnode import TextNode, TextType
import splitnodesdelimiter as snl


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

class TextTextNodeSplit(unittest.TestCase):
    def setUp(self):
        self.node1 = TextNode("This is a **text** node", TextType.BOLD,"")
        self.node2 = TextNode("This is a text node", TextType.BOLD,"")
        self.node3 = TextNode("This is a text node", TextType.TEXT,"")
        self.node4 = TextNode("This is a `text` node", TextType.CODE,"")
        self.node_list_1 [TextNode("This is a ", TextType.TEXT),
                          TextNode("text", TextType.BOLD),
                          TextNode(" node", TextType.TEXT)]

    def bold_text(self):
        self.assertEqual(snl.split_nodes_delimiter([self.node1]), self.node_list_1)

    def bold_text_throw(self):
        with self.assertRaises(ValueError):
            snl.split_nodes_delimiter([self.node2])



if __name__ == "__main__":
    unittest.main()
