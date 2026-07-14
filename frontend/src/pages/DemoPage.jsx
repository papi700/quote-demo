import { useState } from "react";

import { generateDraft } from "../api/client";
import AudioRecorder from "../components/AudioRecorder";
import NewQuoteForm from "../components/NewQuoteForm";
import QuoteDraft from "../components/QuoteDraft";
import QuotePreview from "../components/QuotePreview";

export default function DemoPage() {
  const [transcript, setTranscript] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    setLoading(true);
    setError("");

    try {
      setResult(await generateDraft(transcript));
    } catch (requestError) {
      setResult(null);
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Could not reach the backend. Make sure it is running on port 8000.",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main>
      <header className="hero">
        <p className="eyebrow">Painter demo</p>
        <h1>Voice Note to Quote</h1>
        <p>Turn rough job notes into a clear quote your customer can review.</p>
      </header>
      <div className="workflow">
        <NewQuoteForm
          transcript={transcript}
          onTranscriptChange={setTranscript}
          onSubmit={handleSubmit}
          loading={loading}
        />
        <QuoteDraft draft={result} onChange={setResult} error={error} />
        <QuotePreview draft={result} />
        <AudioRecorder />
      </div>
    </main>
  );
}
