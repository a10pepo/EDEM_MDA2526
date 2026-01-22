# Exercise 3: API Fundamentals (Notes API)

## Introduction

This exercise introduces core HTTP + JSON API fundamentals using a small Notes API built with Flask. It fits between 02 (Postman) and 03 (Basic Auth) and focuses on clean request/response design and basic validation — no authentication yet.

## Learning Objectives

1. Use HTTP methods correctly (GET/POST) and return proper status codes
2. Validate `Content-Type` and JSON payloads (basic checks)
3. Return consistent error responses and add simple error handlers
4. Practice testing with Postman and curl

## Endpoints

- `GET /health`
  - Returns basic service information
  - Response: `200` with `{ status, service, version }`

- `GET /notes`
  - Returns a list of notes (in-memory)
  - Response: `200` with list `[ { id, title, content } ]`

- `POST /notes`
  - Creates a new note
  - Requires `Content-Type: application/json`
  - Body: `{ "title": str, "content": str }`
  - Response: `201` with created note
  - Errors: `415` (not JSON), `400` (validation errors)

- `GET /notes/<id>`
  - Returns a single note by id
  - Response: `200` on success, `404` if not found

## Requirements

- Use an in-memory store (Python dict) — no database
- Validate requests:
  - Reject non-JSON with `415` and `{ error, message }`
  - Validate required fields with `400` and `{ error, details }`
- Add simple error handlers for `404`, `405` (consistent shape)

## Starter Files

- `app.py` – Starter with TODOs and blanks (`_____`) for you to fill
- `example/example03.py` – Complete reference solution (for after you try)
- `requirements.txt` – Minimal dependencies

## Getting Started

```bash
# (Optional) Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Open your browser: http://127.0.0.1:5000/health

## Tasks (fill the blanks in app.py)

1. Routes and methods
   - Add HTTP methods for each route
2. Content-Type validation on `POST /notes`
   - Return `415` if not `application/json`
3. Input validation
   - Ensure `title` and `content` are present and non-empty strings
   - On error, return `400` with a consistent payload
4. Resource creation
   - Generate `id`, return `201` with created note
5. Error handlers
   - Implement `404`, `405` with consistent `{ error, message }`

## Testing (curl)

```bash
# Health
curl -i http://127.0.0.1:5000/health

# Create note (success)
curl -i -X POST http://127.0.0.1:5000/notes \
  -H "Content-Type: application/json" \
  -d '{"title": "First note", "content": "Hello world"}'

# Create note (wrong content-type)
curl -i -X POST http://127.0.0.1:5000/notes -d 'title=bad'

# List notes
curl -i http://127.0.0.1:5000/notes

```

# Get note by id
curl -i http://127.0.0.1:5000/notes/1
```

## Acceptance Criteria

- Correct status codes (`200`, `201`, `404`, `405`, `415`, `400`)
- Consistent error payloads across handlers
- `POST /notes` returns `201` with created note
- No authentication used

## Stretch Goals

- Add `updated_at` if you extend with PUT later
- Add pagination (`?page`/`per_page`) similar to later exercises
- Add simple CORS for browser testing

Good luck building a clean, well-structured API!
