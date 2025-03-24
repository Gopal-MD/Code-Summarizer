from src.parse_code import parse_code
from src.summarize import summarize_code
from src.review import review_code

def main(file_path):
    tree = parse_code(file_path)
    code_snippet = "extracted code snippet from tree"  # Implement code to extract snippet from tree
    summary = summarize_code(code_snippet)
    issues = review_code(code_snippet)

    print("Summary:")
    print(summary)
    print("\nReview Issues:")
    for issue in issues:
        print(issue)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python main.py <file_path>")
    else:
        main(sys.argv[1])