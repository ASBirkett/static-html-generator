import unittest

from textnode import TextNode, TextType


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

if __name__ == "__main__":
    unittest.main()