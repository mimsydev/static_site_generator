class HTMLNode:
    # tag string
    # value string
    # children List<HTMLNode>
    # props Dictionary<string, string>
    def __init__(self,tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

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
