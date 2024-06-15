import textnode as tn


def split_nodes_delimiter(old_nodes: list[tn.TextNode], delimiter_def: dict[str, tn.TextType] = {}
                         ) -> list[tn.TextNode]:
    if len(delimiter_def.keys()) <= 0:
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
