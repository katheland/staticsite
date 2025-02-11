from workwithfiles import *

def main():
    clear_directory("public")
    copy_to_dir("static", "public")
    generate_pages_recursive("content", "template.html", "public")

main()