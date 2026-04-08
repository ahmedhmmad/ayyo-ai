export type MemoryRecord = {
  id: string;
  category: string;
  key: string;
  value: string;
  source_type: string;
  confidence_score: number;
};

function authHeaders(token: string): HeadersInit {
  return {
    "Content-Type": "application/json",
    Authorization: `Bearer ${token}`
  };
}

export async function listMemory(apiBaseUrl: string, token: string): Promise<MemoryRecord[]> {
  const response = await fetch(`${apiBaseUrl}/v1/knox/memory`, {
    headers: authHeaders(token)
  });

  if (!response.ok) {
    throw new Error("Failed to load memory");
  }

  return (await response.json()) as MemoryRecord[];
}

export async function updateMemory(
  apiBaseUrl: string,
  token: string,
  memoryId: string,
  value: string
): Promise<MemoryRecord> {
  const response = await fetch(`${apiBaseUrl}/v1/knox/memory/${memoryId}`, {
    method: "PATCH",
    headers: authHeaders(token),
    body: JSON.stringify({ value })
  });

  if (!response.ok) {
    throw new Error("Failed to update memory");
  }

  return (await response.json()) as MemoryRecord;
}

export async function deleteMemory(apiBaseUrl: string, token: string, memoryId: string): Promise<void> {
  const response = await fetch(`${apiBaseUrl}/v1/knox/memory/${memoryId}`, {
    method: "DELETE",
    headers: authHeaders(token)
  });

  if (!response.ok) {
    throw new Error("Failed to delete memory");
  }
}

export async function resetMemory(apiBaseUrl: string, token: string): Promise<void> {
  const response = await fetch(`${apiBaseUrl}/v1/knox/memory`, {
    method: "DELETE",
    headers: authHeaders(token)
  });

  if (!response.ok) {
    throw new Error("Failed to reset memory");
  }
}
