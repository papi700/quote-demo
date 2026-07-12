from fastapi import APIRouter

router = APIRouter(prefix="/audio", tags=["audio"])


@router.post("/transcribe")
def transcribe_audio() -> dict[str, str]:
    return {
        "status": "not_implemented",
        "message": "Audio transcription is not implemented yet.",
    }
