import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def testToHTML(self):
        node = LeafNode(None, "This is some text")
        node2 = LeafNode("p", "This is some text")
        node3 = LeafNode("a", "This is some text", {"href": "www.boot.dev"})
        self.assertEqual(node.to_html(), "This is some text")
        self.assertEqual(node2.to_html(), "<p>This is some text</p>")
        self.assertEqual(node3.to_html(), "<a href=\"www.boot.dev\">This is some text</a>")
    
    def testErr(self):
        node = LeafNode(None, None)
        self.assertRaises(ValueError, node.to_html)
    
if __name__ == "__main__":
    unittest.main()