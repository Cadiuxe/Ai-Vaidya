import { useCallback } from "react";
import { useChatContext } from "../context/ChatContext";

export function useChat() {
  const { messages, addMessage, setIsLoading, symptoms } = useChatContext();

  const sendMessage = useCallback(
    async (question) => {
      if (!question.trim()) return;

      // If there are active symptoms, prepend them as context
      let enrichedQuery = question;
      if (symptoms.length > 0) {
        enrichedQuery = `[Patient symptoms: ${symptoms.join(", ")}] ${question}`;
      }

      addMessage("user", question);
      setIsLoading(true);

      try {
        // Build chat context from recent messages for follow-up support
        const chatContext = messages.slice(-6).map((msg) => ({
          role: msg.role,
          content: msg.content,
        }));

        const API_URL = import.meta.env.VITE_API_URL || "";
        const response = await fetch(`${API_URL}/api/chat`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            query: enrichedQuery,
            chat_context: chatContext,
          }),
        });

        const data = await response.json();

        if (!response.ok) {
          addMessage("assistant", `⚠️ Error: ${data.error}`);
          return;
        }

        addMessage("assistant", data.answer || "", data.sources || [], data.chakras || []);
      } catch (err) {
        addMessage(
          "assistant",
          "⚠️ Connection error. Make sure the backend is running on port 5000."
        );
      } finally {
        setIsLoading(false);
      }
    },
    [addMessage, setIsLoading, messages, symptoms]
  );

  return { sendMessage };
}
