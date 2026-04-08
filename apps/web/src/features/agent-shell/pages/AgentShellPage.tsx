import { useEffect, useState } from "react";

import { AgentProfile, agentProfiles } from "../data/agentProfiles";

type Props = {
  onSelectAgent?: (slug: string) => void;
  overrideProfiles?: AgentProfile[];
  loadProfiles?: () => Promise<AgentProfile[]>;
};

export function AgentShellPage({ onSelectAgent, overrideProfiles, loadProfiles }: Props) {
  const [loading, setLoading] = useState(true);
  const [profiles, setProfiles] = useState<AgentProfile[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    const load = async () => {
      setLoading(true);
      setError(null);
      try {
        await new Promise((resolve) => setTimeout(resolve, 0));
        const next = loadProfiles ? await loadProfiles() : (overrideProfiles ?? agentProfiles);
        if (!active) {
          return;
        }
        setProfiles(next);
      } catch {
        if (!active) {
          return;
        }
        setError("Failed to load agents.");
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    };

    void load();
    return () => {
      active = false;
    };
  }, [overrideProfiles, loadProfiles]);

  if (loading) {
    return <p data-testid="agent-shell-loading">Loading agents...</p>;
  }

  if (error) {
    return <p data-testid="agent-shell-error">{error}</p>;
  }

  if (profiles.length === 0) {
    return <p data-testid="agent-shell-empty">No agents available yet.</p>;
  }

  return (
    <section>
      <h1>Ayyo Agent Shell</h1>
      <ul data-testid="agent-shell-list">
        {profiles.map((profile) => (
          <li key={profile.id}>
            <h2>{profile.displayName}</h2>
            <p>{profile.specialty}</p>
            {profile.status === "active" ? (
              <button type="button" onClick={() => onSelectAgent?.(profile.slug)}>
                Open {profile.displayName}
              </button>
            ) : (
              <div data-testid="agent-card-coming-soon" aria-disabled="true">
                Coming Soon
              </div>
            )}
          </li>
        ))}
      </ul>
    </section>
  );
}
