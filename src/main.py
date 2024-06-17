from os.path import isfile
from textnode import TextNode
import os
from pathlib import Path
import shutil

def movedirtodir(path_from: str = "static", path_to: str = "public") -> None:
    ROOT_DIR = Path(__file__).resolve().parent.parent

    path_from_abs = os.path.join(ROOT_DIR, path_from)
    path_to_abs = os.path.join(ROOT_DIR, path_to)

    Path(path_to_abs).mkdir(parents = True, exist_ok = True)

    with os.scandir(path_to_abs) as target_dir:
        for element in target_dir:
            if element.is_file() or element.is_symlink():
                os.unlink(element.path)
            elif element.is_dir():
                shutil.rmtree(element.path)


    with os.scandir(path_from_abs) as elements:
        for element in elements:
            path_from_el = os.path.join(path_from_abs, element)
            path_to_el = os.path.join(path_to_abs, element.name)
            print(f"Moving {path_from_el} to {path_to_el}.....")
            if element.is_dir():
               movedirtodir(path_from_el, path_to_el)
            elif element.is_file():
               shutil.copy(path_from_el, path_to_el)
            print("Success!")

if __name__  == "__main__":
    movedirtodir()



