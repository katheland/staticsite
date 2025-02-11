import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def testPropsToHTML(self):
        node = HTMLNode()
        node2 = HTMLNode(tag="p")
        node3 = HTMLNode(value="Hi")
        node4 = HTMLNode(children=[])
        node5 = HTMLNode(props={"href": "www.boot.dev"})
        node6 = HTMLNode("p", "Hi", [], {"href": "www.boot.dev"})
        self.assertEqual(node.props_to_html(), "")
        self.assertEqual(node2.props_to_html(), "")
        self.assertEqual(node3.props_to_html(), "")
        self.assertEqual(node4.props_to_html(), "")
        self.assertEqual(node5.props_to_html(), " href=\"www.boot.dev\"")
        self.assertEqual(node6.props_to_html(), " href=\"www.boot.dev\"")
    
    def testToHTML(self):
        node = HTMLNode()
        self.assertRaises(NotImplementedError, node.to_html)

if __name__ == "__main__":
    unittest.main()