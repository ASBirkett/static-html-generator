from textnode_parser_helper import block_to_block_type
from textnode import BlockType
import unittest

class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_blocktype_paragraph(self):
        block = "This is a paragraph block"

        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))

    def test_block_to_blocktype_code(self):
        block = "```This is a code block```"

        self.assertEqual(BlockType.CODE, block_to_block_type(block))

    def test_block_to_blocktype_heading(self):
        block = "# Heading 1"

        self.assertEqual(BlockType.HEADING, block_to_block_type(block))

    def test_block_to_blocktype_quote(self):
        block = ">This is a quote block"

        self.assertEqual(BlockType.QUOTE, block_to_block_type(block))

    def test_block_to_blocktype_ordered_list(self):
        block = "1. Item 1\n2. item 2\n3. Item 3"

        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(block))

    def test_block_to_blocktype_unordered_list(self):
        block = "- Red\n- Blue\n- Green"

        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(block))

    def test_block_to_blocktype_broken_list_should_return_paragraph(self):
        block = "- Red\n Green\n- Blue"

        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))

    def test_block_to_blocktype_ordered_list_jumped_number_should_return_paragraph(self):
        block = "1. Item 1\n4. Item 4\n5. Item 5"

        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))