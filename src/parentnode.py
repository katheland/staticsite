from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    # A parent node always has a tag and children, but doesn't have a value.
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("This ParentNode is missing a tag!")
        if self.children == None:
            raise ValueError("This ParentNode doesn't have any children!")
        html_string = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            html_string += child.to_html()
        html_string += f"</{self.tag}>"
        return html_string