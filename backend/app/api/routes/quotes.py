from fastapi import APIRouter

router = APIRouter(prefix="/quotes", tags=["quotes"])


@router.get("/{quote_id}")
def get_quote(quote_id: str) -> dict[str, str]:
    return {
        "status": "not_implemented",
        "message": "Quote retrieval is not implemented yet.",
        "quote_id": quote_id,
    }
