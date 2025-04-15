import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_nested_parent_children(self):
        child_node = LeafNode("span", "Hello world")
        parent_node = ParentNode("div", [child_node])
        parent_node_two = ParentNode("div", [parent_node])
        parent_node_three = ParentNode("article", [parent_node_two])

        self.assertEqual(
            parent_node_three.to_html(),
            "<article><div><div><span>Hello world</span></div></div></article>"
        )

    def test_to_html_with_multiple_parent_children(self):
        child_node_one = LeafNode("span", "Hello world")
        parent_node_one = ParentNode("div", [child_node_one])
        child_node_two = LeafNode("h4", "Hello new world")
        parent_node_two = ParentNode("div", [child_node_two])
        root_parent_node = ParentNode("article", [parent_node_one, parent_node_two])

        self.assertEqual(
            root_parent_node.to_html(),
            "<article><div><span>Hello world</span></div><div><h4>Hello new world</h4></div></article>"
        )
    
    def test_to_html_with_multiple_leaf_children(self):
        child_node_one = LeafNode("span", "Hello world")
        child_node_two = LeafNode("h4", "Hello new world")
        root_parent_node = ParentNode("article", [child_node_one, child_node_two])

        self.assertEqual(
            root_parent_node.to_html(),
            "<article><span>Hello world</span><h4>Hello new world</h4></article>"
        )