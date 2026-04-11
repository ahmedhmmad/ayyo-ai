import { useState } from "react"
import { AgentShellPage } from "../features/agent-shell/pages/AgentShellPage"
import { KnoxWorkspacePage } from "../features/chat/pages/KnoxWorkspacePage"

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000"

export default function App() {
  const [activeAgent, setActiveAgent] = useState<string | null>(null)

  if (activeAgent === "knox") {
    return (
      <KnoxWorkspacePage
        apiBaseUrl={API_BASE_URL}
        token="dev-token"
        sessionId="dev-session-001"
      />
    )
  }

  return (
    <AgentShellPage
      onSelectAgent={(agentId) => setActiveAgent(agentId)}
    />
  )
}
