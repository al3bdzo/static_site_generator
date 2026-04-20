import unittest

from src.block import markdown_to_blocks, BlockType, block_to_block_type


class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_block_to_block_type(self):
        blocks = [
            "- This is a list\n- It's unordered", 
            "1. This list on the other hand\n2. is ordered",
            "##### this is a heading",
            "```\nthis is a code block\nIt has multiplelines\n```",
            "> this is a quote",
            ">this is another quote",
            "this is a normal paragraph.\nI am writing stuff here."
        ]
        expected = [
            BlockType.ULIST,
            BlockType.OLIST,
            BlockType.HEADING,
            BlockType.CODE,
            BlockType.QUOTE,
            BlockType.QUOTE,
            BlockType.PARAGRAPH
        ]
        result = []
        for block in blocks:
            result.append(block_to_block_type(block))

        self.assertListEqual(expected, result)