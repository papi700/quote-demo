const TEXT_FIELDS = [
  ["customer_name", "Customer name"],
  ["customer_phone", "Customer phone"],
  ["customer_email", "Customer email"],
  ["city", "City"],
  ["job_address", "Job address"],
  ["job_type", "Job type"],
  ["paint_finish", "Paint finish"],
  ["number_of_coats", "Number of coats"],
  ["tax_note", "Tax note"],
  ["timeline", "Timeline"],
];

const LIST_FIELDS = [
  ["rooms_or_areas", "Rooms or areas"],
  ["included_work", "Included work"],
  ["excluded_work", "Excluded work"],
  ["prep_work", "Prep work"],
  ["missing_fields", "Missing fields"],
  ["confidence_notes", "Confidence notes"],
];

function linesToList(value) {
  return value
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean);
}

export default function QuoteDraft({ draft, onChange, error }) {
  function updateField(field, value) {
    onChange({ ...draft, [field]: value });
  }

  return (
    <section className="card draft-card">
      <span className="step">Step 2</span>
      <h2>Review and edit draft</h2>
      {error && <p className="status error">{error}</p>}
      {draft ? (
        <div className="draft-fields">
          {TEXT_FIELDS.map(([field, label]) => (
            <label key={field}>
              {label}
              <input
                value={draft[field] ?? ""}
                onChange={(event) => updateField(field, event.target.value || null)}
              />
            </label>
          ))}

          <label>
            Price before tax
            <input
              type="number"
              min="0"
              step="0.01"
              value={draft.price_before_tax ?? ""}
              onChange={(event) =>
                updateField(
                  "price_before_tax",
                  event.target.value === "" ? null : Number(event.target.value),
                )
              }
            />
          </label>

          {LIST_FIELDS.map(([field, label]) => (
            <label key={field}>
              {label} <span className="label-hint">(one per line)</span>
              <textarea
                rows="3"
                value={(draft[field] ?? []).join("\n")}
                onChange={(event) => updateField(field, linesToList(event.target.value))}
              />
            </label>
          ))}

          <label className="full-width">
            Customer message
            <textarea
              rows="5"
              value={draft.customer_message ?? ""}
              onChange={(event) =>
                updateField("customer_message", event.target.value || null)
              }
            />
          </label>
        </div>
      ) : (
        <p className="muted">Generated scope, pricing, and notes will appear here.</p>
      )}
    </section>
  );
}
