from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    # A leaf node has no children, but always has a value.
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value == None:
            raise ValueError("This LeafNode is missing a value!")
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"