from flask import Flask, request, render_template, jsonify
import os
from src.parse_code import parse_code
from src.summarize import chunk_code, summarize_code_gemini  # ✅ Updated function import

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    """Handles both Web (file upload) and CLI-based API requests."""

    # ✅ If request comes from CLI (JSON input)
    if request.is_json:
        data = request.get_json()
        code = data.get("code", "")
        if not code:
            return jsonify({"error": "No code provided"}), 400

        # ✅ Debugging: Print received code snippet
        print(f"📥 Received Code: {code[:100]}...")  # Show first 100 chars

        # ✅ Chunk and summarize using Gemini AI API
        chunks = chunk_code(code)
        summaries = [summarize_code_gemini(chunk) for chunk in chunks]
        final_summary = " ".join(summaries)

        return jsonify({"summary": final_summary})

    # ✅ If request comes from Web UI (File Upload)
    if 'code_file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['code_file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        file_path = os.path.join('/tmp', file.filename)
        file.save(file_path)

        language = request.form.get('language', 'python')  # Default to Python
        tree = parse_code(file_path, language)

        # ✅ Ensure correct decoding
        try:
            code_snippet = " ".join([node.text.decode('utf-8') for node in tree.root_node.children])
        except AttributeError:
            return jsonify({"error": "Failed to parse code"}), 500

        print(f"📥 Parsed Code Snippet: {code_snippet[:100]}...")  # Show first 100 chars

        chunks = chunk_code(code_snippet)
        summaries = [summarize_code_gemini(chunk) for chunk in chunks]
        final_summary = " ".join(summaries)

        return render_template('summary.html', summary=final_summary)

if __name__ == '__main__':
    app.run(debug=True)
