import unittest
from blocktype import BlockType, block_to_block_type
from markdowntoblocks import markdown_to_blocks, markdown_to_blocks

class TestBlocks(unittest.TestCase):
    def setUp(self) -> None:
        self.markdown_string = ("# This is my markdown\n\n"
                                "## This is a sub-header    \n\n"
                                "* this is     \n"
                                "* an unordered\n"
                                "* list\n\n"
                                "1. this\n"
                                "2. is an\n"
                                "3. ordered list\n\n"
                                "> this is a \n"
                                "> block quote\n\n"
                                "```this is a \n"
                                "code block```\n\n"
                                "I expect 3 blocks")

if __name__ == "__main__":
    markdown_text: str = ("# This is my markdown\n\n"
                            "## This is a sub-header    \n\n"
                            "* this is     \n"
                            "* an unordered\n"
                            "* list\n\n"
                            "1. this\n"
                            "2. is an\n"
                            "3. ordered list\n\n"
                            "> this is a \n"
                            "> block quote\n\n"
                            "```this is a \n"
                            "code block```\n\n"
                            "I expect 3 blocks")
    
    blocks = markdown_to_blocks(markdown_text)
    print("____________BLOCKS_______________")
    print(blocks)
    block_types = list(map(block_to_block_type, blocks))
    print("___________BLOCK TYPES__________")
    print(block_types)
