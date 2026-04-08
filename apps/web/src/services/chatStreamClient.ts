export type ChatMessage = {
  role: "user" | "assistant" | "system";
  content: string;
};

export async function fetchSessionMessages(
  apiBaseUrl: string,
  token: string,
  sessionId: string
): Promise<ChatMessage[]> {
  const response = await fetch(`${apiBaseUrl}/v1/knox/sessions/${sessionId}/messages`, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  });

  if (!response.ok) {
    throw new Error("Failed to load session history");
  }

  return (await response.json()).map((m: { role: string; content: string }) => ({
    role: m.role,
    content: m.content
  }));
}

export async function streamChat(
  apiBaseUrl: string,
  token: string,
  sessionId: string,
  message: string
): Promise<string> {
  const response = await fetch(`${apiBaseUrl}/v1/knox/chat/stream`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ sessionId, message })
  });

  if (!response.ok) {
    throw new Error("Failed to stream chat");
  }

  const raw = await response.text();
  const lines = raw
    .split("\n")
    .filter((line) => line.startsWith("data: "))
    .map((line) => line.slice(6));

  const tokens = lines.map((line) => {
    const parsed = JSON.parse(line) as { token: string };
    return parsed.token;
  });

  return tokens.join("");
}
