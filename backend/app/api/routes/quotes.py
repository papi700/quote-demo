from fastapi import APIRouter

from app.schemas.pricing import PricingCalculationRequest, PricingCalculationResponse
from app.services.pricing_service import calculate_pricing

router = APIRouter(prefix="/quotes", tags=["quotes"])


@router.post("/calculate-pricing", response_model=PricingCalculationResponse)
def calculate_quote_pricing(
    request: PricingCalculationRequest,
) -> PricingCalculationResponse:
    return calculate_pricing(request.quote_draft, request.pricing_inputs)


@router.get("/{quote_id}")
def get_quote(quote_id: str) -> dict[str, str]:
    return {
        "status": "not_implemented",
        "message": "Quote retrieval is not implemented yet.",
        "quote_id": quote_id,
    }
