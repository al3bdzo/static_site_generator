import unittest

from src.split_nodes import split_nodes_delimiter
from src.textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_one_odd_nest(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), expected)
    
    def test_one_even_nest(self):
        node = TextNode("**bold block** is at the beginning", TextType.TEXT)
        expected = [
            TextNode("bold block", TextType.BOLD),
            TextNode(" is at the beginning", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), expected)
    
    def test_multiple_codes(self):
        node = TextNode("**bold block** is at the beginning and another **bold block** at the middle, and another at the end **bold block**", TextType.TEXT)
        expected = [
            TextNode("bold block", TextType.BOLD),
            TextNode(" is at the beginning and another ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode(" at the middle, and another at the end ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD)
        ]
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), expected)
    
    def test_multiple_nodes(self):
        node1 = TextNode("This is text with a _italic block_ word", TextType.TEXT)
        node2 = TextNode("_italic block_ is at the beginning", TextType.TEXT)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic block", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
            TextNode("italic block", TextType.ITALIC),
            TextNode(" is at the beginning", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_delimiter([node1, node2], "_", TextType.ITALIC), expected)
    
    def test_unclosed_delimiter(self):
        node = TextNode("This _italic must give an error", TextType.TEXT)

        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "_", TextType.ITALIC)

