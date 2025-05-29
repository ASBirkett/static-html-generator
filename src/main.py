from textnode import  TextNode, TextType
from htmlnode import HTMLNode
from textnode_parser_helper import generate_page

import os
import sys
import shutil

SOURCE_DIR = './static'
DESTINATION_DIR = './docs'

SOURCE_CONTENT = './content'
SOURCE_TEMPLATE = './template.html'

def main():
    basepath = "/" if len(sys.argv) <= 1 else sys.argv[1]
    if clear_folder_contents(DESTINATION_DIR):
        print("Cleared destination directory complete")
        if copy_contents_of_source_to_destination(SOURCE_DIR, DESTINATION_DIR):
            print("Copied static contents complete")
            generate_pages_recursive(SOURCE_CONTENT, SOURCE_TEMPLATE, DESTINATION_DIR, basepath)
        else:
            print("Copy failed")
    else:
        print("Content clear failed")
    

def clear_folder_contents(source_dir: str) -> bool:
    print(f"Validating directory: {source_dir}")
    if(not os.path.exists(source_dir)):
        raise Exception("Path does not exist")
    
    print(f"Gethering files and directories")
    contents = os.listdir(source_dir)
    try:
        for content in contents:
            full_path = os.path.join(source_dir, content)
            if os.path.isdir(full_path):
                print(f"Directory found, going into directory: {full_path}")
                clear_folder_contents(full_path)
                print("Deleting folder...")
                os.rmdir(full_path)
            else:
                print(f"Deleting: {full_path}")
                os.remove(full_path)
    except Exception as e:
        print(f"An error has occurred, please resolve this issue and try again: {e}")
        return False
    
    return True

def copy_contents_of_source_to_destination(source_dir: str, destination_dir: str) -> bool:
    print(f"Validating source directory: {source_dir}")
    if(not os.path.exists(source_dir)):
        raise Exception("Source directory does not exist")
    
    print(f"Validating destination directory: {destination_dir}")
    if(not os.path.exists(destination_dir)):
        raise Exception("Destination directory does not exist")
    
    print("Gathering source files and directories")
    source_list = os.listdir(source_dir)
    try:
        for content in source_list:
            current_src_path = os.path.join(source_dir, content)
            current_dest_path = os.path.join(destination_dir, content)
            if os.path.isdir(current_src_path):
                print(f"Creating sub directory: {current_dest_path}")
                os.mkdir(current_dest_path)
                print(f"Going into directory: {current_dest_path}")
                copy_contents_of_source_to_destination(current_src_path, current_dest_path)
            else:
                print(f"Copying {current_src_path} to {current_dest_path}")
                shutil.copy(current_src_path, current_dest_path)
    except Exception as e:
        print(f"An error has occurred while copying content: {e}")
        return False

    return True

def generate_pages_recursive(source_dir: str, page_template: str, destination_dir: str, basepath: str) -> bool:
    print(f"Validating source directory: {source_dir}")
    if(not os.path.exists(source_dir)):
        raise Exception("Source directory does not exist")
    
    print(f"Validating destination directory: {destination_dir}")
    if(not os.path.exists(destination_dir)):
        raise Exception("Destination directory does not exist")
    
    source_list = os.listdir(source_dir)
    try:
        for content in source_list:
            current_src_path = os.path.join(source_dir, content)
            current_dest_path = os.path.join(destination_dir, content)
            if os.path.isdir(current_src_path):
                print(f"Creating sub directory: {current_dest_path}")
                os.mkdir(current_dest_path)
                print(f"Going into directory: {current_dest_path}")
                generate_pages_recursive(current_src_path, page_template, current_dest_path, basepath)
            else:
                filename = os.path.splitext(os.path.basename(current_src_path))[0]
                generate_page(current_src_path, page_template, os.path.join(destination_dir, f"{filename}.html"), basepath)
    except Exception as e:
        print(f"An error has occurred while creating html pages from content files")
        return False

    return True
    


if __name__ == "__main__":
    main()