class HTMLNode:
    # tag string
    # value string
    # children List<HTMLNode>
    # props Dictionary<string, string>
    def __init__(self,tag=None, value=None, children=None, props=None, self_closing = False):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        self.self_closing = self_closing

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        html_string = ""
        if self.props != None:
            if len(self.props) > 0:
                for tag,value in self.props.items():
                    if len(value) > 0:
                        html_string += f" {tag}=\"{value}\""
                    else:
                        html_string += " " + tag
        return html_string

    def __repr__(self):
        name_str = type(self).__name__
        tag_str = "None" if self.tag == None else self.tag
        value_str = "None"if self.value == None else self.value
        children_str = ""
        if self.children == None:
            children_str = "None"
        else:
            for child in self.children:
                children_str += child.__repr__()
        props_str = self.props_to_html()

        print_string = f"{name_str}(\'{tag_str}\', \'{value_str}\', \'{children_str}\', \'{props_str}\')"
        return print_string

class LeafNode(HTMLNode):
    def __init__(self, value, tag = None, props = None, self_closing = False):
        super().__init__(tag, value, None, props, self_closing)

    def to_html(self):
        if self.value == None:
            raise ValueError("The 'value' parameter is required to construct a leaf node.")
        if self.tag == None:
            return self.value
        opening_tag = f"<{self.tag}{self.props_to_html()}>"
        if self.value == "" and self.self_closing:
            closing_tag = ""
        else:
            closing_tag = f"</{self.tag}>"
        return f"{opening_tag}{self.value}{closing_tag}"

class ParentNode(HTMLNode):
    def __init__(self, children, tag = None, props = None):
        super().__init__(tag, None, children, props, False)

    def to_html(self):
        if len(self.children) <= 0:
            raise ValueError("A parent node must have children supplied. That's the point of being a parent...")
        if self.tag == None:
            raise ValueError("A tag must be provided for a parent node")
        opening_tag = f"<{self.tag}{self.props_to_html()}>"
        closing_tag = f"</{self.tag}>"
        inner_html = "".join(list(map(lambda c: c.to_html(), self.children)))
        return f"{opening_tag}{inner_html}{closing_tag}"

