import { fireEvent, render, screen, waitFor } from "@testing-library/react";

import { CheckInPanel } from "../../src/features/checkins/components/CheckInPanel";


describe("CheckInPanel", () => {
  it("shows loading then empty state", async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(new Response(JSON.stringify([]), { status: 200 }));

    vi.stubGlobal("fetch", fetchMock);

    render(
      <CheckInPanel
        apiBaseUrl="http://localhost:8000"
        token="11111111-1111-1111-1111-111111111111"
        onSubmitToChat={vi.fn()}
      />
    );

    expect(screen.getByTestId("checkins-loading")).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByTestId("checkins-empty")).toBeInTheDocument();
    });
  });

  it("shows active check-ins list and submits response", async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(
        new Response(
          JSON.stringify([
            {
              id: "11111111-1111-1111-1111-111111111111",
              commitmentId: "22222222-2222-2222-2222-222222222222",
              promptText: "You committed to 30-minute evening walks every day. How did it go?",
              triggerEvent: "commitment_created",
              status: "pending"
            }
          ]),
          { status: 200 }
        )
      )
      .mockResolvedValueOnce(
        new Response(
          JSON.stringify({
            followUpMessage: "Recovery framing: reset tonight and hit one walk tomorrow."
          }),
          { status: 200 }
        )
      );

    vi.stubGlobal("fetch", fetchMock);
    const onSubmitToChat = vi.fn();

    render(
      <CheckInPanel
        apiBaseUrl="http://localhost:8000"
        token="11111111-1111-1111-1111-111111111111"
        onSubmitToChat={onSubmitToChat}
      />
    );

    await waitFor(() => {
      expect(screen.getByTestId("checkins-list")).toBeInTheDocument();
      expect(screen.getByText(/30-minute evening walks/i)).toBeInTheDocument();
    });

    fireEvent.change(screen.getByLabelText("checkin-response-11111111-1111-1111-1111-111111111111"), {
      target: { value: "I did not complete it" }
    });
    fireEvent.click(screen.getByText("Submit"));

    await waitFor(() => {
      expect(onSubmitToChat).toHaveBeenCalledWith("Recovery framing: reset tonight and hit one walk tomorrow.");
    });
  });
});
