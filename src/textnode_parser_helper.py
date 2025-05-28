from textnode import TextNode, TextType, BlockType
from parentnode import ParentNode
from leafnode import LeafNode
import re
import os

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

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
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

def text_to_textnodes(text: str) -> list[TextNode]:
    node = TextNode(text, TextType.TEXT)
    final_nodes = [node]
    final_nodes = split_nodes_delimiter(final_nodes, "`", TextType.CODE)
    final_nodes = split_nodes_delimiter(final_nodes, "**", TextType.BOLD)
    final_nodes = split_nodes_delimiter(final_nodes, "_", TextType.ITALIC)
    final_nodes = split_nodes_image(final_nodes)
    final_nodes = split_nodes_link(final_nodes)
    return final_nodes

def markdown_to_blocks(markdown : str) -> list[str]:
    text_blocks = []

    raw_blocks = markdown.split("\n\n")

    for block in raw_blocks:
        block = block.strip()
        if len(block) > 0:
            text_blocks.append(block)

    return text_blocks

def block_to_block_type(block : str) -> BlockType:
    match block:
        case p if bool(re.match(r"^#{1,6} .*", p)):
            return BlockType.HEADING
        case p if bool(re.fullmatch(r"^`{3}.*`{3}$", p, re.DOTALL)):
            return BlockType.CODE
        case p if bool(re.match(r"^>.*", p)):
            return BlockType.QUOTE
        case p if bool(re.match(r"^- .*", p)):
            lines = p.split('\n')
            for line in lines:
                if not bool(re.match(r"^- .*", line)):
                    return BlockType.PARAGRAPH
            return BlockType.UNORDERED_LIST
        case p if bool(re.match(r"1\. .*", p)):
            lines = p.split('\n')
            expected_number = 0
            for line in lines:
                expected_number += 1
                if not bool(re.match(rf"{expected_number}\. .*", line)):
                    return BlockType.PARAGRAPH
            return BlockType.ORDERED_LIST
        case _:
            return BlockType.PARAGRAPH
        

def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                nodes.append(__create_heading_html_node(block))
            case BlockType.QUOTE:
                nodes.append(__create_quote_html_node(block))
            case BlockType.ORDERED_LIST:
                nodes.append(__create_ordered_list_html_node(block))
            case BlockType.UNORDERED_LIST:
                nodes.append(__create_unordered_list_html_node(block))
            case BlockType.CODE:
                nodes.append(__create_code_html_node(block))
            case _: #PARAGRAPH
                nodes.append(__create_paragraph_html_node(block))
    
    return ParentNode('div', nodes)


def __create_paragraph_html_node(block_str: str) -> ParentNode:
    text_nodes = text_to_textnodes(block_str.replace('\n', ' '))
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    new_parent_node = ParentNode('p', html_nodes)
    return new_parent_node

def __create_code_html_node(block_str: str) -> ParentNode:
    code_text_node = TextNode(block_str, TextType.TEXT)
    code_text_nodes = split_nodes_delimiter([code_text_node], '```', TextType.CODE)
    code_text_nodes[0].text = code_text_nodes[0].text.strip().replace('\n', '\n')
    code_html = text_node_to_html_node(code_text_nodes[0])
    return ParentNode('pre', [code_html])

def __create_heading_html_node(block_str: str) -> ParentNode:
    split_header = re.split(r"^(#{1,6} )", block_str)
    header_hash_count = len(split_header[1]) - 1
    header_text_nodes = text_to_textnodes(split_header[2])[0]
    return ParentNode(f"h{header_hash_count}", [text_node_to_html_node(header_text_nodes)])

def __create_quote_html_node(block_str: str) -> ParentNode:
    quote_texts = re.findall(r"(^>.*)", block_str, re.MULTILINE)
    final_quote_text = ""
    for quote_text in quote_texts:
        final_quote_text += quote_text.replace("> ", "")
    print(final_quote_text)
    quote_text_node = TextNode(final_quote_text, TextType.TEXT)
    return ParentNode('blockquote', [text_node_to_html_node(quote_text_node)])

def __create_ordered_list_html_node(block_str: str) -> ParentNode:
    list_items = []
    ordered_item_lines = re.findall(r"(\d+\.\s+.*?)(?=\n|$)", block_str)
    num_prefix = 0
    for line in ordered_item_lines:
        num_prefix += 1
        text_nodes = text_to_textnodes(line.replace(f"{num_prefix}. ", ""))
        current_line_parent = ParentNode('li', [])
        for text_node in text_nodes:
            current_line_parent.children.append(text_node_to_html_node(text_node))
        list_items.append(current_line_parent)
    return ParentNode('ol', list_items)

def __create_unordered_list_html_node(block_str: str) -> ParentNode:
    list_items = []
    unordered_item_lines = re.findall(r"(-\s+.*?)(?=\n|$)", block_str)
    for line in unordered_item_lines:
        text_nodes = text_to_textnodes(line.replace("- ", ""))
        current_line_parent = ParentNode('li', [])
        for text_node in text_nodes:
            current_line_parent.children.append(text_node_to_html_node(text_node))
        list_items.append(current_line_parent)
    return ParentNode('ul', list_items)

def extract_title(markdown) -> str:
    potential_title = re.findall(r"^(#{1} .*)", markdown)
    if len(potential_title) == 0:
        raise Exception("Markdown must start with a header tag that contains one (1) hash (#)")
    split_header = re.split(r"^(#{1} )", potential_title[0])
    
    return split_header[2]
        
def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from \"{from_path}\" to \"{dest_path}\" using \"{template_path}\" as the template")
    content_markdown = __read_content_from_file(from_path)
    template_html = __read_content_from_file(template_path)
    
    converted_markdown_html = markdown_to_html_node(content_markdown).to_html()

    content_title = extract_title(content_markdown)

    template_html = template_html.replace("{{ Title }}", f"{content_title}")
    template_html = template_html.replace("{{ Content }}", converted_markdown_html)
    
    dir_name = os.path.dirname(dest_path)
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    write_result = __write_content_to_file(dest_path, template_html)

    return write_result






def __read_content_from_file(file_path: str) -> str:
    with open(file_path, "r") as f:
        return f.read()
    
def __write_content_to_file(file_path: str, content: str) -> bool:
    try:
        with open(file_path, 'w') as f:
            f.write(content)
    except Exception as e:
        print(f"Failed to write contents to {file_path}: {e}")
        return False
    
    return True

# generate_page("../content/index.md", "../template.html", "../public/index.html")
# md = """### This is a header

# This is a **bolded** paragraph
# text in a p
# tag here

# This is another paragraph with _italic_ text and `code` here

# ```Check this out
# int thing = 55;
# thing += 10;```

# >This is a quote block.
# This line should also be apart of the quote block


# - Item 1
# - Item 2
# - Item 3
# - Item 4

# 1. Get materials
# 2. Read instructions
# 3. Make Food
# """

# md = """
# ```
# This is text that _should_ remain
# the **same** even with inline stuff
# ```
# """
# md = """
# - Item 1
# - Item 2
# - Item 3
# - Item 4
# """
# node = markdown_to_html_node(md)
# print(node.to_html())