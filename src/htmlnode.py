class HTMLNode:
    # tag: a string representing the HTML tag name
    # value: a string representing the value of the HTML tag
    # children: a list of HTMLNode objects representing this node's children
    # props: a dictionary of key-value pairs representing the attributes of the HTML tag
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html isn't implemented here.  Try one of the child classes.")

    def props_to_html(self):
        if self.props == None:
            return ""
        html_string = ""
        for prop in self.props:
            html_string += f' {prop}="{self.props[prop]}"'
        return html_string
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props