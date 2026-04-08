type GuidanceStep = {
  order: number;
  action: string;
  scheduleHint?: string;
};

type GuidancePlan = {
  type: "guidance_plan";
  title: string;
  steps: GuidanceStep[];
  constraints?: string[];
};

type Props = {
  content: string;
  loading?: boolean;
};

function parseGuidance(content: string): GuidancePlan | null {
  try {
    const parsed = JSON.parse(content) as GuidancePlan;
    if (parsed.type !== "guidance_plan" || !parsed.title || !Array.isArray(parsed.steps)) {
      return null;
    }
    return parsed;
  } catch {
    return null;
  }
}

export function GuidanceMessageCard({ content, loading = false }: Props) {
  if (loading) {
    return <div data-testid="guidance-loading">Generating guidance...</div>;
  }

  const guidance = parseGuidance(content);
  if (!guidance) {
    return <div data-testid="guidance-error">Unable to render guidance plan.</div>;
  }

  return (
    <article data-testid="guidance-card">
      <h3>{guidance.title}</h3>
      <ol>
        {guidance.steps.map((step) => (
          <li key={`${step.order}-${step.action}`}>
            {step.action}
            {step.scheduleHint ? ` (${step.scheduleHint})` : ""}
          </li>
        ))}
      </ol>
      {guidance.constraints && guidance.constraints.length > 0 && (
        <ul>
          {guidance.constraints.map((constraint) => (
            <li key={constraint}>{constraint}</li>
          ))}
        </ul>
      )}
    </article>
  );
}
