from .textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        node_text = node.text.split(delimiter)

        if len(node_text) % 2 == 0:
            raise Exception("Invalid Markdown syntax")

        for i in range(len(node_text)):
            if node_text[i] == "":
                continue
            if i % 2 == 1:
                new_nodes.append(TextNode(node_text[i], text_type))
            else:
                new_nodes.append(TextNode(node_text[i], TextType.TEXT))
    
    return new_nodes