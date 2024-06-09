import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def setUp(self):
        self.child_node = HTMLNode("p", "Test child", None, {"class": "body_p", "id": "test_text"})
        self.button_disabled = HTMLNode("button", "Submit", None, {"type": "submit", "disabled":""})
        self.div = HTMLNode("div", None, [self.child_node], {"class": "container"})
        self.button_string = " type=\"submit\" disabled"
        self.child_string = " class=\"body_p\" id=\"test_text\""
        self.print_div = "HTMLNode(\'div\', \'None\', \'HTMLNode(\'p\', \'Test child\', \'None\', \' class=\"body_p\" id=\"test_text\"\')\', \' class=\"container\"\')"

    def test_to_html(self):
        with self.assertRaises(NotImplementedError):
            self.div.to_html()

    def test_prop_to_html_child(self):
        child_string_test = self.child_node.props_to_html()
        print(child_string_test)
        self.assertEqual(child_string_test, self.child_string)

    def test_prop_to_html_button(self):
        button_string_test = self.button_disabled.props_to_html()
        self.assertEqual(button_string_test, self.button_string)

    def test_print(self):
        self.assertEqual(self.div.__repr__(), self.print_div)


if __name__ == "__main__":
    unittest.main()
