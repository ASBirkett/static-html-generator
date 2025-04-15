import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        html_node = HTMLNode("<p>", "Hello world", props={"style":"color: red"})
        self.assertEqual(" style=\"color: red\"", html_node.props_to_html())

    def test_children_type(self):
        child_node = HTMLNode("<div>", "Says the script")
        html_node = HTMLNode("<p>", "Hello world", children=[child_node], props={"style":"color: red"})
        for x in range(len(html_node.children)):
            self.assertIsInstance(html_node.children[x], HTMLNode)

if __name__ == "__main__":
    unittest.main()