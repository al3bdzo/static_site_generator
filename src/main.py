import os
import shutil

from file_system import copy_static_to_public

static_dir = "./static"
public_dir = "./public"

def main():
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)

    copy_static_to_public(static_dir, public_dir)


main()