function DetailList({ title, items }) {
  if (!items?.length) return null;

  return (
    <div>
      <strong>{title}</strong>
      <ul>
        {items.map((item, index) => (
          <li key={`${item}-${index}`}>{item}</li>
        ))}
      </ul>
    </div>
  );
}

export default function QuotePreview({ draft }) {
  return (
    <section className="card preview-card">
      <span className="step">Step 5</span>
      <h2>Customer-facing quote preview</h2>
      {draft ? (
        <div className="preview customer-preview">
          <p className="review-note">Review before sending.</p>
          <h3>{draft.job_type || "Painting quote"}</h3>
          <p>
            {draft.customer_name || "Customer"}
            {draft.city ? ` - ${draft.city}` : ""}
          </p>
          <DetailList title="Areas" items={draft.rooms_or_areas} />
          <DetailList title="Included work" items={draft.included_work} />
          <DetailList title="Excluded work" items={draft.excluded_work} />
          <DetailList title="Preparation" items={draft.prep_work} />
          <p>
            <strong>Finish:</strong> {draft.paint_finish || "To be confirmed"}
            {draft.number_of_coats ? ` - ${draft.number_of_coats}` : ""}
          </p>
          {draft.timeline && (
            <p>
              <strong>Timeline:</strong> {draft.timeline}
            </p>
          )}
          <p className="final-price-label">Final price</p>
          <p className="price">
            {draft.price_before_tax == null
              ? "Price to be confirmed"
              : `$${draft.price_before_tax.toLocaleString()}`}
          </p>
          {draft.tax_note && <p>{draft.tax_note}</p>}
          {draft.customer_message && (
            <p className="customer-message">{draft.customer_message}</p>
          )}

          <div className="customer-actions" aria-label="Future customer actions">
            <button type="button" disabled>Approve quote</button>
            <button type="button" className="secondary" disabled>Ask a question</button>
            <button type="button" className="secondary" disabled>Request a change</button>
          </div>
        </div>
      ) : (
        <p className="muted">Your customer-facing quote will be previewed here.</p>
      )}
    </section>
  );
}
