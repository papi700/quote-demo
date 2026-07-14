from fastapi.testclient import TestClient

from app.api.routes import drafts as drafts_route
from app.core.config import settings
from app.main import app
from app.services.quote_parser_service import QuoteParserError


def test_empty_transcript_returns_400() -> None:
    with TestClient(app) as client:
        response = client.post("/drafts/from-transcript", json={"transcript": "   \n"})

    assert response.status_code == 400
    assert response.json() == {"detail": "Transcript must not be empty."}


def test_valid_transcript_returns_fallback_quote(monkeypatch) -> None:
    monkeypatch.setattr(settings, "google_api_key", None)

    with TestClient(app) as client:
        response = client.post(
            "/drafts/from-transcript",
            json={
                "transcript": (
                    "Sarah in Burnaby. Interior repaint. Living room, hallway, and two "
                    "bedrooms. Walls only except hallway ceiling. Minor nail holes and "
                    "one drywall patch near the window. Two coats eggshell. Customer "
                    "wants it done next week if possible. Price around 2800 plus GST."
                )
            },
        )

    assert response.status_code == 200
    draft = response.json()
    assert draft["customer_name"] == "Sarah"
    assert draft["city"] == "Burnaby"
    assert draft["job_type"] == "Interior repaint"
    assert draft["price_before_tax"] == 2800.0
    assert draft["tax_note"] == "Plus GST"
    assert draft["rooms_or_areas"] == ["Living room", "Hallway", "Two bedrooms"]
    assert "customer_phone" in draft["missing_fields"]


def test_parser_failure_returns_safe_500(monkeypatch) -> None:
    def fail_safely(_transcript: str):
        raise QuoteParserError("internal provider details")

    monkeypatch.setattr(drafts_route, "parse_transcript_to_quote", fail_safely)

    with TestClient(app) as client:
        response = client.post(
            "/drafts/from-transcript",
            json={"transcript": "Paint the living room."},
        )

    assert response.status_code == 500
    assert response.json() == {
        "detail": "Unable to generate a quote draft right now."
    }
    assert "provider" not in response.text
