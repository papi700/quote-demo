# Voice Note to Quote

Voice Note to Quote is a 14-day demo app for turning a painter's spoken or pasted job notes into a reviewable customer quote. This repository currently contains only the working scaffold; transcription, AI parsing, persistence, messaging, and audio capture are intentionally not implemented yet.

## Architecture

- `frontend/`: React and Vite mobile-friendly painter UI
- `backend/`: FastAPI API managed with `uv`

The frontend calls the backend through a small API client. FastAPI enables CORS for the local Vite development origins.

## Backend setup

Install [`uv`](https://docs.astral.sh/uv/) and run:

```bash
cd backend
uv sync
uv run fastapi dev app/main.py
```

The API runs at `http://127.0.0.1:8000`. Check `http://127.0.0.1:8000/health` or browse the interactive docs at `http://127.0.0.1:8000/docs`.

Run tests with:

```bash
cd backend
uv run pytest
```

Copy `backend/.env.example` to `backend/.env` to override local settings when needed.

## Frontend setup

Install Node.js 18+ and npm, then run:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. The frontend defaults to `http://127.0.0.1:8000` for API requests. Set `VITE_API_BASE_URL` in a local frontend environment file if the backend runs elsewhere.

## Current status

- Health endpoint and automated health test are working.
- Draft, audio, quote, and message routes return explicit placeholder responses.
- The demo UI shows the intended workflow and can call the draft placeholder endpoint.
- No production product logic or external services are included.

## Next development milestones

1. Define the quote draft contract and transcript parsing behavior.
2. Add transcription and browser audio capture.
3. Implement editable draft and customer quote rendering.
4. Add persistence, message delivery, and follow-up workflows.
5. Add end-to-end validation and deployment configuration.
