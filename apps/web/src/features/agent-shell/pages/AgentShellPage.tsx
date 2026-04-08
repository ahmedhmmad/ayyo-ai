import { useEffect, useState } from "react";

import { AgentProfile, agentProfiles } from "../data/agentProfiles";

type Props = {
  onSelectAgent?: (slug: string) => void;
  overrideProfiles?: AgentProfile[];
};

export function AgentShellPage({ onSelectAgent, overrideProfiles }: Props) {
  const [loading, setLoading] = useState(true);
  const [profiles, setProfiles] = useState<AgentProfile[]>([]);

  useEffect(() => {
    const timer = setTimeout(() => {
      setProfiles(overrideProfiles ?? agentProfiles);
      setLoading(false);
    }, 0);

    return () => clearTimeout(timer);
  }, [overrideProfiles]);

  if (loading) {
    return <p data-testid="agent-shell-loading">Loading agents...</p>;
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
