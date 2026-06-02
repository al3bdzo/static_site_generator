import os 
import shutil

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
