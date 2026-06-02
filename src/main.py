import os
import shutil

from .file_system import copy_static_to_public, generate_page

static_dir = "./static"
public_dir = "./public"
content_dir = "./content"
template_path = "./template.html"

def main():
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)

    copy_static_to_public(static_dir, public_dir)

    generate_page(
        os.path.join(content_dir, "index.md"), 
        template_path, 
        os.path.join(public_dir, "index.html")
    )

main()