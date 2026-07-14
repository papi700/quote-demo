# Voice Note to Quote

Voice Note to Quote is a 14-day demo app for turning a painter's pasted job notes into a reviewable customer quote. It generates structured, locally editable painting quote drafts through Gemini, with a deterministic fallback when no API key is configured. A separate deterministic pricing worksheet calculates a suggested estimating range while leaving the final customer price under the painter's control. Persistence, messaging, transcription, and audio capture are intentionally not implemented yet.

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

To enable Gemini parsing, set the server-side key in `backend/.env`:

```env
GOOGLE_API_KEY=your_key_here
```

Without a key, the draft endpoint returns a deterministic demo quote so the local flow remains usable. Never place this key in frontend code or a `VITE_` environment variable.

## Frontend setup

Install Node.js 18+ and npm, then run:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. The frontend defaults to `http://127.0.0.1:8000` for API requests. Set `VITE_API_BASE_URL` in a local frontend environment file if the backend runs elsewhere.

## Current status

- Health and transcript draft endpoints are working and covered by tests.
- Gemini 2.5 Flash-Lite produces schema-validated painter quote drafts when configured. If Google reports that model as unavailable to a new API user, the backend retries Google's `gemini-flash-lite-latest` compatibility alias.
- `POST /quotes/calculate-pricing` calculates a deterministic suggested range from painter-entered labor, allowance, markup, and risk inputs. It never calls Gemini.
- The demo UI renders editable quote fields, a pricing worksheet, a clearly marked internal painter review, and a separate customer-facing preview.
- Suggested ranges, calculation details, missing fields, and confidence notes stay in the internal review; the customer preview shows only the painter-approved final price and customer-ready scope.
- Audio, quote retrieval, and message routes remain explicit placeholders.
- No database, authentication, messaging, or audio capture is included.

## Next development milestones

1. Validate quote extraction and pricing defaults with painter feedback.
2. Add transcription and browser audio capture.
3. Add persistence for customers and quote drafts.
4. Add message delivery and follow-up workflows.
5. Add end-to-end validation and deployment configuration.
