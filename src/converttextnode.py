from textnode import TextNode, TextType
from htmlnode import LeafNode

def text_node_to_html_node(text_node):
    valid_text_types = { \
            #"type": ("tag", "self_closing", ("[v]alue[p]rops", ["prop1", "prop2", ...]))
            TextType.TEXT: ("", False, ("v", None)), \
            TextType.BOLD: ("b", False, ("v", None)), \
            TextType.ITALIC: ("i", False, ("v", None)), \
            TextType.CODE: ("code", False, ("v", None)), \
            TextType.LINK: ("a", True, ("vp", ["href"])), \
            TextType.IMAGE: ("img", True, ("p", ["alt", "src"])) \
            }

    if text_node.text_type not in valid_text_types.keys():
        text_type = text_node.text_type
        valid_types = "',".join(valid_text_types.keys())
        raise ValueError(f"The text_type '{text_type}' is not supported. The accepted text_types are '{valid_types.keys()}'.")

    text_info = valid_text_types[text_node.text_type]
    tag = text_info[0] if len(text_info[0]) > 0 else None
    self_closing = text_info[1]
    format = text_info[2][0]
    value = ""
    props = {}

    match format:
        case "v":
            value = text_node.text
        case "p":
            props[text_info[2][1][0]] = text_node.text
            props[text_info[2][1][1]] = text_node.url
        case "vp":
            value = text_node.text
            props[text_info[2][1][0]] = text_node.url
        case _:
            raise ValueError("The text type yielded an invalid value/attribute format")

    return LeafNode(value, tag, props, self_closing)
