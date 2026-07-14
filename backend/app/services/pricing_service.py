import math

from app.schemas.pricing import PricingCalculationResponse, PricingWorksheet
from app.schemas.quote import QuoteDraft

DEFAULT_OVERHEAD_PROFIT_PERCENT = 25.0
DEFAULT_RISK_BUFFER_PERCENT = 10.0


def _round_to_nearest_fifty(value: float) -> float:
    return float(math.floor((value + 25) / 50) * 50)


def _money(value: float) -> str:
    return f"${value:,.2f}"


def calculate_pricing(
    quote_draft: QuoteDraft,
    pricing_inputs: PricingWorksheet,
) -> PricingCalculationResponse:
    """Calculate a deterministic estimate range without calling an AI service."""

    missing_labor_fields = [
        field
        for field in ("crew_size", "labor_days", "labor_rate_per_day")
        if getattr(pricing_inputs, field) is None
    ]

    if missing_labor_fields:
        labor_cost = 0.0
    else:
        labor_cost = (
            pricing_inputs.crew_size
            * pricing_inputs.labor_days
            * pricing_inputs.labor_rate_per_day
        )

    material_allowance = pricing_inputs.material_allowance or 0.0
    prep_allowance = pricing_inputs.prep_allowance or 0.0
    overhead_profit_percent = (
        pricing_inputs.overhead_profit_percent
        if pricing_inputs.overhead_profit_percent is not None
        else DEFAULT_OVERHEAD_PROFIT_PERCENT
    )
    risk_buffer_percent = (
        pricing_inputs.risk_buffer_percent
        if pricing_inputs.risk_buffer_percent is not None
        else DEFAULT_RISK_BUFFER_PERCENT
    )

    base_cost = labor_cost + material_allowance + prep_allowance
    unrounded_low = base_cost * (1 + overhead_profit_percent / 100)
    unrounded_high = unrounded_low * (1 + risk_buffer_percent / 100)
    suggested_low = _round_to_nearest_fifty(unrounded_low)
    suggested_high = _round_to_nearest_fifty(unrounded_high)

    final_price = pricing_inputs.final_price_before_tax
    if final_price is None:
        final_price = quote_draft.price_before_tax

    calculation_breakdown = [
        f"Labor cost: {_money(labor_cost)}",
        f"Material allowance: {_money(material_allowance)}",
        f"Prep allowance: {_money(prep_allowance)}",
        f"Base cost: {_money(base_cost)}",
        (
            f"Low estimate before rounding: {_money(unrounded_low)} "
            f"({overhead_profit_percent:g}% overhead/profit)"
        ),
        (
            f"High estimate before rounding: {_money(unrounded_high)} "
            f"({risk_buffer_percent:g}% risk buffer)"
        ),
        (
            f"Suggested estimating range rounded to the nearest $50: "
            f"{_money(suggested_low)} - {_money(suggested_high)}"
        ),
    ]

    pricing_notes = []
    if missing_labor_fields:
        pricing_notes.append(
            "Labor cost was treated as $0 because these fields are missing: "
            + ", ".join(missing_labor_fields)
            + "."
        )
    else:
        pricing_notes.append(
            "Labor cost was calculated as crew size x labor days x labor rate per day."
        )

    defaulted_fields = []
    if pricing_inputs.material_allowance is None:
        defaulted_fields.append("material_allowance ($0)")
    if pricing_inputs.prep_allowance is None:
        defaulted_fields.append("prep_allowance ($0)")
    if pricing_inputs.overhead_profit_percent is None:
        defaulted_fields.append("overhead_profit_percent (25%)")
    if pricing_inputs.risk_buffer_percent is None:
        defaulted_fields.append("risk_buffer_percent (10%)")
    if defaulted_fields:
        pricing_notes.append("Defaults were used for: " + ", ".join(defaulted_fields) + ".")

    if pricing_inputs.final_price_before_tax is None and quote_draft.price_before_tax is not None:
        pricing_notes.append(
            "The draft transcript price was copied into the painter-approved final price field."
        )
    elif final_price is None:
        pricing_notes.append("The painter-approved final price is still missing.")

    pricing_notes.extend(
        [
            "This suggested range is an estimating helper only, not a guaranteed price.",
            "The painter must review and approve the final price before sending the quote.",
        ]
    )

    pricing = pricing_inputs.model_copy(
        update={
            "material_allowance": material_allowance,
            "prep_allowance": prep_allowance,
            "overhead_profit_percent": overhead_profit_percent,
            "risk_buffer_percent": risk_buffer_percent,
            "suggested_low_price": suggested_low,
            "suggested_high_price": suggested_high,
            "final_price_before_tax": final_price,
            "pricing_notes": pricing_notes,
        }
    )

    return PricingCalculationResponse(
        quote_draft=quote_draft,
        pricing=pricing,
        calculation_breakdown=calculation_breakdown,
    )
