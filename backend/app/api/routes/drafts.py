from fastapi import APIRouter, HTTPException, status

from app.schemas.draft import DraftFromTranscriptRequest
from app.schemas.quote import QuoteDraft
from app.services.quote_parser_service import QuoteParserError, parse_transcript_to_quote

router = APIRouter(prefix="/drafts", tags=["drafts"])


@router.post("/from-transcript", response_model=QuoteDraft)
def create_draft_from_transcript(request: DraftFromTranscriptRequest) -> QuoteDraft:
    transcript = request.transcript.strip()
    if not transcript:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Transcript must not be empty.",
        )

    try:
        return parse_transcript_to_quote(transcript)
    except QuoteParserError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to generate a quote draft right now.",
        ) from exc
