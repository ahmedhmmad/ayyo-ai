import { fireEvent, render, screen, waitFor } from "@testing-library/react";

import { AgentShellPage } from "../../src/features/agent-shell/pages/AgentShellPage";

describe("AgentShellPage", () => {
  it("shows loading then renders KNOX selectable and others non-interactive coming soon", async () => {
    render(<AgentShellPage />);

    expect(screen.getByTestId("agent-shell-loading")).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByTestId("agent-shell-list")).toBeInTheDocument();
    });

    const knox = screen.getByRole("button", { name: /open knox/i });
    expect(knox).toBeEnabled();

    const comingSoon = screen.getAllByTestId("agent-card-coming-soon");
    expect(comingSoon.length).toBeGreaterThan(0);

    for (const item of comingSoon) {
      expect(item).toHaveAttribute("aria-disabled", "true");
    }
  });

  it("shows empty state when no agent profiles available", async () => {
    render(<AgentShellPage overrideProfiles={[]} />);

    await waitFor(() => {
      expect(screen.getByTestId("agent-shell-empty")).toBeInTheDocument();
    });
  });

  it("opens KNOX workspace on selection", async () => {
    const onSelect = vi.fn();
    render(<AgentShellPage onSelectAgent={onSelect} />);

    await waitFor(() => {
      expect(screen.getByRole("button", { name: /open knox/i })).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole("button", { name: /open knox/i }));
    expect(onSelect).toHaveBeenCalledWith("knox");
  });
});
