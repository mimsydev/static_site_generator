from collections.abc import Callable
import textnode as tn
import re

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches

def split_nodes_recursive(text: str, typed_splitters: list[tuple[str,tn.TextType]]) -> list[tuple[str, tn.TextType]]:
    def helper(text: str, 
               typed_splitters: list[tuple[str, tn.TextType]], 
               arr: list[tuple[str, tn.TextType]]) -> list[tuple[str, tn.TextType]]:
        if len(typed_splitters) == 0:
            if len(text) > 0:
                arr.append((text, tn.TextType.TEXT))
            return arr
        else:
            splitter = typed_splitters[0][0]
            text_type = typed_splitters[0][1]
            split_string = text.split(splitter)
            arr.append((split_string[0], tn.TextType.TEXT))
            arr.append((splitter, text_type))
            return helper("".join(split_string[1:]), typed_splitters[1:], arr)

    return helper(text, typed_splitters, [])

def split_nodes_wrapped(nodes: list[tn.TextNode], splitter_tuple: tuple[str, tn.TextType]):
    return_nodes: list[tn.TextNode] = []
    for node in nodes:
        splitter = splitter_tuple[0]
        text_type = splitter_tuple[1]

        if splitter in node.text:
            split_text = node.text.split(splitter)
            if len(split_text) == 2:
                raise ValueError(f"A closing tag must be provided in '{node.text}'")
            for i, text in enumerate(split_text):
                if i % 2 == 0:
                    return_nodes.append(tn.TextNode(text, tn.TextType.TEXT))
                else:
                    return_nodes.append(tn.TextNode(text, text_type))
        else:
            return_nodes.append(node)
    return return_nodes

def split_nodes_unwrapped(nodes: list[tn.TextNode], 
                          target_text_type: tn.TextType, 
                          search_pattern: str, 
                          extractor: Callable[[str],list[tuple[str,str]]]) -> list[tn.TextNode]:
    new_nodes: list[tn.TextNode] = []
    for node in nodes:
        tuples = extractor(node.text)
        if len(tuples) == 0:
            new_nodes.append(node)
        else:
            def to_split(search_tuple: tuple[str, str], target_text_type: tn.TextType) -> tuple[str, tn.TextType]:
                return (search_pattern.format(search_tuple[0], search_tuple[1]), target_text_type)

            def convert_to_node(text_tuple: tuple[str, tn.TextType], 
                                target_text_type: tn.TextType) -> tn.TextNode:
                text_type = text_tuple[1]
                text = text_tuple[0]
                if text_type != target_text_type:
                    return tn.TextNode(text, text_type)
                else:
                    result_tuple = extractor(text)
                    return tn.TextNode(result_tuple[0][0], text_type, result_tuple[0][1])

            splitters = list(map(lambda t: to_split(t, target_text_type), tuples))

            node_strings = split_nodes_recursive(node.text, splitters)
            new_nodes.extend(list(map(lambda n: convert_to_node(n, target_text_type), node_strings)))

    return new_nodes

#Takes a list of typed text nodes and returns a list of typed text nodes
def split_nodes_delimiter(old_nodes: list[tn.TextNode]) -> list[tn.TextNode]:
    new_nodes = old_nodes
    splitters = [("`", tn.TextType.CODE), ("**", tn.TextType.BOLD),
                     ("__", tn.TextType.BOLD), ("*", tn.TextType.ITALIC),
                     ("_", tn.TextType.ITALIC)]
    for splitter in splitters:
        new_nodes = split_nodes_wrapped(new_nodes, splitter)

    return new_nodes

    
def split_nodes_image(old_nodes: list[tn.TextNode]) -> list[tn.TextNode]:
    target_type = tn.TextType.IMAGE
    search_pattern = "![{0}]({1})"
    extractor = extract_markdown_images

    return split_nodes_unwrapped(old_nodes, target_type, search_pattern, extractor)


def split_nodes_link(old_nodes: list[tn.TextNode]) -> list[tn.TextNode]:
    target_type = tn.TextType.LINK
    search_pattern = "[{0}]({1})"
    extractor = extract_markdown_links

    return split_nodes_unwrapped(old_nodes, target_type, search_pattern, extractor)
