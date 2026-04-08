import { ChatPanel } from "../components/ChatPanel";

type Props = {
  apiBaseUrl: string;
  token: string;
  sessionId: string;
};

export function KnoxWorkspacePage({ apiBaseUrl, token, sessionId }: Props) {
  return (
    <main>
      <header>
        <h1>KNOX</h1>
        <p>Role: Health and Discipline Coach</p>
        <p>Character: Tough, Direct, Disciplined, Motivational</p>
      </header>
      <ChatPanel apiBaseUrl={apiBaseUrl} token={token} sessionId={sessionId} />
    </main>
  );
}
