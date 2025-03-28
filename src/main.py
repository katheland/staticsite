from workwithfiles import *
import sys

def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    print(f"basepath: {basepath} {sys.argv}")
    clear_directory("docs")
    copy_to_dir("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)

main()