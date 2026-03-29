from textnode import TextType, TextNode


def main():
    
    node = TextNode("Text and stuff", TextType.BOLD, "https://example.com")
    print(node)


main()