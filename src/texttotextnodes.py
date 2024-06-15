from textnode import TextNode, TextType
import splitnodesdelimiter as snl

def text_to_textnodes(text: str) -> list[TextNode]:
    node = [TextNode(text, TextType.TEXT)]
    return snl.split_nodes_delimiter(snl.split_nodes_link(snl.split_nodes_image(node)))


