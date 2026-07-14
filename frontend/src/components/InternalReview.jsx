function formatMoney(value) {
  return value == null ? "Not set" : `$${value.toLocaleString()}`;
}

function ReviewList({ title, items, emptyMessage }) {
  return (
    <div className="internal-list">
      <strong>{title}</strong>
      {items?.length ? (
        <ul>
          {items.map((item, index) => (
            <li key={`${item}-${index}`}>{item}</li>
          ))}
        </ul>
      ) : (
        <p className="muted compact">{emptyMessage}</p>
      )}
    </div>
  );
}

export default function InternalReview({ draft, pricingResult }) {
  const pricing = pricingResult?.pricing;
  const hasMissingFields = Boolean(draft?.missing_fields?.length);
  const hasConfidenceNotes = Boolean(draft?.confidence_notes?.length);
  const finalPrice = pricing?.final_price_before_tax ?? draft?.price_before_tax;

  return (
    <section className="card internal-review-card">
      <span className="step">Step 4</span>
      <h2>Internal painter review</h2>
      <p className="internal-only">Customer will not see this section.</p>

      {draft ? (
        <>
          <div className="internal-summary">
            <div>
              <span>Customer</span>
              <strong>{draft.customer_name || "Not provided"}</strong>
            </div>
            <div>
              <span>City</span>
              <strong>{draft.city || "Not provided"}</strong>
            </div>
            <div>
              <span>Job type</span>
              <strong>{draft.job_type || "Not provided"}</strong>
            </div>
          </div>

          <div className="internal-prices">
            <div>
              <span>Suggested estimating range</span>
              <strong>
                {pricing?.suggested_low_price != null &&
                pricing?.suggested_high_price != null
                  ? `${formatMoney(pricing.suggested_low_price)} - ${formatMoney(
                      pricing.suggested_high_price,
                    )}`
                  : "Calculate pricing to see a range"}
              </strong>
            </div>
            <div>
              <span>Painter-approved final price</span>
              <strong>{formatMoney(finalPrice)}</strong>
            </div>
          </div>

          <div className="review-warnings">
            {finalPrice == null && (
              <p className="status warning">
                Final price is missing. Set a painter-approved price before sending.
              </p>
            )}
            {hasMissingFields && (
              <p className="status warning">
                Some quote fields are missing. Review them before sending.
              </p>
            )}
            {hasConfidenceNotes && (
              <p className="status warning">
                The generated draft contains confidence notes that need painter review.
              </p>
            )}
          </div>

          <div className="internal-details">
            <ReviewList
              title="Missing fields"
              items={draft.missing_fields}
              emptyMessage="No missing fields reported."
            />
            <ReviewList
              title="Confidence notes"
              items={draft.confidence_notes}
              emptyMessage="No confidence notes reported."
            />
          </div>

          {pricingResult && (
            <div className="internal-details">
              <ReviewList
                title="Calculation breakdown"
                items={pricingResult.calculation_breakdown}
                emptyMessage="No calculation breakdown available."
              />
              <ReviewList
                title="Pricing notes"
                items={pricing.pricing_notes}
                emptyMessage="No pricing notes available."
              />
            </div>
          )}

          <p className="review-before-sending">Review before sending.</p>
        </>
      ) : (
        <p className="muted">Generate a quote draft to begin the internal review.</p>
      )}
    </section>
  );
}
