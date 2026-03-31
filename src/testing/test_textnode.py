import unittest 

from src.textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node = TextNode("This is text", TextType.TEXT)
        node2 = TextNode("This is also text", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_url(self):
        node = TextNode("Something", TextType.LINK, "https://example.com")
        node2 = TextNode("Something", TextType.LINK, "https://example.com")
        self.assertEqual(node, node2)
    
    def test_type(self):
        node = TextNode("NO NO NO", TextType.IMAGE, None)
        node2 = TextNode("NO NO NO", TextType.ITALIC, None)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()