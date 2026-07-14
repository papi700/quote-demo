from fastapi.testclient import TestClient

from app.main import app


def _quote_draft(price_before_tax: float | None = 2800.0) -> dict:
    return {
        "customer_name": "Sarah",
        "city": "Burnaby",
        "job_type": "Interior repaint",
        "rooms_or_areas": ["Living room", "Hallway"],
        "included_work": ["Paint walls"],
        "excluded_work": [],
        "prep_work": ["Fill nail holes"],
        "paint_finish": "Eggshell",
        "number_of_coats": "Two coats",
        "price_before_tax": price_before_tax,
        "missing_fields": [],
        "confidence_notes": [],
    }


def test_calculate_pricing_returns_expected_range() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/quotes/calculate-pricing",
            json={
                "quote_draft": _quote_draft(),
                "pricing_inputs": {
                    "crew_size": 1,
                    "labor_days": 2,
                    "labor_rate_per_day": 450,
                    "material_allowance": 350,
                    "prep_allowance": 250,
                    "overhead_profit_percent": 25,
                    "risk_buffer_percent": 10,
                },
            },
        )

    assert response.status_code == 200
    result = response.json()
    assert result["pricing"]["suggested_low_price"] == 1900.0
    assert result["pricing"]["suggested_high_price"] == 2050.0
    assert result["pricing"]["final_price_before_tax"] == 2800.0
    assert result["quote_draft"]["price_before_tax"] == 2800.0
    assert len(result["calculation_breakdown"]) == 7


def test_missing_optional_pricing_fields_do_not_crash() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/quotes/calculate-pricing",
            json={
                "quote_draft": _quote_draft(price_before_tax=None),
                "pricing_inputs": {},
            },
        )

    assert response.status_code == 200
    pricing = response.json()["pricing"]
    assert pricing["suggested_low_price"] == 0.0
    assert pricing["suggested_high_price"] == 0.0
    assert pricing["final_price_before_tax"] is None
    assert pricing["overhead_profit_percent"] == 25.0
    assert pricing["risk_buffer_percent"] == 10.0
    assert any("crew_size" in note for note in pricing["pricing_notes"])


def test_negative_pricing_input_returns_validation_error() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/quotes/calculate-pricing",
            json={
                "quote_draft": _quote_draft(),
                "pricing_inputs": {"crew_size": 0, "material_allowance": -1},
            },
        )

    assert response.status_code == 422
