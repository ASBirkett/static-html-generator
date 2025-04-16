from textnode import  TextNode, TextType
from htmlnode import HTMLNode

def main():
    test_node = TextNode("Some test text", TextType.TEXT, "www.google.com")
    print(test_node)

    
    test_html_node = HTMLNode("<p>", "Hello world", props={"style":"color: red", "class": "fw-bold"})
    print(test_html_node)

    inner_test_html_node = HTMLNode("<img>", props={"src": "https://www.boot.dev/img/bootdev-logo-full-small.webp", "width": 300, "height": 150})
    test_html_node_two = HTMLNode("<p>", "Hello world!", children=[inner_test_html_node], props={"style":"color: red", "class": "fw-bold"})
    print(test_html_node_two)
    

if __name__ == "__main__":
    main()