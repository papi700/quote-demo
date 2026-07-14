from pydantic import BaseModel


class DraftFromTranscriptRequest(BaseModel):
    transcript: str
