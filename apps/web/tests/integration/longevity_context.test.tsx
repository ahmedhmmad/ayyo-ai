import { fireEvent, render, screen, waitFor } from "@testing-library/react";

import { ChatPanel } from "../../src/features/chat/components/ChatPanel";

describe("Longevity context in chat", () => {
  it("renders assistant response with natural longevity framing in chat stream", async () => {
    const historyPayload = JSON.stringify([]);
    const ssePayload =
      'data: {"sessionId":"11111111-1111-1111-1111-111111111111","messageId":"22222222-2222-2222-2222-222222222222","token":"Build habits that protect your long-term health and mobility.","done":true}\n\n';

    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(new Response(historyPayload, { status: 200 }))
      .mockResolvedValueOnce(new Response(ssePayload, { status: 200 }))
      .mockResolvedValueOnce(
        new Response(
          JSON.stringify([
            { role: "user", content: "How should I train?" },
            {
              role: "assistant",
              content: "Build habits that protect your long-term health and mobility."
            }
          ]),
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

    fireEvent.change(screen.getByLabelText("message"), { target: { value: "How should I train?" } });
    fireEvent.click(screen.getByText("Send"));

    await waitFor(() => {
      expect(screen.getByTestId("chat-list").textContent?.toLowerCase()).toContain("long-term health");
      expect(screen.getByTestId("longevity-context")).toBeInTheDocument();
    });
  });
});
