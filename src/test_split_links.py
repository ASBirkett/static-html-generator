from textnode_parser_helper import split_nodes_link
from textnode import TextNode, TextType
import unittest


class TestSplitLinks(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_links_no_links(self):
        node = TextNode(
            "This is text with a link and",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link and", TextType.TEXT)
            ],
            new_nodes,
        )
    
    def test_split_links_missing_url(self):
        node = TextNode(
            "This is text with a link [to boot dev] and",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link [to boot dev] and", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_links_empty_url(self):
        node = TextNode(
            "This is text with a link [to boot dev]()",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "")
            ],
            new_nodes,
        )
    
    def test_split_links_link_only(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")
            ],
            new_nodes,
        )