def markdown_to_blocks(text: str) -> list[str]:
    string_blocks: list[str] = []
    split_text = text.split("\n")
    block: list[str] = []
    for i, split in enumerate(split_text):
        clean_split = split.strip()
        if len(clean_split) > 1:
            block.append(clean_split)
        elif i < len(split_text) -1:
            string_blocks.append("\n".join(block))
            block = []
        else:
            block = []

    return string_blocks

if __name__ == "__main__":

    markdown_text: str = ("# This is my markdown\n\n"
                    "## This is a sub-header    \n\n"
                    "* this is     \n"
                    "* an unordered\n"
                    "* list\n\n"
                    "I expect 3 blocks")

    print(markdown_to_blocks(markdown_text))
