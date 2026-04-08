export type AgentProfile = {
  id: string;
  slug: string;
  displayName: string;
  specialty: string;
  status: "active" | "coming_soon";
};

export const agentProfiles: AgentProfile[] = [
  {
    id: "1",
    slug: "knox",
    displayName: "KNOX",
    specialty: "Health and Discipline Coach",
    status: "active"
  },
  {
    id: "2",
    slug: "atlas",
    displayName: "ATLAS",
    specialty: "Strength Engineering",
    status: "coming_soon"
  },
  {
    id: "3",
    slug: "nova",
    displayName: "NOVA",
    specialty: "Nutrition Intelligence",
    status: "coming_soon"
  }
];
