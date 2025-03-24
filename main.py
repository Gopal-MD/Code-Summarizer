import sys
from src.parse_code import parse_code
from src.summarize import summarize_code

def main(file_path):
    tree = parse_code(file_path)
    code_snippet = " ".join([node.text for node in tree.root_node.children])  # Adjust as needed
    summary = summarize_code(code_snippet)
    print("Summary:")
    print(summary)

if __name__ == "__main__":
    main(sys.argv[1])