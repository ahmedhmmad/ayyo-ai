import { FormEvent, useEffect, useState } from "react";

import { createChatStore } from "../state/chatStore";
import { CheckInPanel } from "../../checkins/components/CheckInPanel";
import { GuidanceMessageCard } from "./GuidanceMessageCard";

type Props = {
  apiBaseUrl: string;
  token: string;
  sessionId: string;
};

export function ChatPanel({ apiBaseUrl, token, sessionId }: Props) {
  const [store] = useState(() => createChatStore(apiBaseUrl, token, sessionId));
  const [, setTick] = useState(0);
  const [draft, setDraft] = useState("");
  const [showCheckins, setShowCheckins] = useState(false);

  useEffect(() => {
    void store.loadHistory().then(() => setTick((v) => v + 1));
  }, [store]);

  const submitViaComposer = async (message: string) => {
    if (!message.trim()) {
      return;
    }
    setDraft(message);
    await store.sendMessage(message.trim());
    setDraft("");
    setTick((v) => v + 1);
  };

  const onSubmit = async (event: FormEvent) => {
    event.preventDefault();
    await submitViaComposer(draft);
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
          <li key={`${message.role}-${idx}`}>
            {message.role === "assistant" && message.content.trim().startsWith("{") ? (
              <>
                <span>assistant: </span>
                <GuidanceMessageCard content={message.content} loading={store.loading && idx === store.messages.length - 1} />
              </>
            ) : (
              `${message.role}: ${message.content}`
            )}
          </li>
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
      <button type="button" onClick={() => setShowCheckins((v) => !v)}>
        Check-ins
      </button>
      {showCheckins && (
        <CheckInPanel
          apiBaseUrl={apiBaseUrl}
          token={token}
          onSubmitToChat={(text) => {
            void submitViaComposer(text);
          }}
        />
      )}
    </section>
  );
}
