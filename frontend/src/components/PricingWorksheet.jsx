const PRICING_FIELDS = [
  ["crew_size", "Crew size", "1"],
  ["labor_days", "Labor days", "0.5"],
  ["labor_rate_per_day", "Labor rate per day", "0.01"],
  ["material_allowance", "Material allowance", "0.01"],
  ["prep_allowance", "Prep allowance", "0.01"],
  ["overhead_profit_percent", "Overhead/profit %", "0.1"],
  ["risk_buffer_percent", "Risk buffer %", "0.1"],
  ["final_price_before_tax", "Painter-approved final price", "0.01"],
];

function formatMoney(value) {
  return value == null ? "Not available" : `$${value.toLocaleString()}`;
}

export default function PricingWorksheet({
  draft,
  inputs,
  result,
  error,
  loading,
  onInputChange,
  onCalculate,
}) {
  return (
    <section className="card pricing-card">
      <span className="step">Step 3</span>
      <h2>Pricing worksheet</h2>
      <p>
        Check your assumptions, calculate a suggested estimating range, and approve
        the final customer price yourself.
      </p>

      <div className="pricing-fields">
        {PRICING_FIELDS.map(([field, label, step]) => (
          <label key={field}>
            {label}
            <input
              type="number"
              min={field === "crew_size" ? "1" : "0"}
              step={step}
              value={inputs[field] ?? ""}
              onChange={(event) =>
                onInputChange(
                  field,
                  event.target.value === "" ? null : Number(event.target.value),
                )
              }
            />
          </label>
        ))}
      </div>

      <button type="button" onClick={onCalculate} disabled={!draft || loading}>
        {loading ? "Calculating..." : "Calculate Suggested Range"}
      </button>

      {error && <p className="status error">{error}</p>}

      {result && (
        <div className="pricing-result">
          <p className="range-label">Suggested estimating range</p>
          <p className="suggested-range">
            {formatMoney(result.pricing.suggested_low_price)}
            {" - "}
            {formatMoney(result.pricing.suggested_high_price)}
          </p>
          <p className="review-note">Review before sending. This is not a guaranteed price.</p>

          <details>
            <summary>Calculation breakdown</summary>
            <ul>
              {result.calculation_breakdown.map((line) => (
                <li key={line}>{line}</li>
              ))}
            </ul>
          </details>

          <div className="pricing-notes">
            <strong>Pricing notes</strong>
            <ul>
              {result.pricing.pricing_notes.map((note) => (
                <li key={note}>{note}</li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </section>
  );
}
