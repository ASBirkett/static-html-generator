from textnode import TextNode, TextType
from leafnode import LeafNode

def split_nodes_delimiter(old_nodes, delimiter, text_type) -> list[TextNode]:
    nodes = []
    current_node_text = ""
    for node in old_nodes:
        split_by_space_string = node.text.split()
        for string in split_by_space_string:
            if string.startswith(delimiter):
                if len(current_node_text) > 0:
                    nodes.append(TextNode(current_node_text.strip(), TextType.TEXT))
                current_node_text = ""
            elif string.endswith(delimiter):
                current_node_text += f"{string} "
                nodes.append(TextNode(current_node_text.strip(), text_type))
                current_node_text = ""
                continue
            
            current_node_text += f"{string} "

        if len(current_node_text) > 0:
            nodes.append(TextNode(current_node_text.strip(), TextType.TEXT))

    return nodes

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, { "href" : f"{text_node.url}"})
        case TextType.IMAGE:
            return LeafNode("img", "", { "src" : f"{text_node.url}", "alt" : f"{text_node.text}" })
        case _:
            raise Exception("Invalid text node type")
 

# node = TextNode("This is text with a **code block** word", TextType.TEXT)
# new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
# print(f"New node value: {new_nodes}")