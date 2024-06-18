from blocktohtml import block_to_html, markdown_to_blocks
from blocktype import block_to_block_type
from htmlnode import ParentNode 

def markdown_to_html_node(markdown: str) -> list[ParentNode | None]:
    return list(map(block_to_html,
             list(map(block_to_block_type, markdown_to_blocks(markdown)))
             ))

