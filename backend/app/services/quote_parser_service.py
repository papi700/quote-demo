from google import genai
from google.genai import errors
from google.genai import types

from app.core.config import settings
from app.schemas.quote import QuoteDraft

PRIMARY_MODEL_NAME = "gemini-2.5-flash-lite"
COMPATIBILITY_MODEL_NAME = "gemini-flash-lite-latest"

SYSTEM_INSTRUCTION = """
You extract residential painting estimate details from messy painter notes.
Use only facts stated or directly implied by the transcript. Never invent customer
details, scope, prices, finishes, coats, dates, or exclusions. Use null for unknown
scalar values and empty arrays for unknown list values. Add important unknowns that
the painter should confirm to missing_fields. Put ambiguity or interpretation notes
in confidence_notes. Write customer_message as a concise, friendly summary suitable
for the painter to review before sending. Price must be a number without currency
symbols; preserve tax wording separately in tax_note.
""".strip()


class QuoteParserError(RuntimeError):
    """Raised when an AI-backed quote draft cannot be generated safely."""


def _fallback_quote() -> QuoteDraft:
    """Return a deterministic quote so the demo works without an API key."""

    return QuoteDraft(
        customer_name="Sarah",
        city="Burnaby",
        job_type="Interior repaint",
        rooms_or_areas=["Living room", "Hallway", "Two bedrooms"],
        included_work=[
            "Paint walls in the living room, hallway, and two bedrooms",
            "Paint the hallway ceiling",
        ],
        excluded_work=["Ceilings other than the hallway ceiling"],
        prep_work=["Fill minor nail holes", "Repair one drywall patch near the window"],
        paint_finish="Eggshell",
        number_of_coats="Two coats",
        price_before_tax=2800.0,
        tax_note="Plus GST",
        timeline="Next week, if possible",
        customer_message=(
            "Hi Sarah, here is the draft scope for your interior repaint in Burnaby. "
            "It includes two coats on the listed walls, the hallway ceiling, and the "
            "noted minor prep work. The estimated price is $2,800 plus GST."
        ),
        missing_fields=["customer_phone", "customer_email", "job_address"],
        confidence_notes=[
            "Demo fallback used because GOOGLE_API_KEY is not configured.",
            "Confirm which room contains the drywall patch near the window.",
        ],
    )


def _generate_quote(client: genai.Client, transcript: str, model: str) -> QuoteDraft:
    response = client.models.generate_content(
        model=model,
        contents=transcript,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            response_mime_type="application/json",
            response_schema=QuoteDraft,
            temperature=0.1,
        ),
    )

    if isinstance(response.parsed, QuoteDraft):
        return response.parsed
    if response.parsed is not None:
        return QuoteDraft.model_validate(response.parsed)
    if response.text:
        return QuoteDraft.model_validate_json(response.text)
    raise ValueError("Gemini returned no quote draft")


def parse_transcript_to_quote(transcript: str) -> QuoteDraft:
    """Convert transcript notes into a validated painter quote draft."""

    api_key = settings.google_api_key
    if api_key is None or not api_key.get_secret_value().strip():
        return _fallback_quote()

    try:
        client = genai.Client(api_key=api_key.get_secret_value())
        try:
            return _generate_quote(client, transcript, PRIMARY_MODEL_NAME)
        except errors.ClientError as exc:
            if exc.code != 404:
                raise
            return _generate_quote(client, transcript, COMPATIBILITY_MODEL_NAME)
    except Exception as exc:
        raise QuoteParserError("Quote generation failed") from exc
