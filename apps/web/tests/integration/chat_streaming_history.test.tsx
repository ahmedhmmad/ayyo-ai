import { fireEvent, render, screen, waitFor } from "@testing-library/react";

import { KnoxWorkspacePage } from "../../src/features/chat/pages/KnoxWorkspacePage";

describe("KnoxWorkspacePage", () => {
  it("renders streamed chat and reloads history", async () => {
    const historyPayload = JSON.stringify([
      { role: "assistant", content: "Start now." }
    ]);
    const ssePayload = 'data: {"sessionId":"11111111-1111-1111-1111-111111111111","messageId":"22222222-2222-2222-2222-222222222222","token":"Do","done":false}\n\n' +
      'data: {"sessionId":"11111111-1111-1111-1111-111111111111","messageId":"22222222-2222-2222-2222-222222222222","token":" it.","done":true}\n\n';

    const fetchMock = vi.fn()
      .mockResolvedValueOnce(new Response(historyPayload, { status: 200 }))
      .mockResolvedValueOnce(new Response(ssePayload, { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify([
        { role: "assistant", content: "Start now." },
        { role: "user", content: "push" },
        { role: "assistant", content: "Do it." }
      ]), { status: 200 }));

    vi.stubGlobal("fetch", fetchMock);

    render(
      <KnoxWorkspacePage
        apiBaseUrl="http://localhost:8000"
        token="11111111-1111-1111-1111-111111111111"
        sessionId="11111111-1111-1111-1111-111111111111"
      />
    );

    await waitFor(() => {
      expect(screen.getByTestId("chat-list").textContent).toContain("assistant: Start now.");
    });

    fireEvent.change(screen.getByLabelText("message"), { target: { value: "push" } });
    fireEvent.click(screen.getByText("Send"));

    await waitFor(() => {
      expect(screen.getByTestId("chat-list").textContent).toContain("assistant: Do it.");
    });
  });
});
