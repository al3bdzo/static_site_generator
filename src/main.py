import os
import shutil

from .file_system import copy_static_to_public, generate_pages_recursive

static_dir = "./static"
public_dir = "./public"
content_dir = "./content"
template_path = "./template.html"

def main():
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)

    copy_static_to_public(static_dir, public_dir)

    generate_pages_recursive(
        content_dir,
        template_path, 
        public_dir
    )

main()