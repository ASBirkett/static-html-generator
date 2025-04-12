from textnode import  TextNode, TextType

def main():
    test_node = TextNode("Some test text", TextType.NORMAL, "www.google.com")
    print(test_node)

if __name__ == "__main__":
    main()