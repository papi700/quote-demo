import { useState } from "react";

import { calculatePricing, generateDraft } from "../api/client";
import AudioRecorder from "../components/AudioRecorder";
import NewQuoteForm from "../components/NewQuoteForm";
import PricingWorksheet from "../components/PricingWorksheet";
import QuoteDraft from "../components/QuoteDraft";
import QuotePreview from "../components/QuotePreview";

const DEFAULT_PRICING_INPUTS = {
  crew_size: 1,
  labor_days: 2,
  labor_rate_per_day: 450,
  material_allowance: 350,
  prep_allowance: 250,
  overhead_profit_percent: 25,
  risk_buffer_percent: 10,
  final_price_before_tax: null,
};

export default function DemoPage() {
  const [transcript, setTranscript] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [pricingInputs, setPricingInputs] = useState(DEFAULT_PRICING_INPUTS);
  const [pricingResult, setPricingResult] = useState(null);
  const [pricingError, setPricingError] = useState("");
  const [pricingLoading, setPricingLoading] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    setLoading(true);
    setError("");

    try {
      const draft = await generateDraft(transcript);
      setResult(draft);
      setPricingInputs({
        ...DEFAULT_PRICING_INPUTS,
        final_price_before_tax: draft.price_before_tax ?? null,
      });
      setPricingResult(null);
      setPricingError("");
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

  function handlePricingInputChange(field, value) {
    setPricingInputs((current) => ({ ...current, [field]: value }));

    if (field === "final_price_before_tax") {
      setResult((current) =>
        current ? { ...current, price_before_tax: value } : current,
      );
    } else {
      setPricingResult(null);
    }
  }

  async function handleCalculatePricing() {
    if (!result) return;

    setPricingLoading(true);
    setPricingError("");

    try {
      const calculation = await calculatePricing(result, pricingInputs);
      setPricingResult(calculation);
      setPricingInputs(calculation.pricing);
      if (calculation.pricing.final_price_before_tax != null) {
        setResult((current) => ({
          ...current,
          price_before_tax: calculation.pricing.final_price_before_tax,
        }));
      }
    } catch (requestError) {
      setPricingError(
        requestError instanceof Error
          ? requestError.message
          : "Could not calculate pricing right now.",
      );
    } finally {
      setPricingLoading(false);
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
        <PricingWorksheet
          draft={result}
          inputs={pricingInputs}
          result={pricingResult}
          error={pricingError}
          loading={pricingLoading}
          onInputChange={handlePricingInputChange}
          onCalculate={handleCalculatePricing}
        />
        <QuotePreview draft={result} pricing={pricingResult?.pricing} />
        <AudioRecorder />
      </div>
    </main>
  );
}
