import unittest

from src.split_nodes import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
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

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_multi_images(self):
        matches = extract_markdown_images(
            "This is text with multiple ![image](https://i.imgur.com/zjjcJKZ.png) ![another image](https://i.imgur.com/something.png) images [noise](more noise) [link](https://example.com)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("another image", "https://i.imgur.com/something.png")], matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with multiple [link](https://example.com) links [another link](https://google.com) [noise] (more noise) ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://example.com"), ("another link", "https://google.com")], matches)

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
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
    
    def test_split_links(self):
        node = TextNode(
            "[link](https://example.com)[second link](https://google.com) and something here",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode("second link", TextType.LINK, "https://google.com"),
                TextNode(" and something here", TextType.TEXT)
            ],
            new_nodes,
        )
