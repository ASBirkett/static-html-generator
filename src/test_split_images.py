from textnode_parser_helper import split_nodes_image
from textnode import TextNode, TextType
import unittest

class TestSplitImages(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_image_no_images(self):
        node = TextNode(
            "This is text with no images",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with no images", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_image_missing_url(self):
        node = TextNode(
            "This is text with no image url ![image]",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with no image url ![image]", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_image_empty_url(self):
        node = TextNode(
            "This is text with empty url ![image]()",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with empty url ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "")
            ],
            new_nodes,
        )

    def test_split_image_images_only(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
            ],
            new_nodes,
        )