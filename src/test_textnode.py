import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.BOLD, None)
        node4 = TextNode("This is a text node", TextType.BOLD, "http://www.boot.dev")
        node5 = TextNode("This is a text node", TextType.BOLD, "http://www.boot.dev")
        self.assertEqual(node, node2)
        self.assertEqual(node, node3)
        self.assertEqual(node4, node5)

    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.ITALIC)
        node4 = TextNode("This is a text node", TextType.BOLD, "")
        node5 = TextNode("This is a text node", TextType.BOLD, "http://www.boot.dev")
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node, node4)
        self.assertNotEqual(node, node5)

if __name__ == "__main__":
    unittest.main()