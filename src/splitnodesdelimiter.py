import textnode as tn
import re

#Takes a list of typed text nodes and returns a list of typed text nodes
def split_nodes_delimiter(old_nodes: list[tn.TextNode]) -> list[tn.TextNode]:
    delimiter_def = {"```": tn.TextType.CODE, "`": tn.TextType.CODE,
                     "**": tn.TextType.BOLD, "__": tn.TextType.BOLD,
                     "*": tn.TextType.ITALIC, "_": tn.TextType.ITALIC
                     }
    new_nodes: list[tn.TextNode] = []
    # We want to take each old node, check its type, and split it out into new nodes as appropriate based on
    # its type
    for node in old_nodes:
        if node.text_type != tn.TextType.TEXT:
            new_nodes.append(node)
        else:
            for i,(delimiter, text_type) in enumerate(delimiter_def.items()):
                if delimiter in node.text:
                    split_node_text = node.text.split(delimiter)
                    if len(split_node_text) == 2:
                        raise ValueError(f"There was no closing tag in '{node.text}'. This is invalid syntax.")
                    for i, text in enumerate(split_node_text):
                        if len(text) == 0:
                            continue
                        if i % 2 != 0:
                            new_nodes.append(tn.TextNode(text, tn.TextType.TEXT))
                        else:
                            new_nodes.append(tn.TextNode(text, text_type))
                    break
                elif i >= len(delimiter_def.items()):
                    raise ValueError(f"There was not matching delimiter found for text_type '{node.text_type}' in '{node.text}'.")
                else:
                    continue
    return new_nodes

def split_recursive(text: str, splitters: list[str], text_type: tn.TextType) -> list[tuple[str, tn.TextType]]:
    def helper(text: str, splitters: list[str], arr: list[tuple[str, tn.TextType]]) -> list[tuple[str, tn.TextType]]:
        if len(splitters) == 0:
            if len(text) > 0:
                arr.append((text, tn.TextType.TEXT))
            return arr
        else:
            split_string = text.split(splitters[0])
            arr.append((split_string[0], tn.TextType.TEXT))
            arr.append((splitters[0], text_type))
            return helper("".join(split_string[1:]), splitters[1:], arr)
    
    return helper(text, splitters, [])
    
def split_nodes_image(old_nodes: list[tn.TextNode]) -> list[tn.TextNode]:
    new_nodes: list[tn.TextNode] = []
    for node in old_nodes:
        image_tuples = extract_markdown_images(node.text)
        if len(image_tuples) == 0:
            new_nodes.append(node)
        else:
            def image_to_split(image_tuple: tuple[str, str]) -> str:
                return f"![{image_tuple[0]}]({image_tuple[1]})"

            def convert_to_node_image(text_tuple: tuple[str, tn.TextType]) -> tn.TextNode:
                text_type = text_tuple[1]
                text = text_tuple[0]
                if text_type == tn.TextType.TEXT:
                    return tn.TextNode(text, text_type)
                elif text_type == tn.TextType.IMAGE:
                    image_tuple = extract_markdown_images(text)
                    return tn.TextNode(image_tuple[0][0], text_type, image_tuple[0][1])
                else:
                    raise ValueError(f"Text type {text_type} is not handled by image conversion")

            splitters = list(map(image_to_split, image_tuples))

            node_strings = split_recursive(node.text, splitters, tn.TextType.IMAGE)
            new_nodes.extend(list(map(convert_to_node_image, node_strings)))

    return new_nodes

def split_nodes_link(old_nodes: list[tn.TextNode]) -> list[tn.TextNode]:
    new_nodes: list[tn.TextNode] = []
    for node in old_nodes:
        link_tuples = extract_markdown_links(node.text)
        if len(link_tuples) == 0:
            new_nodes.append(node)
        else:
            def link_to_split(link_tuple: tuple[str, str]) -> str:
                return f"[{link_tuple[0]}]({link_tuple[1]})"

            def convert_to_node_link(text_tuple: tuple[str, tn.TextType]) -> tn.TextNode:
                text_type = text_tuple[1]
                text = text_tuple[0]
                if text_type == tn.TextType.TEXT:
                    return tn.TextNode(text, text_type)
                elif text_type == tn.TextType.LINK:
                    link_tuple = extract_markdown_links(text)
                    return tn.TextNode(link_tuple[0][0], text_type, link_tuple[0][1])
                else:
                    raise ValueError(f"Text type {text_type} is not handled by link conversion")

            splitters = list(map(link_to_split, link_tuples))

            node_strings = split_recursive(node.text, splitters, tn.TextType.LINK)
            print("NODE STINGS")
            print(node_strings)
            new_nodes.extend(list(map(convert_to_node_link, node_strings)))

    return new_nodes

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches
    
def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches
