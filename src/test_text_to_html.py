import unittest

from textnode import TextNode, TextType
from htmlnode import LeafNode 
from text_to_html import text_node_to_html_node

class TestTextToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, "bold text")
    
    def test_link(self):
        node = TextNode("GOOGLE", TextType.LINK, url="https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, "GOOGLE")
        self.assertEqual(html_node.props, {"href": "https://google.com"})
    
    def test_unsupported_type(self):
        node = TextNode("something", "new type")
        
        with self.assertRaises(Exception):
            html_node = text_node_to_html_node(node)