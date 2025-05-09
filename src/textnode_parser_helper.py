from textnode import TextNode, TextType
from leafnode import LeafNode
import re

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

def extract_markdown_images(text) -> list[tuple]:
    extract_tuple_list = []

    potential_images = re.findall(r"!\[(.*?)\]\((.*?)\)", text)

    for image_set in potential_images:
        extract_tuple_list.append(image_set)

    return extract_tuple_list

def extract_markdown_links(text) -> list[tuple]:
    extract_tuple_list = []

    potential_links = re.findall(r"\[(.*?)\]\((.*?)\)", text)

    for link_set in potential_links:
        extract_tuple_list.append(link_set)

    return extract_tuple_list

def split_nodes_image(old_nodes):
    text_nodes = []

    for node in old_nodes:
        split_nodes = re.split(r"(!\[.*?\]\(.*?\))", node.text)
        for split_node in split_nodes:
            potential_image_extract = extract_markdown_images(split_node)
            if len(potential_image_extract) > 0:
                text_nodes.append(TextNode(potential_image_extract[0][0], TextType.IMAGE, potential_image_extract[0][1]))
            else:
                if len(split_node) > 0:
                    text_nodes.append(TextNode(split_node, TextType.TEXT))            

    return text_nodes

def split_nodes_link(old_nodes):
    text_nodes = []

    for node in old_nodes:
        split_nodes = re.split(r"(\[.*?\]\(.*?\))", node.text)
        for split_node in split_nodes:
            potential_link_extract = extract_markdown_links(split_node)
            if len(potential_link_extract) > 0:
                text_nodes.append(TextNode(potential_link_extract[0][0], TextType.LINK, potential_link_extract[0][1]))
            else:
                if len(split_node) > 0:
                    text_nodes.append(TextNode(split_node, TextType.TEXT))            

    return text_nodes