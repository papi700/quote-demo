from pydantic import BaseModel, Field


class DraftFromTranscriptRequest(BaseModel):
    transcript: str = Field(min_length=1)
