const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json", ...options.headers },
    ...options,
  });

  if (!response.ok) {
    const errorBody = await response.json().catch(() => null);
    throw new Error(
      errorBody?.detail ?? `API request failed with status ${response.status}`,
    );
  }

  return response.json();
}

export function generateDraft(transcript) {
  return request("/drafts/from-transcript", {
    method: "POST",
    body: JSON.stringify({ transcript }),
  });
}
