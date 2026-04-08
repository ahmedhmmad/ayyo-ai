import { render, screen, waitFor } from "@testing-library/react";

import { ChatPanel } from "../../src/features/chat/components/ChatPanel";
import { GuidanceMessageCard } from "../../src/features/chat/components/GuidanceMessageCard";


describe("ChatPanel guidance rendering", () => {
  it("renders structured guidance card inside chat", async () => {
    const guidance = JSON.stringify({
      type: "guidance_plan",
      title: "3-Day Constraint Plan",
      steps: [
        { order: 1, action: "Zone 2 walk", scheduleHint: "Mon" },
        { order: 2, action: "Mobility", scheduleHint: "Wed" }
      ],
      constraints: ["no jumping"]
    });

    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(
        new Response(
          JSON.stringify([{ role: "assistant", content: guidance }]),
          { status: 200 }
        )
      );

    vi.stubGlobal("fetch", fetchMock);

    render(
      <ChatPanel
        apiBaseUrl="http://localhost:8000"
        token="11111111-1111-1111-1111-111111111111"
        sessionId="11111111-1111-1111-1111-111111111111"
      />
    );

    await waitFor(() => {
      expect(screen.getByTestId("guidance-card")).toBeInTheDocument();
      expect(screen.getByText("3-Day Constraint Plan")).toBeInTheDocument();
      expect(screen.getByText("no jumping")).toBeInTheDocument();
    });
  });

  it("shows loading and error states for guidance message card", () => {
    const { rerender } = render(
      <GuidanceMessageCard
        content={JSON.stringify({ type: "guidance_plan", title: "Plan", steps: [] })}
        loading
      />
    );

    expect(screen.getByTestId("guidance-loading")).toBeInTheDocument();

    rerender(<GuidanceMessageCard content="not-json" />);
    expect(screen.getByTestId("guidance-error")).toBeInTheDocument();
  });
});
