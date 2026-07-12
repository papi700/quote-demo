export default function QuoteDraft({ result, error }) {
  return (
    <section className="card">
      <span className="step">Step 2</span>
      <h2>Review draft</h2>
      {error && <p className="status error">{error}</p>}
      {result ? (
        <div className="status">
          <strong>Backend response</strong>
          <p>{result.message}</p>
        </div>
      ) : (
        <p className="muted">Generated scope, line items, and notes will appear here.</p>
      )}
    </section>
  );
}
