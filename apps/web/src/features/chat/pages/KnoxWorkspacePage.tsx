import { useEffect, useState } from "react";

import { ChatPanel } from "../components/ChatPanel";
import { VoicePlaceholder } from "../components/VoicePlaceholder";
import { MemoryPanel } from "../../memory/components/MemoryPanel";

type Props = {
  apiBaseUrl: string;
  token: string;
  sessionId: string;
};

export function KnoxWorkspacePage({ apiBaseUrl, token, sessionId }: Props) {
  const [booting, setBooting] = useState(true);
  const [tab, setTab] = useState<"chat" | "memory">("chat");

  useEffect(() => {
    const timer = setTimeout(() => setBooting(false), 0);
    return () => clearTimeout(timer);
  }, []);

  if (booting) {
    return <p data-testid="workspace-loading">Loading workspace...</p>;
  }

  if (!apiBaseUrl || !token || !sessionId) {
    return <p data-testid="workspace-error">Workspace configuration is missing.</p>;
  }

  if (!["chat", "memory"].includes(tab)) {
    return <p data-testid="workspace-empty">No workspace section selected.</p>;
  }

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
      <VoicePlaceholder />
      {tab === "chat" ? (
        <ChatPanel apiBaseUrl={apiBaseUrl} token={token} sessionId={sessionId} />
      ) : (
        <MemoryPanel apiBaseUrl={apiBaseUrl} token={token} />
      )}
    </main>
  );
}
