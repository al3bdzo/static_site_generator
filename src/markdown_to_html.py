from .block import markdown_to_blocks, block_to_block_type, BlockType
from .htmlnode import ParentNode
from .split_nodes import text_to_textnodes
from .text_to_html import text_node_to_html_node
from .textnode import TextNode, TextType

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        html_node = block_to_html(block)
        children.append(html_node)

    return ParentNode("div", children)

def text_to_children(text):
    inline_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in inline_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

def block_to_html(block):
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.ULIST:
            return ulist_to_html_node(block)
        case BlockType.OLIST:
            return olist_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case _:
            raise ValueError("unknown block type!")

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == '#':
            level += 1 
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level {level}")
    text = block[level+1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    text_node = TextNode(text, TextType.TEXT)
    html_node = text_node_to_html_node(text_node)
    code = ParentNode("code", [html_node])
    return ParentNode("pre", [code])

def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        parts = item.split(". ", 1)
        if len(parts) != 2:
            raise ValueError("invalid ordered list item")
        text = parts[1]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def quote_to_html_node(block):
    lines = block.split("\n")
    new_line = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_line.append(line.lstrip(">").strip())
    content = " ".join(new_line)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            text = line.strip("#").strip()
            return text
    raise Exception("There's no title for this document!")