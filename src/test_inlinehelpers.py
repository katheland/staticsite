import unittest

from inlinehelpers import *
from textnode import *
from leafnode import LeafNode

class TestInlineHelpers(unittest.TestCase):
    def testTextHTML(self):
        node = TextNode("Normal text", TextType.TEXT)
        node2 = TextNode("Italic text", TextType.ITALIC)
        node3 = TextNode("Bold text", TextType.BOLD)
        node4 = TextNode("Code text", TextType.CODE)
        node5 = TextNode("URL text", TextType.LINK, "www.boot.dev")
        node6 = TextNode("Image text", TextType.IMAGE, "www.boot.dev")
        self.assertEqual(text_node_to_html_node(node), LeafNode(None, "Normal text"))
        self.assertEqual(text_node_to_html_node(node2), LeafNode("i", "Italic text"))
        self.assertEqual(text_node_to_html_node(node3), LeafNode("b", "Bold text"))
        self.assertEqual(text_node_to_html_node(node4), LeafNode("code", "Code text"))
        self.assertEqual(text_node_to_html_node(node5), LeafNode("a", "URL text", {"href": "www.boot.dev"}))
        self.assertEqual(text_node_to_html_node(node6), LeafNode("img", "", {"src": "www.boot.dev", "alt": "Image text"}))
        
    def testTextHTMLError(self):
        node7 = TextNode("Invalid text", "invalid")
        self.assertRaises(Exception, text_node_to_html_node, node7)
    
    def testSplitTextNode(self):
        node = TextNode("Plain text", TextType.TEXT)
        node2 = TextNode("*Italics*", TextType.TEXT)
        node3 = TextNode("URL text", TextType.LINK, "www.boot.dev")
        node4 = TextNode("The **bold** is contained", TextType.TEXT)
        node5 = TextNode("`There's some code` on the left", TextType.TEXT)
        node6 = TextNode("And now some code `on the right`", TextType.TEXT)
        node7 = TextNode("Read it **like** a bad **comic book**", TextType.TEXT)
        node8 = TextNode("This should *only* pick up the **bold**, not the `others`, okay?", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node, node2], "*", TextType.ITALIC), [TextNode("Plain text", TextType.TEXT), TextNode("Italics", TextType.ITALIC)])
        self.assertEqual(split_nodes_delimiter([node3], "`", TextType.CODE), [TextNode("URL text", TextType.LINK, "www.boot.dev")])
        self.assertEqual(split_nodes_delimiter([node4], "**", TextType.BOLD), [TextNode("The ", TextType.TEXT), TextNode("bold", TextType.BOLD), TextNode(" is contained", TextType.TEXT)])
        self.assertEqual(split_nodes_delimiter([node5], "`", TextType.CODE), [TextNode("There's some code", TextType.CODE), TextNode(" on the left", TextType.TEXT)])
        self.assertEqual(split_nodes_delimiter([node6], "`", TextType.CODE), [TextNode("And now some code ", TextType.TEXT), TextNode("on the right", TextType.CODE)])
        self.assertEqual(split_nodes_delimiter([node7], "**", TextType.BOLD), [TextNode("Read it ", TextType.TEXT), TextNode("like", TextType.BOLD), TextNode(" a bad ", TextType.TEXT), TextNode("comic book", TextType.BOLD)])
        self.assertEqual(split_nodes_delimiter([node8], "**", TextType.BOLD), [TextNode("This should *only* pick up the ", TextType.TEXT), TextNode("bold", TextType.BOLD), TextNode(", not the `others`, okay?", TextType.TEXT)])
        
    def testSplitTextNodeError(self):
        node9 = TextNode("This one should **fail*", TextType.TEXT)
        self.assertRaises(Exception, split_nodes_delimiter, [node9], "**", TextType.BOLD)
    
    def testExtractImages(self):
        text = ""
        text2 = "noodle"
        text3 = "![this is an image](image.com/hi)"
        text4 = "[this is a url](url.com)"
        text5 = "![this is an image](image.com) [this is a url](url.com)"
        text6 = "![this is an image](image.com) ![this is a second image](image.com)"
        self.assertEqual(extract_markdown_images(text), [])
        self.assertEqual(extract_markdown_images(text2), [])
        self.assertEqual(extract_markdown_images(text3), [("this is an image", "image.com/hi")])
        self.assertEqual(extract_markdown_images(text4), [])
        self.assertEqual(extract_markdown_images(text5), [("this is an image", "image.com")])
        self.assertEqual(extract_markdown_images(text6), [("this is an image", "image.com"), ("this is a second image", "image.com")])
    
    def testExtractLinks(self):
        text = ""
        text2 = "noodle"
        text3 = "![this is an image](image.com)"
        text4 = "[this is a url](url.com/hi)"
        text5 = "![this is an image](image.com) [this is a url](url.com)"
        text6 = "[this is a url](url.com) [this is a second url](url.com)"
        self.assertEqual(extract_markdown_links(text), [])
        self.assertEqual(extract_markdown_links(text2), [])
        self.assertEqual(extract_markdown_links(text3), [])
        self.assertEqual(extract_markdown_links(text4), [("this is a url", "url.com/hi")])
        self.assertEqual(extract_markdown_links(text5), [("this is a url", "url.com")])
        self.assertEqual(extract_markdown_links(text6), [("this is a url", "url.com"), ("this is a second url", "url.com")])
    
    def testSplitImages(self):
        text = TextNode("", TextType.TEXT)
        text2 = TextNode("noodle", TextType.TEXT)
        text3 = TextNode("![this is an image](image.com)", TextType.TEXT)
        text4 = TextNode("[this is a url](url.com)", TextType.TEXT)
        text5 = TextNode("![this is an image](image.com) [this is a url](url.com)", TextType.TEXT)
        text6 = TextNode("![this is an image](image.com) ![this is a second image](image.com)", TextType.TEXT)
        self.assertEqual(split_nodes_image([]), [])
        self.assertEqual(split_nodes_image([text]), [])
        self.assertEqual(split_nodes_image([text2]), [text2])
        self.assertEqual(split_nodes_image([text3]), [TextNode("this is an image", TextType.IMAGE, "image.com")])
        self.assertEqual(split_nodes_image([text4]), [text4])
        self.assertEqual(split_nodes_image([text3, text4]), [TextNode("this is an image", TextType.IMAGE, "image.com"), text4])
        self.assertEqual(split_nodes_image([text5]), [TextNode("this is an image", TextType.IMAGE, "image.com"), TextNode(" [this is a url](url.com)", TextType.TEXT)])
        self.assertEqual(split_nodes_image([text6]), [TextNode("this is an image", TextType.IMAGE, "image.com"), TextNode(" ", TextType.TEXT), TextNode("this is a second image", TextType.IMAGE, "image.com")])
    
    def testSplitLinks(self):
        text = TextNode("", TextType.TEXT)
        text2 = TextNode("noodle", TextType.TEXT)
        text3 = TextNode("![this is an image](image.com)", TextType.TEXT)
        text4 = TextNode("[this is a url](url.com)", TextType.TEXT)
        text5 = TextNode("![this is an image](image.com) [this is a url](url.com)", TextType.TEXT)
        text6 = TextNode("[this is a url](url.com) [this is a second url](url.com)", TextType.TEXT)
        self.assertEqual(split_nodes_link([]), [])
        self.assertEqual(split_nodes_link([text]), [])
        self.assertEqual(split_nodes_link([text2]), [text2])
        self.assertEqual(split_nodes_link([text3]), [text3])
        self.assertEqual(split_nodes_link([text4]), [TextNode("this is a url", TextType.LINK, "url.com")])
        self.assertEqual(split_nodes_link([text3, text4]), [text3, TextNode("this is a url", TextType.LINK, "url.com")])
        self.assertEqual(split_nodes_link([text5]), [TextNode("![this is an image](image.com) ", TextType.TEXT), TextNode("this is a url", TextType.LINK, "url.com")])
        self.assertEqual(split_nodes_link([text6]), [TextNode("this is a url", TextType.LINK, "url.com"), TextNode(" ", TextType.TEXT), TextNode("this is a second url", TextType.LINK, "url.com")])
        
    def testTextToNodes(self):
        text = ""
        text2 = "normal"
        text3 = "**bold**"
        text4 = "*italic*"
        text5 = "`code`"
        text6 = "![image](image.com)"
        text7 = "[link](link.com)"
        text8 = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        text9 = "*Have some italics* **before the bold**"
        self.assertEqual(text_to_textnodes(text), [])
        self.assertEqual(text_to_textnodes(text2), [TextNode("normal", TextType.TEXT)])
        self.assertEqual(text_to_textnodes(text3), [TextNode("bold", TextType.BOLD)])
        self.assertEqual(text_to_textnodes(text4), [TextNode("italic", TextType.ITALIC)])
        self.assertEqual(text_to_textnodes(text5), [TextNode("code", TextType.CODE)])
        self.assertEqual(text_to_textnodes(text6), [TextNode("image", TextType.IMAGE, "image.com")])
        self.assertEqual(text_to_textnodes(text7), [TextNode("link", TextType.LINK, "link.com")])
        self.assertEqual(text_to_textnodes(text8), [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ])
        self.assertEqual(text_to_textnodes(text9), [TextNode("Have some italics", TextType.ITALIC), TextNode(" ", TextType.TEXT), TextNode("before the bold", TextType.BOLD)])


if __name__ == "__main__":
    unittest.main()