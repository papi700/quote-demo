from pydantic import BaseModel, Field

from app.schemas.customer import Customer


class QuoteLineItem(BaseModel):
    description: str
    amount: float = Field(ge=0)


class QuoteDraft(BaseModel):
    customer: Customer | None = None
    summary: str = ""
    line_items: list[QuoteLineItem] = Field(default_factory=list)
    notes: str = ""
