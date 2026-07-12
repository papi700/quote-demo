from fastapi import APIRouter

from app.schemas.draft import DraftFromTranscriptRequest

router = APIRouter(prefix="/drafts", tags=["drafts"])


@router.post("/from-transcript")
def create_draft_from_transcript(request: DraftFromTranscriptRequest) -> dict[str, str]:
    return {
        "status": "not_implemented",
        "message": "Transcript-to-draft parsing is not implemented yet.",
        "transcript": request.transcript,
    }
