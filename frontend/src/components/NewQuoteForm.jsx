export default function NewQuoteForm({ transcript, onTranscriptChange, onSubmit, loading }) {
  return (
    <section className="card">
      <span className="step">Step 1</span>
      <h2>Paste transcript</h2>
      <p>Add notes from a customer conversation or site visit.</p>
      <form onSubmit={onSubmit}>
        <label htmlFor="transcript">Job notes</label>
        <textarea
          id="transcript"
          value={transcript}
          onChange={(event) => onTranscriptChange(event.target.value)}
          placeholder="Example: Paint the kitchen and hallway, two coats..."
          rows="7"
          required
        />
        <button type="submit" disabled={loading || !transcript.trim()}>
          {loading ? "Generating…" : "Generate Quote Draft"}
        </button>
      </form>
    </section>
  );
}
