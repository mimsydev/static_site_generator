from blocktype import Block, BlockType, block_to_block_type
from converttextnode import text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
from markdowntoblocks import markdown_to_blocks
from texttotextnodes import text_to_textnodes


def block_to_html(block: Block) -> ParentNode | None:
    block_type = block.block_type
    body = block.body
    body_lines = body.split("\n")
    if block_type == BlockType.CODE:
        body_lines = list(map(lambda l: l.strip("```"), body_lines))

    html_leaf_nodes = list(map(text_node_to_html_node, 
                              [node for node_list in 
                               list(map(text_to_textnodes, body_lines)) 
                               for node in node_list]
                              ))

    def to_list(nodes: list[HTMLNode], list_format: str) -> ParentNode:
        c_nodes: list[HTMLNode] = []
        p_node: ParentNode | None = None
        list_length = len(nodes)
        li_count = 1
        for i, node in enumerate(nodes):

            #format for list type
            if list_format == "ul":
                leader = node.value[0:1]
            elif list_format == "ol":
                leader = f"{li_count}. "
            else: 
                raise ValueError(f"The list format '{list_format}'is invalid")

            #Validate nodes
            if node == None:
                raise ValueError("This node is nothing which should never happen")
            if node.value == None:
                raise ValueError("This node value is nothing which should never happen")

            next_node = None if list_length < i + 2 else nodes[i + 1]

            # if this is a stand-alone list node, add it to the nodes list
            if (node and node.tag and node.value.startswith(leader)) \
                    and (not next_node or next_node.value.startswith(leader)):
                if p_node != None:
                    c_nodes.append(p_node)
                    p_node = None
                node.value = node.value.lstrip(leader)
                c_nodes.append(ParentNode([node], "li"))
                li_count += 1
            # if the parent node does not exist, create it
            elif node.value.startswith(leader):
                if p_node != None:
                    c_nodes.append(p_node)
                node.value = node.value.lstrip(leader)
                p_node = ParentNode([node], "li")
                li_count += 1
            else:
                p_node.children.append(node)
                if next_node == None:
                    c_nodes.append(p_node)

        return ParentNode(c_nodes, list_format)

    match block_type:
        case BlockType.PARAGRAPH:
            p_node = ParentNode(html_leaf_nodes, "p")
            return p_node

        case BlockType.HEADING:
            header_id_str = html_leaf_nodes[0].value
            if header_id_str == None:
                raise ValueError("Somthing really stupid happened with the header value....")
            header_level = header_id_str.split(" ")[0].count("#")
            html_leaf_nodes[0].value = header_id_str.lstrip("#").lstrip()
            header_node = ParentNode(html_leaf_nodes, f"h{header_level}")
            return header_node

        case BlockType.UNORDERED_LIST:
            ul_node = to_list(html_leaf_nodes, "ul")
            return ul_node

        case BlockType.ORDERED_LIST:
            ol_node = to_list(html_leaf_nodes, "ol")
            return ol_node

        case BlockType.QUOTE:
            def strip_quote(node: LeafNode):
                node.value = node.value.lstrip(">").lstrip()
                return node
            stripped_nodes = list(map(strip_quote, html_leaf_nodes))
            for i, node in enumerate(stripped_nodes):
                if i < len(stripped_nodes) - 1:
                    node.value = node.value + "\n"
            p_node = ParentNode(stripped_nodes, "blockquote")
            return p_node

        case BlockType.CODE:
            for i, node in enumerate(html_leaf_nodes):
                if i < len(html_leaf_nodes) - 1:
                    node.value = node.value + "\n"
            code_block = ParentNode([ParentNode(html_leaf_nodes, "code")], "pre")
            return code_block

        case _:
            raise ValueError(f"Unexpected block type {block_type} was encountered.")


if __name__ == "__main__":
    markdown_text: str = ("# This is my markdown\n\n"
                    "## This **is** a sub-header    \n\n"
                    "* this is     \n"
                    "* an _unordered_ bit of _list_\n"
                    "* list\n\n"
                    "I expect `3 blocks`\n\n"
                    "This is an ![inline](https://image.to.review)\n\n"
                    "> and quotes\n"
                    "> like this\n\n"
                    "``` and code\n"
                    "like this\n"
                    "```\n\n"
                    "1. [and ordered](https://this.isa.link)\n"
                    "2. lists like\n"
                    "3. this\n\n")

    mblocks = markdown_to_blocks(markdown_text)
    print("_____________MBLOCKS__________")
    print(mblocks)
    block_types = list(map(block_to_block_type, mblocks))
    print("_________________BLOCK TYPES______________")
    print(block_types)
    blocks = list(map(block_to_html, block_types))
    print("_______________BLOCKS_____________")
    for block in blocks:
        print(block.to_html())





