from typing import Self

class HTMLNode():
    def __init__(self, tag = None, value = None, children: list[Self] = None, props : dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self) -> str:
        return_value = ""

        for name, value in self.props.items():
            return_value += f" {name}=\"{value}\""

        return return_value
    
    def __repr__(self):
        return_value = "\n===========HTMLNode Start==============\n"

        return_value += f"tag: {self.tag}\n"
        return_value += f"value: {self.value}\n"
        return_value += f"children: {self.children}\n"
        return_value += f"props: {self.props_to_html()}"

        return_value += "\n===========HTMLNode End==============\n"

        return return_value
