from tree_sitter import Language, Parser
import os

# Build the Tree-sitter library if not already built
if not os.path.exists('build/my-languages.so'):
    Language.build_library(
        'build/my-languages.so',
        [
            'tree-sitter-python',
            'tree-sitter-javascript',
            'tree-sitter-java',
            'tree-sitter-go',
            'tree-sitter-rust',
            'tree-sitter-cpp'
        ]
    )

# Load the languages
PY_LANGUAGE = Language('build/my-languages.so', 'python')
JS_LANGUAGE = Language('build/my-languages.so', 'javascript')
JAVA_LANGUAGE = Language('build/my-languages.so', 'java')
GO_LANGUAGE = Language('build/my-languages.so', 'go')
RUST_LANGUAGE = Language('build/my-languages.so', 'rust')
CPP_LANGUAGE = Language('build/my-languages.so', 'cpp')

PARSERS = {
    'python': PY_LANGUAGE,
    'javascript': JS_LANGUAGE,
    'java': JAVA_LANGUAGE,
    'go': GO_LANGUAGE,
    'rust': RUST_LANGUAGE,
    'cpp': CPP_LANGUAGE
}

EXTENSIONS = {
    '.py': 'python',
    '.js': 'javascript',
    '.java': 'java',
    '.go': 'go',
    '.rs': 'rust',
    '.cpp': 'cpp',
    '.c': 'cpp',
    '.h': 'cpp'
}

def parse_code(file_path, language=None):
    """
    Parses the code file using Tree-sitter and returns the syntax tree.

    Args:
        file_path (str): The path to the code file.
        language (str): The programming language of the code file. If not provided, it will be inferred from the file extension.

    Returns:
        tree_sitter.Tree: The syntax tree of the code file.
    """
    if language is None:
        _, ext = os.path.splitext(file_path)
        if ext in EXTENSIONS:
            language = EXTENSIONS[ext]
        else:
            raise ValueError(f"Unsupported file extension: {ext}")

    if language not in PARSERS:
        raise ValueError(f"Unsupported language: {language}")

    parser = Parser()
    parser.set_language(PARSERS[language])
    
    with open(file_path, 'r') as file:
        code = file.read()

    tree = parser.parse(bytes(code, 'utf8'))
    return tree