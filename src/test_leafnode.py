import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_raw(self):
        node = LeafNode(None, "This is a raw text leaf node")
        self.assertEqual(node.to_html(), "This is a raw text leaf node")

    def test_leaf_to_img(self):
        node = LeafNode("img", "This is alt text", { "src" : "https://www.boot.dev/img/bootdev-logo-full-small.webp", "width" : 120, "height" : 70 })
        self.assertEqual(node.to_html(), "<img src=\"https://www.boot.dev/img/bootdev-logo-full-small.webp\" width=\"120\" height=\"70\">This is alt text</img>")

if __name__ == "__main__":
    unittest.main()