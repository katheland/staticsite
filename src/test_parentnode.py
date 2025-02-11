import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def testToHTML(self):
        node = ParentNode("p", [LeafNode("p", "This is some text")])
        node2 = ParentNode("p", [])
        node3 = ParentNode("a", [LeafNode("p", "This is some text")], {"href": "www.boot.dev"})
        node4 = ParentNode("p", [LeafNode("b", "This is bold text"), LeafNode(None, "This isn't bold text")])
        node5 = ParentNode("p", [ParentNode("b", [LeafNode("i", "Text!")])])
        node6 = ParentNode("p", [ParentNode("b", [LeafNode("i", "Italic text")]), LeafNode(None, "Not italic text")])
        self.assertEqual(node.to_html(), "<p><p>This is some text</p></p>")
        self.assertEqual(node2.to_html(), "<p></p>")
        self.assertEqual(node3.to_html(), "<a href=\"www.boot.dev\"><p>This is some text</p></a>")
        self.assertEqual(node4.to_html(), "<p><b>This is bold text</b>This isn't bold text</p>")
        self.assertEqual(node5.to_html(), "<p><b><i>Text!</i></b></p>")
        self.assertEqual(node6.to_html(), "<p><b><i>Italic text</i></b>Not italic text</p>")

    def testErr(self):
        node = ParentNode(None, [LeafNode("p", "This is some text")])
        node2 = ParentNode("p", None)
        node3 = ParentNode(None, None)
        self.assertRaises(ValueError, node.to_html)
        self.assertRaises(ValueError, node2.to_html)
        self.assertRaises(ValueError, node3.to_html)

if __name__ == "__main__":
    unittest.main()