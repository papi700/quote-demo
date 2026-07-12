from fastapi import APIRouter

router = APIRouter(prefix="/messages", tags=["messages"])


@router.post("/send-test")
def send_test_message() -> dict[str, str]:
    return {
        "status": "not_implemented",
        "message": "Message sending is not implemented yet.",
    }
