from parentnode import ParentNode
from leafnode import LeafNode

from blockhelpers import *
from inlinehelpers import *

# converts a markdown document into a parent HTML node that contains its children
def markdown_to_html_node(markdown):
    child_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        lines = block.split("\n")
        children = []
        node_type = block_to_block_type(block)
        match node_type:
            case BlockType.HEADING:
                header_num = len(block) - len(block.lstrip("#"))
                lines = block.lstrip("#")[1:].split("\n")
                for line in lines:
                    nodes = text_to_children(line)
                    for node in nodes:
                        children.append(node)
                child_nodes.append(ParentNode(f"h{header_num}", children))
            case BlockType.CODE:
                # everything in the code block goes in as is, save for the ``` at the start and end
                child_nodes.append(ParentNode("pre", [LeafNode("code", block[3:-3])]))
            case BlockType.QUOTE:
                for line in lines:
                    nodes = text_to_children(line[1:].strip())
                    for node in nodes:
                        children.append(node)
                child_nodes.append(ParentNode("blockquote", children))
            case BlockType.UNORDERED:
                for line in lines:
                    children.append(ParentNode("li", text_to_children(line[2:])))
                child_nodes.append(ParentNode("ul", children))
            case BlockType.ORDERED:
                for line in lines:
                    children.append(ParentNode("li", text_to_children(line.lstrip("0123456789")[2:])))
                child_nodes.append(ParentNode("ol", children))
            case BlockType.PARAGRAPH:
                for line in lines:
                    nodes = text_to_children(line)
                    for node in nodes:
                        children.append(node)
                child_nodes.append(ParentNode("p", children))
            case _:
                # not sure how we'd get here but to cover all bases
                raise Exception("Invalid block type, somehow???")
    return ParentNode("div", child_nodes)
    
def text_to_children(line):
    line_nodes = text_to_textnodes(line)
    html_nodes = []
    for node in line_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes
