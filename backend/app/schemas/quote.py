from pydantic import BaseModel, Field


class QuoteDraft(BaseModel):
    """Editable residential painting quote extracted from a transcript."""

    customer_name: str | None = None
    customer_phone: str | None = None
    customer_email: str | None = None
    city: str | None = None
    job_address: str | None = None
    job_type: str | None = None
    rooms_or_areas: list[str] = Field(default_factory=list)
    included_work: list[str] = Field(default_factory=list)
    excluded_work: list[str] = Field(default_factory=list)
    prep_work: list[str] = Field(default_factory=list)
    paint_finish: str | None = None
    number_of_coats: str | None = None
    price_before_tax: float | None = Field(default=None, ge=0)
    tax_note: str | None = None
    timeline: str | None = None
    customer_message: str | None = None
    missing_fields: list[str] = Field(default_factory=list)
    confidence_notes: list[str] = Field(default_factory=list)
