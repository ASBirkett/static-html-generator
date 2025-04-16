import unittest

from textnode import TextNode, TextType
from leafnode import LeafNode

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.NORMAL:
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
        node = TextNode("This is a text node", TextType.NORMAL)
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


if __name__ == "__main__":
    unittest.main()