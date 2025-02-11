from enum import Enum

class BlockType(Enum):
    HEADING = "heading",
    CODE = "code",
    QUOTE = "quote",
    UNORDERED = "unordered",
    ORDERED = "ordered",
    PARAGRAPH = "paragraph"


# separates raw markdown into blocks
def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n")
    stripped_blocks = []
    for block in raw_blocks:
        if block != "":
            stripped_blocks.append(block.strip())
    return stripped_blocks

# returns the block's type
def block_to_block_type(block):
    # these should have been stripped away by now but just in case
    if block == "":
        return BlockType.PARAGRAPH
    # headings start with 1-6 # characters followed by a space
    if block[0] == "#":
        # count the number of #s
        without_sharps = block.lstrip('#')
        sharp_num = len(block) - len(without_sharps)
        if sharp_num <= 6 and without_sharps != "" and without_sharps[0] == " ":
            return BlockType.HEADING

    # code blocks start and end with 3 ` characters
    if block[0] == "`":
        front_three = block[0:3]
        back_three = block[-3:]
        if front_three == "```" and back_three == "```":
            return BlockType.CODE

    # every line in a quote block starts with a > character
    if block[0] == ">":
        lines = block.split("\n")
        for line in lines:
            if line[0] != ">":
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    # every line in an unordered list block starts with a * or - character followed by a space
    if block[0] == "-" or block[0] == "*":
        lines = block.split("\n")
        for line in lines:
            if line[0:2] != "* " and line[0:2] != "- ":
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED

    # every line in an ordered list block starts with an increasing number followed by a . and a space
    if block[0] == "1":
        lines = block.split("\n")
        for i in range(0, len(lines)):
            num_length = len(str(i+1))
            if lines[i][0:num_length+2] != f"{i+1}. ":
                return BlockType.PARAGRAPH
        return BlockType.ORDERED

    # if it's none of these, it's a normal paragraph
    return BlockType.PARAGRAPH

# extracts the h1 header from the markdown file
def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block[0:2] == "# ":
            return block[2:]
    raise Exception("No h1 header found!")