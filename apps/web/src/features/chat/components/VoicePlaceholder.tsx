export function VoicePlaceholder() {
  return (
    <section aria-label="voice-placeholder" data-testid="voice-placeholder">
      <h3>Voice</h3>
      <p data-testid="voice-coming-soon">Coming Soon</p>
      <button type="button" disabled aria-disabled="true">
        Start Voice (Coming Soon)
      </button>
    </section>
  );
}
