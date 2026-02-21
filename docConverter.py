from io import BytesIO
import os

from docx import Document
from flask import Flask, jsonify, request


app = Flask(__name__)
MAX_UPLOAD_BYTES = 20 * 1024 * 1024  # 20MB
WEBHOOK_TOKEN = os.getenv("WEBHOOK_TOKEN")


def extract_docx_text(docx_bytes: bytes) -> str:
    document = Document(BytesIO(docx_bytes))
    lines = [paragraph.text for paragraph in document.paragraphs]
    return "\n".join(lines).strip()


@app.get("/health")
def health_check():
    return jsonify({"ok": True}), 200


@app.post("/webhook/docx-to-text")
def docx_to_text():
    """
    Accepts:
    1) multipart/form-data with any file field
    2) raw application/octet-stream body containing the .docx file
    """
    if WEBHOOK_TOKEN:
        auth_header = request.headers.get("Authorization", "")
        expected = f"Bearer {WEBHOOK_TOKEN}"
        if auth_header != expected:
            return jsonify({"error": "Unauthorized"}), 401

    file_bytes = None

    if request.files:
        first_file = next(iter(request.files.values()))
        if not first_file or not first_file.filename:
            return jsonify({"error": "No file provided"}), 400
        file_bytes = first_file.read()
    else:
        raw = request.get_data()
        if raw:
            file_bytes = raw

    if not file_bytes:
        return jsonify({"error": "No file content received"}), 400

    if len(file_bytes) > MAX_UPLOAD_BYTES:
        return jsonify({"error": "File is too large", "max_bytes": MAX_UPLOAD_BYTES}), 413

    try:
        text = extract_docx_text(file_bytes)
    except Exception:
        return jsonify({"error": "Invalid DOCX or failed to parse document"}), 400

    return jsonify({"text": text}), 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    app.run(host="0.0.0.0", port=port, debug=False)
