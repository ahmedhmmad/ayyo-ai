import { useState } from "react";

import { ChatPanel } from "../components/ChatPanel";
import { MemoryPanel } from "../../memory/components/MemoryPanel";

type Props = {
  apiBaseUrl: string;
  token: string;
  sessionId: string;
};

export function KnoxWorkspacePage({ apiBaseUrl, token, sessionId }: Props) {
  const [tab, setTab] = useState<"chat" | "memory">("chat");

  return (
    <main>
      <header>
        <h1>KNOX</h1>
        <p>Role: Health and Discipline Coach</p>
        <p>Character: Tough, Direct, Disciplined, Motivational</p>
      </header>
      <nav>
        <button type="button" onClick={() => setTab("chat")}>Chat</button>
        <button type="button" onClick={() => setTab("memory")}>Memory</button>
      </nav>
      {tab === "chat" ? (
        <ChatPanel apiBaseUrl={apiBaseUrl} token={token} sessionId={sessionId} />
      ) : (
        <MemoryPanel apiBaseUrl={apiBaseUrl} token={token} />
      )}
    </main>
  );
}
