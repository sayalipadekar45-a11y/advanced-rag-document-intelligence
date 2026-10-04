from flask import Flask, render_template, request, jsonify
from rag.pipeline import RAGPipeline
from pathlib import Path
import uuid


app = Flask(__name__)

UPLOAD_FOLDER = Path("data")
UPLOAD_FOLDER.mkdir(exist_ok=True)

pipeline = None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_documents():

    global pipeline

    files = request.files.getlist("files")

    if not files:
        return jsonify({
            "error": "No files uploaded."
        }), 400

    allowed_extensions = {
        ".pdf",
        ".docx",
        ".txt"
    }

    saved_files = []

    try:

        # Save all uploaded documents
        for file in files:

            if file.filename == "":
                continue

            extension = Path(file.filename).suffix.lower()

            if extension not in allowed_extensions:
                return jsonify({
                    "error":
                    f"Unsupported file type: {file.filename}"
                }), 400

            safe_name = f"{uuid.uuid4().hex}{extension}"

            file_path = UPLOAD_FOLDER / safe_name

            file.save(file_path)

            saved_files.append(
                (file.filename, str(file_path))
            )

        if not saved_files:
            return jsonify({
                "error": "No valid files selected."
            }), 400

        # Extract paths
        file_paths = [
            path
            for _, path in saved_files
        ]

        # Build multi-document RAG pipeline
        pipeline = RAGPipeline(file_paths)

        return jsonify({

            "message":
            "Documents processed successfully.",

            "files": [
                name
                for name, _ in saved_files
            ],

            "chunks":
            len(pipeline.chunks)

        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


@app.route("/ask", methods=["POST"])
def ask_question():

    if pipeline is None:
        return jsonify({
            "error":
            "Please upload documents first."
        }), 400

    data = request.get_json()

    question = data.get(
        "question",
        ""
    ).strip()

    if not question:
        return jsonify({
            "error":
            "Please enter a question."
        }), 400

    try:

        result = pipeline.ask(question)

        return jsonify(result)

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":

    app.run(
        debug=True
    )