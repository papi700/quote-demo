from pydantic import BaseModel, Field

from app.schemas.quote import QuoteDraft


class PricingWorksheet(BaseModel):
    crew_size: int | None = Field(default=None, ge=1)
    labor_days: float | None = Field(default=None, ge=0)
    labor_rate_per_day: float | None = Field(default=None, ge=0)
    material_allowance: float | None = Field(default=None, ge=0)
    prep_allowance: float | None = Field(default=None, ge=0)
    overhead_profit_percent: float | None = Field(default=None, ge=0)
    risk_buffer_percent: float | None = Field(default=None, ge=0)
    suggested_low_price: float | None = Field(default=None, ge=0)
    suggested_high_price: float | None = Field(default=None, ge=0)
    final_price_before_tax: float | None = Field(default=None, ge=0)
    pricing_notes: list[str] = Field(default_factory=list)


class PricingCalculationRequest(BaseModel):
    quote_draft: QuoteDraft
    pricing_inputs: PricingWorksheet


class PricingCalculationResponse(BaseModel):
    quote_draft: QuoteDraft
    pricing: PricingWorksheet
    calculation_breakdown: list[str] = Field(default_factory=list)
