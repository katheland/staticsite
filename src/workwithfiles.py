import os
import shutil
from markdowntohtml import markdown_to_html_node
from blockhelpers import extract_title

# first we clear the public directory
def clear_directory(destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)

# copies contents from source directory to destination directory
def copy_to_dir(source, destination):
    if not os.path.exists(source):
        raise Exception(f"path {source} doesn't exist?")
    if not os.path.exists(destination):
        os.mkdir(destination)
    for item in os.listdir(source):
        item_path = os.path.join(source, item)
        if os.path.isdir(item_path):
            copy_to_dir(item_path, os.path.join(destination, item))
        else:
            print(f"copyiing {item_path} to {destination}")
            shutil.copy(item_path, destination)

# generates a webpage from markdown
def generate_page(from_path, template_path, dest_path, basepath):
    print(f"generating page from {from_path} to {dest_path} using {template_path}")
    
    # first we read the source files
    markdown_text = ""
    with open(from_path) as f:
        markdown_text = f.read()
    template_text = ""
    with open(template_path) as f:
        template_text = f.read()
    
    # next we convert the html, grab the title, and insert them into the template
    markdown_html = markdown_to_html_node(markdown_text).to_html()
    title = extract_title(markdown_text)
    new_page = template_text.replace("{{ Title }}", title).replace("{{ Content }}", markdown_html).replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    
    # and now we write this to a new file at dest_path
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, mode='x') as f:
        f.write(new_page)
    
# recursively crawls the content directory and generates html files for every markdown file found
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    print(f"generating pages recursively from {dir_path_content} to {dest_dir_path} using {template_path}")
    dir_contents = os.listdir(dir_path_content)
    for content in dir_contents:
        from_path = os.path.join(dir_path_content, content)
        print(f"{from_path}: {os.path.isfile(from_path)}")
        if os.path.isdir(from_path):
            dest_path = os.path.join(dest_dir_path, content)
            os.mkdir(dest_path)
            generate_pages_recursive(from_path, template_path, dest_path, basepath)
        elif os.path.isfile(from_path):
            dest_file = os.path.join(dest_dir_path, os.path.splitext(content)[0]) + ".html"
            print(f"generate_page({from_path}, {template_path}, {dest_file})", basepath)
            generate_page(from_path, template_path, dest_file, basepath)
        else:
            raise Exception("How are we here?")
