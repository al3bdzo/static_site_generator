
import unittest

from src.htmlnode import HTMLNode, LeafNode, ParentNode

class TextHTMLNode(unittest.TestCase):
    def test_props(self):
        props = {
            "href" : "https://example.com",
            "target" : "_blank"
        }
        node = HTMLNode(tag='a', value='some text here', props=props)
        props_repr = f' href="https://example.com" target="_blank"'

        self.assertEqual(node.props_to_html(), props_repr)

    def test_children(self):
        node1 = HTMLNode(value='one thing')
        node2 = HTMLNode(value='two thing')
        node = HTMLNode(tag='p', value='things happen\nand happen again', children=[node1, node2])
        child = [node1, node2]
        self.assertEqual(node.children, child)
    
    def test_values(self):
        node = HTMLNode(tag='h1', value='things happen\nand happen again')
        s = "things happen\nand happen again"
        self.assertEqual(node.value, s)

    def test_tag(self):
        node = HTMLNode(tag='p')
        s = 'p'
        self.assertEqual(node.tag, s)

    def test_to_html(self):
        node = HTMLNode(tag='p')

        with self.assertRaises(NotImplementedError):
            node.to_html()
        
    
class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_with_props(self):
        props = {
            "href" : "https://google.com",
            "target" : "_blank"
        }
        node = LeafNode("a", "google", props)
        self.assertEqual(node.to_html(), '<a href="https://google.com" target="_blank">google</a>')
    
    def test_leaf_with_no_value(self):
        node = LeafNode('h1', None)

        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_leaf_with_no_tag(self):
        node = LeafNode(None, 'some text here')
        self.assertEqual(node.to_html(), 'some text here')


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
    
    def test_to_html_with_multiple_children(self):
        child1 = LeafNode("span", "child1")
        child2 = LeafNode("div", "child2")
        child3 = LeafNode(None, "lastChild")
        parent_node = ParentNode("p", [child1, child2, child3])
        self.assertEqual(
            parent_node.to_html(),
            "<p><span>child1</span><div>child2</div>lastChild</p>"
        )
    
    def test_to_html_with_nested_parents(self):
        props = {
            "href" : "https://google.com",
            "target" : "_blank"
        }
        grand_child1 = LeafNode("h1", "grand child1")
        grand_child2 = LeafNode("h1", "grand child2")
        child1 = ParentNode("p", [grand_child1])
        child2 = ParentNode("p", [grand_child2], props=props)
        grand_parent = ParentNode("body", [child1, child2])
        grand_grand_parent = ParentNode("html", [grand_parent])

        self.assertEqual(
            grand_grand_parent.to_html(),
            '<html><body><p><h1>grand child1</h1></p><p href="https://google.com" target="_blank"><h1>grand child2</h1></p></body></html>'
        )


