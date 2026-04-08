import { fireEvent, render, screen, waitFor } from "@testing-library/react";

import { MemoryPanel } from "../../src/features/memory/components/MemoryPanel";


describe("MemoryPanel", () => {
  it("supports loading, empty, error, edit, delete, and reset with confirmation", async () => {
    const listPayload = [
      {
        id: "11111111-1111-1111-1111-111111111111",
        category: "health_goal",
        key: "goal",
        value: "lose 10kg",
        source_type: "explicit",
        confidence_score: 1
      }
    ];

    const fetchMock = vi.fn()
      .mockResolvedValueOnce(new Response(JSON.stringify(listPayload), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify({ ...listPayload[0], value: "sleep 8h" }), { status: 200 }))
      .mockResolvedValueOnce(new Response(undefined, { status: 204 }))
      .mockResolvedValueOnce(new Response(undefined, { status: 204 }))
      .mockResolvedValueOnce(new Response(JSON.stringify([]), { status: 200 }));

    vi.stubGlobal("fetch", fetchMock);
    vi.spyOn(window, "confirm").mockReturnValue(true);

    render(<MemoryPanel apiBaseUrl="http://localhost:8000" token="11111111-1111-1111-1111-111111111111" />);

    expect(screen.getByTestId("memory-loading")).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByTestId("memory-list").textContent).toContain("lose 10kg");
    });

    fireEvent.change(screen.getByLabelText("edit-value-11111111-1111-1111-1111-111111111111"), {
      target: { value: "sleep 8h" }
    });
    fireEvent.click(screen.getByText("Save"));

    await waitFor(() => {
      expect(screen.getByTestId("memory-list").textContent).toContain("sleep 8h");
    });

    fireEvent.click(screen.getByText("Delete"));
    fireEvent.click(screen.getByText("Reset All"));

    await waitFor(() => {
      expect(screen.getByTestId("memory-empty")).toBeInTheDocument();
    });
  });
});
