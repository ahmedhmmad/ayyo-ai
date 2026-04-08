import { ChatMessage, fetchSessionMessages, streamChat } from "../../../services/chatStreamClient";

export type ChatStoreState = {
  messages: ChatMessage[];
  loading: boolean;
  error: string | null;
};

export type ChatStore = ChatStoreState & {
  loadHistory: () => Promise<void>;
  sendMessage: (message: string) => Promise<void>;
};

export function createChatStore(apiBaseUrl: string, token: string, sessionId: string): ChatStore {
  const store: ChatStore = {
    messages: [],
    loading: false,
    error: null,
    async loadHistory() {
      store.loading = true;
      store.error = null;
      try {
        store.messages = await fetchSessionMessages(apiBaseUrl, token, sessionId);
      } catch (error) {
        store.error = error instanceof Error ? error.message : "Unknown error";
      } finally {
        store.loading = false;
      }
    },
    async sendMessage(message: string) {
      store.loading = true;
      store.error = null;
      store.messages = [...store.messages, { role: "user", content: message }];
      try {
        const assistant = await streamChat(apiBaseUrl, token, sessionId, message);
        store.messages = [...store.messages, { role: "assistant", content: assistant }];
      } catch (error) {
        store.error = error instanceof Error ? error.message : "Unknown error";
      } finally {
        store.loading = false;
      }
    }
  };
  return store;
}
