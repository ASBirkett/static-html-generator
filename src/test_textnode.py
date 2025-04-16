import unittest

from textnode import TextNode, TextType
from textnode_parser_helper import split_nodes_delimiter, text_node_to_html_node



class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a link node", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_link_has_url(self):
        node = TextNode("This is a link node", TextType.LINK, "www.something.com")
        self.assertIsNotNone(node.url)
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_text_node_to_link(self):
        node = TextNode("Link test", TextType.LINK, "www.something.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(
            html_node.to_html(),
            "<a href=\"www.something.com\">Link test</a>"
        )

    def test_text_node_to_image(self):
        node = TextNode("Image test", TextType.IMAGE, "https://www.boot.dev/img/bootdev-logo-full-small.webp")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(
            html_node.to_html(),
            "<img src=\"https://www.boot.dev/img/bootdev-logo-full-small.webp\" alt=\"Image test\"></img>"
        )

    def test_split_nodes_code(self):
        delimiter = "`"
        node = TextNode(f"This is text with a {delimiter}code block{delimiter} word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], f"{delimiter}", TextType.CODE)
        self.assertIsNotNone(new_nodes)
        self.assertTrue(len(new_nodes) == 3)
        self.assertTrue(any(x.text_type == TextType.CODE for x in new_nodes))

    def test_split_nodes_multiple_code(self):
        delimiter = "`"
        node = TextNode(f"{delimiter}This is{delimiter} text with a {delimiter}code block{delimiter} word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], f"{delimiter}", TextType.CODE)
        self.assertIsNotNone(new_nodes)
        self.assertTrue(len(new_nodes) == 4)
        self.assertTrue(any(x.text_type == TextType.CODE for x in new_nodes))

    def test_split_nodes_bold(self):
        delimiter = "**"
        node = TextNode(f"This is text with a {delimiter}bold text{delimiter} word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], f"{delimiter}", TextType.BOLD)
        self.assertIsNotNone(new_nodes)
        self.assertTrue(len(new_nodes) == 3)
        self.assertTrue(any(x.text_type == TextType.BOLD for x in new_nodes))

    def test_split_nodes_itallic(self):
        delimiter = "_"
        node = TextNode(f"This is text with a {delimiter}italic word{delimiter} word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], f"{delimiter}", TextType.ITALIC)
        self.assertIsNotNone(new_nodes)
        self.assertTrue(len(new_nodes) == 3)
        self.assertTrue(any(x.text_type == TextType.ITALIC for x in new_nodes))



if __name__ == "__main__":
    unittest.main()