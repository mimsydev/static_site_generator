import os
from pathlib import Path
import shutil
from markdowntohtml import markdown_to_html_node 


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

def extract_title(markdown :str) -> str:
    if markdown:
        splits = markdown.split("\n")
        if not splits[0].startswith("# "):
            raise ValueError(f"The document did not start with a title: {splits[0]}")
        else:
            return splits[0].lstrip("# ")
    else:
        raise ValueError("There was no markdown provided")

def generate_page(from_path: str, template_path: str, dest_path: str, root_path: Path):
    from_path_abs = os.path.join(root_path, from_path)
    dest_path_abs = os.path.join(root_path, dest_path)
    template_path_abs = os.path.join(root_path, template_path)
    
    print(f"Generating page from '{from_path_abs}' to '{dest_path_abs}'"
          f"using '{template_path_abs}'.")

    md: str = ""
    with open(from_path_abs, "r") as file:
        md = file.read()

    template: str = ""
    with open(template_path_abs, "r") as file:
        template = file.read()

    header = extract_title(md)

    content = "\n".join(list(map(lambda n: n.to_html(),
                                 markdown_to_html_node(md))))

    html = template.replace("{{ Title }}", header).replace("{{ Content }}", content)

    target_file = Path(dest_path_abs)
    target_file.parent.mkdir(parents=True, exist_ok=True)
    target_file.write_text(html)

def generate_pages_recursive(dir_path_content: str, 
                             template_path: str, dest_dir_path: str, 
                             root_path: Path = Path("")) -> None:
    if root_path == Path(""):
        root_path = Path(__file__).resolve().parent.parent

    from_path_abs = os.path.join(root_path, dir_path_content)
    dest_path_abs = os.path.join(root_path, dest_dir_path)
    template_path_abs = os.path.join(root_path, template_path)

    with os.scandir(from_path_abs) as elements:
        for element in elements:
            path_from_el = os.path.join(from_path_abs, element.name) 
            if element.is_dir():
                path_to_el = os.path.join(dest_path_abs, element.name)
                return generate_pages_recursive(path_from_el, template_path_abs,
                                                path_to_el, root_path)
            elif element.is_file() and os.path.splitext(element.path)[-1].lower() \
                .endswith(".md"):
                path_to_el = os.path.join(dest_path_abs, element.name)
                generate_page(path_from_el, template_path_abs,
                              path_to_el.replace(".md",".html"), root_path)
    return


def main() -> None:
    movedirtodir()
    generate_pages_recursive(dir_path_content="content/", template_path="template.html",
                  dest_dir_path="public/")

if __name__  == "__main__":
    main()
