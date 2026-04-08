import { useEffect, useState } from "react";

import {
  deleteMemory,
  listMemory,
  MemoryRecord,
  resetMemory,
  updateMemory
} from "../../../services/memoryClient";

type Props = {
  apiBaseUrl: string;
  token: string;
};

export function MemoryPanel({ apiBaseUrl, token }: Props) {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [records, setRecords] = useState<MemoryRecord[]>([]);
  const [drafts, setDrafts] = useState<Record<string, string>>({});

  const load = async () => {
    setLoading(true);
    setError(null);
    try {
      const next = await listMemory(apiBaseUrl, token);
      setRecords(next);
      setDrafts(Object.fromEntries(next.map((record) => [record.id, record.value])));
    } catch {
      setError("Failed to load memory");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void load();
  }, []);

  const onSave = async (id: string) => {
    const value = drafts[id]?.trim();
    if (!value) {
      return;
    }

    try {
      const updated = await updateMemory(apiBaseUrl, token, id, value);
      setRecords((prev) => prev.map((record) => (record.id === id ? updated : record)));
    } catch {
      setError("Failed to update memory");
    }
  };

  const onDelete = async (id: string) => {
    try {
      await deleteMemory(apiBaseUrl, token, id);
      setRecords((prev) => prev.filter((record) => record.id !== id));
    } catch {
      setError("Failed to delete memory");
    }
  };

  const onReset = async () => {
    if (!window.confirm("Reset all memory?")) {
      return;
    }

    try {
      await resetMemory(apiBaseUrl, token);
      await load();
    } catch {
      setError("Failed to reset memory");
    }
  };

  return (
    <section>
      <h2>Memory</h2>
      {loading && <p data-testid="memory-loading">Loading memory...</p>}
      {error && <p data-testid="memory-error">{error}</p>}
      {!loading && !error && records.length === 0 && <p data-testid="memory-empty">No memory yet.</p>}

      <ul data-testid="memory-list">
        {records.map((record) => (
          <li key={record.id}>
            <p>{`${record.key}: ${record.value}`}</p>
            <input
              aria-label={`edit-value-${record.id}`}
              value={drafts[record.id] ?? ""}
              onChange={(event) => setDrafts((prev) => ({ ...prev, [record.id]: event.target.value }))}
            />
            <button type="button" onClick={() => void onSave(record.id)}>
              Save
            </button>
            <button type="button" onClick={() => void onDelete(record.id)}>
              Delete
            </button>
          </li>
        ))}
      </ul>

      <button type="button" onClick={() => void onReset()}>
        Reset All
      </button>
    </section>
  );
}
