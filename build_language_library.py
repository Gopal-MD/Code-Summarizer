import os
import subprocess
from tree_sitter import Language

# Ensure the build directory exists
os.makedirs('build', exist_ok=True)

# List of Tree-Sitter grammars
languages = [
    'tree-sitter-python',
    'tree-sitter-javascript',
    'tree-sitter-java',
    'tree-sitter-go',
    'tree-sitter-rust',
    'tree-sitter-cpp'
]

# Function to compile C++ scanner files with correct flags
def compile_cpp_scanner():
    cpp_scanner_path = 'tree-sitter-cpp/src/scanner.c'
    output_object = 'tree-sitter-cpp/src/scanner.o'

    if os.path.exists(cpp_scanner_path):
        print("🔄 Compiling C++ scanner for Tree-Sitter C++...")
        try:
            subprocess.run([
                'clang++', '-std=c++11', '-fPIC', '-Itree-sitter-cpp/src', 
                '-c', cpp_scanner_path, '-o', output_object
            ], check=True)
            print("✅ C++ Scanner compiled successfully!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error during compilation: {e}")
            exit(1)
    else:
        print(f"⚠️ Scanner file not found: {cpp_scanner_path}")

# Compile the C++ scanner before building the library
compile_cpp_scanner()

# Force clang++ for Tree-Sitter compilation
print("🔄 Building Tree-Sitter language library...")
try:
    env = os.environ.copy()
    env["CC"] = "clang++"  # Force C++ compiler
    env["CXX"] = "clang++"

    Language.build_library(
        os.path.abspath('build/my-languages.so'),
        [os.path.abspath(lang) for lang in languages]
    )
    print("✅ Successfully built Tree-Sitter language library!")
except Exception as e:
    print(f"❌ Failed to build Tree-Sitter library: {e}")
    exit(1)
