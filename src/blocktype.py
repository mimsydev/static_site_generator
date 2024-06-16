from enum import StrEnum


class BlockType(StrEnum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block: str) -> tuple[str, BlockType]:
    def verify_ordered_list(lines: list[str]) -> bool:
        for i, line in enumerate(lines):
            if not line.startswith(f"{i+1}. "):
                return False
        return True
    if block.startswith("#") and len(block.split(" ")) > 1 and len(block.split(" ")[0]) < 7:
        return (block, BlockType.HEADING)
    elif block.startswith("```") and block.endswith("```"):
        return (block, BlockType.CODE)
    elif len(list(filter(lambda l: not l.startswith(">"), block.split("\n")))) == 0:
        return (block, BlockType.QUOTE)
    elif len(list(filter(
        lambda l: not l.startswith("* ") and not l.startswith("- ") 
        , block.split("\n")
        ))) == 0:
        return (block, BlockType.UNORDERED_LIST)
    elif verify_ordered_list(block.split("\n")):
        return (block, BlockType.ORDERED_LIST)
    else:
        return (block, BlockType.PARAGRAPH)





