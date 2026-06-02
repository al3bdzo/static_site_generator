import os 
import shutil

from .markdown_to_html import markdown_to_html_node, extract_title

def copy_static_to_public(source, dest):
    if not os.listdir(source):
        return

    if not os.path.exists(dest):
        os.mkdir(dest)

    for item in os.listdir(source):
        source_in = os.path.join(source, item)
        if os.path.isfile(source_in):
            print(f"copying {item} from {source} to {dest}")
            shutil.copy(source_in, dest)
        else:
            print(f"going to {os.path.join(source, item)}")
            dest_in = os.path.join(dest, item)
            copy_static_to_public(source_in, dest_in)


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    if os.path.exists(from_path):
        with open(from_path, "r") as file:
            md = file.read()
    else:
        raise Exception("No md file to translate")

    with open(template_path, "r") as file: 
        template = file.read()
    
    node = markdown_to_html_node(md)
    html = node.to_html()
    title = extract_title(md)

    index_html = template.replace("{{ Title }}", title)
    index_html = index_html.replace("{{ Content }}", html)
    index_html = index_html.replace('href="/', f'href="{basepath}')
    index_html = index_html.replace('src="/', f'src="{basepath}')

    
    dest_dir_path = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path, exist_ok = True)

    with open(dest_path, "w") as file: 
        file.write(index_html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    if not os.listdir(dir_path_content):
        return 
    
    for item in os.listdir(dir_path_content):
        source = os.path.join(dir_path_content, item)
        if os.path.isfile(source):
            dest = os.path.join(dest_dir_path, "index.html")
            generate_page(source, template_path, dest, basepath)
        else:
            dest = os.path.join(dest_dir_path, item)
            generate_pages_recursive(source, template_path, dest, basepath)
