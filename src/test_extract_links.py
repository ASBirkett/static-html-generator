from textnode_parser_helper import extract_markdown_images, extract_markdown_links
import unittest

class TestExtractLinks(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and here is another image ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"),("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is [a link to an image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("a link to an image", "https://i.imgur.com/zjjcJKZ.png")], matches) 

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "This is [a link to an image](https://i.imgur.com/zjjcJKZ.png), here is [another link to the same image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("a link to an image", "https://i.imgur.com/zjjcJKZ.png"), ("another link to the same image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    