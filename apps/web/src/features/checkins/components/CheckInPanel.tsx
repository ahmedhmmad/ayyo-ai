import { useEffect, useState } from "react";

type CheckInPrompt = {
  id: string;
  commitmentId: string;
  promptText: string;
  triggerEvent: string;
  status: string;
};

type Props = {
  apiBaseUrl: string;
  token: string;
  onSubmitToChat: (text: string) => void;
};

export function CheckInPanel({ apiBaseUrl, token, onSubmitToChat }: Props) {
  const [loading, setLoading] = useState(true);
  const [prompts, setPrompts] = useState<CheckInPrompt[]>([]);
  const [drafts, setDrafts] = useState<Record<string, string>>({});

  useEffect(() => {
    let active = true;
    const load = async () => {
      setLoading(true);
      const response = await fetch(`${apiBaseUrl}/v1/knox/checkins`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      const data = response.ok ? ((await response.json()) as CheckInPrompt[]) : [];
      if (!active) {
        return;
      }
      setPrompts(data);
      setLoading(false);
    };

    void load();
    return () => {
      active = false;
    };
  }, [apiBaseUrl, token]);

  const onSubmit = async (prompt: CheckInPrompt) => {
    const responseText = (drafts[prompt.id] ?? "").trim();
    if (!responseText) {
      return;
    }

    const response = await fetch(`${apiBaseUrl}/v1/knox/checkins/${prompt.id}/respond`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({ responseText, outcome: "not_complete" })
    });

    if (!response.ok) {
      return;
    }

    const payload = (await response.json()) as { followUpMessage: string };
    onSubmitToChat(payload.followUpMessage);
    setPrompts((prev) => prev.filter((p) => p.id !== prompt.id));
  };

  if (loading) {
    return <p data-testid="checkins-loading">Loading check-ins...</p>;
  }

  if (prompts.length === 0) {
    return <p data-testid="checkins-empty">No pending check-ins.</p>;
  }

  return (
    <section>
      <h3>Check-ins</h3>
      <ul data-testid="checkins-list">
        {prompts.map((prompt) => (
          <li key={prompt.id}>
            <p>{prompt.promptText}</p>
            <input
              aria-label={`checkin-response-${prompt.id}`}
              value={drafts[prompt.id] ?? ""}
              onChange={(event) => setDrafts((prev) => ({ ...prev, [prompt.id]: event.target.value }))}
            />
            <button type="button" onClick={() => void onSubmit(prompt)}>
              Submit
            </button>
          </li>
        ))}
      </ul>
    </section>
  );
}
