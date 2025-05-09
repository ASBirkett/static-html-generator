from textnode import TextNode, TextType
from leafnode import LeafNode
import re

def __make_delimiter_regex_safe(delimiter: str) -> str:
    match delimiter:
        case "**":
            return "\\*\\*"
        case _:
            return delimiter

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    nodes = []
    regex_safe_delim = __make_delimiter_regex_safe(delimiter)
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            # might not be the best way to do this, but i'm doing it this way
            split_nodes = re.split(rf"({regex_safe_delim}.*?{regex_safe_delim})", node.text)
            for string in split_nodes:
                if string.startswith(delimiter):
                    nodes.append(TextNode(string.replace(delimiter, ''), text_type))
                else:
                    if len(string) > 0:
                        nodes.append(TextNode(string, TextType.TEXT))
        else:
            nodes.append(node)

    return nodes

def text_node_to_html_node(text_node: TextNode):
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

def extract_markdown_images(text: str) -> list[tuple]:
    extract_tuple_list = []

    potential_images = re.findall(r"!\[(.*?)\]\((.*?)\)", text)

    for image_set in potential_images:
        extract_tuple_list.append(image_set)

    return extract_tuple_list

def extract_markdown_links(text: str) -> list[tuple]:
    extract_tuple_list = []

    potential_links = re.findall(r"\[(.*?)\]\((.*?)\)", text)

    for link_set in potential_links:
        extract_tuple_list.append(link_set)

    return extract_tuple_list

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    text_nodes = []

    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            split_nodes = re.split(r"(!\[.*?\]\(.*?\))", node.text)
            for split_node in split_nodes:
                potential_image_extract = extract_markdown_images(split_node)
                if len(potential_image_extract) > 0:
                    text_nodes.append(TextNode(potential_image_extract[0][0], TextType.IMAGE, potential_image_extract[0][1]))
                else:
                    if len(split_node) > 0:
                        text_nodes.append(TextNode(split_node, TextType.TEXT))
        else:
            text_nodes.append(node)   

    return text_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    text_nodes = []

    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            split_nodes = re.split(r"(\[.*?\]\(.*?\))", node.text)
            for split_node in split_nodes:
                potential_link_extract = extract_markdown_links(split_node)
                if len(potential_link_extract) > 0:
                    text_nodes.append(TextNode(potential_link_extract[0][0], TextType.LINK, potential_link_extract[0][1]))
                else:
                    if len(split_node) > 0:
                        text_nodes.append(TextNode(split_node, TextType.TEXT))
        else:
            text_nodes.append(node)            

    return text_nodes

def text_to_textnodes(text: str):
    node = TextNode(text, TextType.TEXT)
    final_nodes = [node]
    final_nodes = split_nodes_delimiter(final_nodes, "`", TextType.CODE)
    final_nodes = split_nodes_delimiter(final_nodes, "**", TextType.BOLD)
    final_nodes = split_nodes_delimiter(final_nodes, "_", TextType.ITALIC)
    final_nodes = split_nodes_image(final_nodes)
    final_nodes = split_nodes_link(final_nodes)
    return final_nodes



