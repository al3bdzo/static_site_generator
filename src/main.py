import os
import shutil
import sys

from .file_system import copy_static_to_public, generate_pages_recursive

static_dir = "./static"
public_dir = "./docs"
content_dir = "./content"
template_path = "./template.html"

def main():
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    
    basepath = "/"
    if sys.argv[0]:
        basepath = sys.argv[0]

    copy_static_to_public(static_dir, public_dir)

    generate_pages_recursive(
        content_dir,
        template_path, 
        public_dir,
        basepath
    )
    


main()