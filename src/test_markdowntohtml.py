import unittest

from markdowntohtml import *
from textnode import *

class TestMarkdownToHTML(unittest.TestCase):
    def testMarkdownToHTMLNode(self):
        text = ""
        text2 = "paragraph\nparagraph"
        text3 = "## heading\nstill heading"
        text4 = "####### not heading"
        text5 = ">quote\n>quote"
        text11 = "> quote\n> quote"
        text6 = "- unordered\n* unordered"
        text7 = "1. one\n2. two\n3. three\n4. four\n5. five\n6. six\n7. seven\n8. eight\n9. nine\n10. ten"
        text8 = "```here is some code```"
        text9 = "**Bold** or *italic*"
        text10 = "# heading\n\nparagraph\n\n```code```"
        self.assertEqual(markdown_to_html_node(text), ParentNode("div", []))
        self.assertEqual(markdown_to_html_node(text2), ParentNode("div", [ParentNode("p", [LeafNode(None, "paragraph"), LeafNode(None, "paragraph")])]))
        self.assertEqual(markdown_to_html_node(text3), ParentNode("div", [ParentNode("h2", [LeafNode(None, "heading"), LeafNode(None, "still heading")])]))
        self.assertEqual(markdown_to_html_node(text4), ParentNode("div", [ParentNode("p", [LeafNode(None, "####### not heading")])]))
        self.assertEqual(markdown_to_html_node(text5), ParentNode("div", [ParentNode("blockquote", [LeafNode(None, "quote"), LeafNode(None, "quote")])]))
        self.assertEqual(markdown_to_html_node(text11), ParentNode("div", [ParentNode("blockquote", [LeafNode(None, "quote"), LeafNode(None, "quote")])]))
        self.assertEqual(markdown_to_html_node(text6), ParentNode("div", [ParentNode("ul", [ParentNode("li", [LeafNode(None, "unordered")]), ParentNode("li", [LeafNode(None, "unordered")])])]))
        self.assertEqual(markdown_to_html_node(text7), ParentNode("div", [ParentNode("ol", [ParentNode("li", [LeafNode(None, "one")]), ParentNode("li", [LeafNode(None, "two")]), ParentNode("li", [LeafNode(None, "three")]),ParentNode("li", [LeafNode(None, "four")]), ParentNode("li", [LeafNode(None, "five")]), ParentNode("li", [LeafNode(None, "six")]), ParentNode("li", [LeafNode(None, "seven")]), ParentNode("li", [LeafNode(None, "eight")]), ParentNode("li", [LeafNode(None, "nine")]), ParentNode("li", [LeafNode(None, "ten")])])]))
        self.assertEqual(markdown_to_html_node(text8), ParentNode("div", [ParentNode("pre", [LeafNode("code", "here is some code")])]))
        self.assertEqual(markdown_to_html_node(text9), ParentNode("div", [ParentNode("p", [LeafNode("b", "Bold"), LeafNode(None, " or "), LeafNode("i", "italic")])]))
        self.assertEqual(markdown_to_html_node(text10), ParentNode("div", [ParentNode("h1", [LeafNode(None, "heading")]),ParentNode("p", [LeafNode(None, "paragraph")]),ParentNode("pre", [LeafNode("code", "code")])]))

    def testTextToChildren(self):
        text = ""
        text2 = "plain"
        text3 = "*italic*"
        text4 = "**bold**"
        text5 = "`code`"
        text6 = "[url](url.com)"
        text7 = "![img](img.com)"
        text8 = "**Bold** or *italic*"
        self.assertEqual(text_to_children(text), [])
        self.assertEqual(text_to_children(text2), [LeafNode(None, "plain")])
        self.assertEqual(text_to_children(text3), [LeafNode("i", "italic")])
        self.assertEqual(text_to_children(text4), [LeafNode("b", "bold")])
        self.assertEqual(text_to_children(text5), [LeafNode("code", "code")])
        self.assertEqual(text_to_children(text6), [LeafNode("a", "url", {"href": "url.com"})])
        self.assertEqual(text_to_children(text7), [LeafNode("img", "", {"src": "img.com", "alt": "img"})])
        self.assertEqual(text_to_children(text8), [LeafNode("b", "Bold"), LeafNode(None, " or "), LeafNode("i", "italic")])

if __name__ == "__main__":
    unittest.main()