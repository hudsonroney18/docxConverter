# DOCX to Text Webhook

Public webhook service for n8n Cloud workflows.

## Endpoint

- `POST /webhook/docx-to-text`
- Optional auth: `Authorization: Bearer <WEBHOOK_TOKEN>`

Supported request bodies:
- `multipart/form-data` with a DOCX file in any file field
- `application/octet-stream` raw DOCX bytes

Response:

```json
{
  "text": "Extracted text from docx..."
}
```

## Local Run

```bash
pip install -r requirements.txt
python3 docConverter.py
```

## Render Deploy

This repo includes `render.yaml` and `Procfile`.

1. Create a new Render Blueprint/Web Service from this repo.
2. Set environment variable:
   - `WEBHOOK_TOKEN` (recommended)
3. Deploy.

## n8n Cloud Setup

Use an `HTTP Request` node:

- Method: `POST`
- URL: `https://<your-render-domain>/webhook/docx-to-text`
- Send Binary Data: `true`
- Binary Property: `data` (or your incoming binary property)
- Headers:
  - `Content-Type: application/octet-stream`
  - `Authorization: Bearer <WEBHOOK_TOKEN>` (if enabled)

Output JSON will contain `text`.
