class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Child classes will override")

    def props_to_html(self):
        if not self.props:
            return ""

        props_repr = ""

        for key, value in self.props.items():
            props_repr += f' {key}="{value}"'
        
        return props_repr

    def __repr__(self):
        return f"tag = {self.tag},\nvalue = {self.value},\nchildren = {self.children},\nprops = {self.props}\n" 

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props, children=None)
    
    def to_html(self):
        if not self.value:
            raise ValueError("No value given")
        
        if not self.tag:
            return self.value
        
        if not self.props:
            return f'<{self.tag}>{self.value}</{self.tag}>'
        
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    
    def __repr__(self):
        return f"tag = {self.tag},\nvalue = {self.value},\nprops = {self.props}\n" 

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, props=props, children=children)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("Parent Nodes should have tags!")
        
        if not self.children:
            raise ValueError("The parent have no children")
        
        html = ""
        if self.props:
            html += f'<{self.tag}{self.props_to_html()}>'
        else:
            html += f'<{self.tag}>'
                
        for child in self.children:
            child_html = child.to_html()
            html += child_html
        
        html += f'</{self.tag}>'

        return html
