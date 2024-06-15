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

class TextImageSplit(unittest.TestCase):
    def setUp(self):
        self.image_str_1: TextNode = TextNode("This is an ![image](https://go.here.now) and another ![image](https://or.maybe.here) and more text", TextType.TEXT)
        self.image_str_2: TextNode = TextNode("This is an ![image](https://go.here.nowagain) and another ![image](https://or.maybe.hereagain) and more text", TextType.TEXT)
        self.text_str_1: TextNode = TextNode("Not an image", TextType.TEXT)
        self.link_str_1: TextNode = TextNode("This is a [link](https://go.heere.now) and another [link](https://or.maybe.here)", TextType.TEXT)

        self.node_list_img: list[TextNode] = [self.image_str_1, self.image_str_2, self.text_str_1]
        self.node_list_link: list[TextNode] = [self.text_str_1, self.link_str_1]
        self.result_list_image: list[TextNode] = [TextNode("This is an ", TextType.TEXT, ""), 
                                               TextNode("image", TextType.IMAGE, "https://go.here.now"), 
                                               TextNode(" and another ", TextType.TEXT, ""), 
                                               TextNode("image", TextType.IMAGE, "https://or.maybe.here"), 
                                               TextNode(" and more text", TextType.TEXT, ""), 
                                               TextNode("This is an ", TextType.TEXT, ""), 
                                               TextNode("image", TextType.IMAGE, "https://go.here.nowagain"), 
                                               TextNode(" and another ", TextType.TEXT, ""), 
                                               TextNode("image", TextType.IMAGE, "https://or.maybe.hereagain"), 
                                               TextNode(" and more text", TextType.TEXT, ""),
                                               TextNode("Not an image", TextType.TEXT, "")]
        self.result_list_link: list[TextNode] = [TextNode("Not an image", TextType.TEXT, ""), 
                                                 TextNode("This is a ", TextType.TEXT, ""), 
                                                 TextNode("link", TextType.LINK, "https://go.heere.now"), 
                                                 TextNode(" and another ", TextType.TEXT, ""), 
                                                 TextNode("link", TextType.LINK, "https://or.maybe.here")]

    def test_image(self):
        self.maxDiff = None
        self.assertEqual(snl.split_nodes_image(self.node_list_img), self.result_list_image)

    def test_link(self):
        self.maxDiff = None
        self.assertEqual(snl.split_nodes_link(self.node_list_link), self.result_list_link)




if __name__ == "__main__":
    unittest.main()
