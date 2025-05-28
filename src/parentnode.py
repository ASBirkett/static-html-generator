from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, props=props)
        self.children = children

    def to_html(self) -> str:
        if self.tag == None:
            raise ValueError("Parent node must have a tag")
        
        if self.children == None:
            raise ValueError("Parent node must have at least one child")
        
        final_element = ""

        if self.props == None:
            final_element = f"<{self.tag}>"
        else:
            final_element = f"<{self.tag} {self.props_to_html()}>"

        for child in self.children:
            final_element += child.to_html()

        final_element += f"</{self.tag}>"
        
        return final_element