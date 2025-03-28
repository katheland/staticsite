import re
from textnode import TextType, TextNode
from leafnode import LeafNode

# convert a TextNode to a LeafNode
def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Text type not found!")

# splits TextNodes up based on a delimiter
# FOR LATER: extend this to allow nesting
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_text = node.text.split(delimiter)
            if len(split_text) == 1:
                new_nodes.append(TextNode(node.text, TextType.TEXT))
            else:
                if split_text[0] != "":
                    new_nodes.append(TextNode(split_text[0], TextType.TEXT))
                for i in range(1, len(split_text), 2):
                    new_nodes.append(TextNode(split_text[i], text_type))
                    if i+1 == len(split_text):
                        raise Exception("Markdown exception - no matching pair")
                    if split_text[i+1] != "":
                        new_nodes.append(TextNode(split_text[i+1], TextType.TEXT))
    return new_nodes

# extract images from markdown text
def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

# extract links from markdown text
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

# split TextNodes up from their images
def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            image_list = extract_markdown_images(node.text)
            last_string = node.text
            for image in image_list:
                sections = last_string.split(f"![{image[0]}]({image[1]})", 1)
                if sections[0] != "":
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                last_string = sections[1]
            if last_string != "":
                new_nodes.append(TextNode(last_string, TextType.TEXT))
    return new_nodes

# split TextNodes up from their links
def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            link_list = extract_markdown_links(node.text)
            last_string = node.text
            for link in link_list:
                sections = last_string.split(f"[{link[0]}]({link[1]})", 1)
                if sections[0] != "":
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                last_string = sections[1]
            if last_string != "":
                new_nodes.append(TextNode(last_string, TextType.TEXT))
    return new_nodes

# split a string into a list of TextNodes
# (code before bold before italics)
def text_to_textnodes(text):
    return split_nodes_link(
        split_nodes_image(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_delimiter([TextNode(text, TextType.TEXT)], "`", TextType.CODE), "**", TextType.BOLD), "_", TextType.ITALIC
                )
            )
        )
    