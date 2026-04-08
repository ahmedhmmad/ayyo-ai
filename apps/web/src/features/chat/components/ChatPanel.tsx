import { FormEvent, useEffect, useState } from "react";

import { createChatStore } from "../state/chatStore";

type Props = {
  apiBaseUrl: string;
  token: string;
  sessionId: string;
};

export function ChatPanel({ apiBaseUrl, token, sessionId }: Props) {
  const [store] = useState(() => createChatStore(apiBaseUrl, token, sessionId));
  const [, setTick] = useState(0);
  const [draft, setDraft] = useState("");

  useEffect(() => {
    void store.loadHistory().then(() => setTick((v) => v + 1));
  }, [store]);

  const onSubmit = async (event: FormEvent) => {
    event.preventDefault();
    if (!draft.trim()) {
      return;
    }
    await store.sendMessage(draft.trim());
    setDraft("");
    setTick((v) => v + 1);
  };

  return (
    <section>
      {store.loading && <p data-testid="chat-loading">Loading chat...</p>}
      {store.error && <p data-testid="chat-error">{store.error}</p>}
      {!store.loading && !store.error && store.messages.length === 0 && (
        <p data-testid="chat-empty">No messages yet.</p>
      )}
      <ul data-testid="chat-list">
        {store.messages.map((message, idx) => (
          <li key={`${message.role}-${idx}`}>{`${message.role}: ${message.content}`}</li>
        ))}
      </ul>
      <form onSubmit={onSubmit}>
        <input
          aria-label="message"
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
          placeholder="Tell KNOX your next move"
        />
        <button type="submit">Send</button>
      </form>
    </section>
  );
}
