import { createContext, useContext, useState, useCallback, useEffect } from "react";

const ChatContext = createContext(null);

const HISTORY_KEY = "aivaidya_history";

function loadHistory() {
  try {
    const raw = localStorage.getItem(HISTORY_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

function saveHistory(history) {
  try {
    localStorage.setItem(HISTORY_KEY, JSON.stringify(history));
  } catch { /* ignore quota errors */ }
}

export function ChatProvider({ children }) {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [symptoms, setSymptoms] = useState([]); // active symptom tags
  const [history, setHistory] = useState(loadHistory); // saved consultations
  const [historyOpen, setHistoryOpen] = useState(false);

  // Persist history to localStorage
  useEffect(() => {
    saveHistory(history);
  }, [history]);

  const addMessage = useCallback((role, content, sources = [], chakras = []) => {
    setMessages((prev) => [
      ...prev,
      { id: Date.now(), role, content, sources, chakras, timestamp: new Date().toISOString() },
    ]);
  }, []);

  const addSymptom = useCallback((symptom) => {
    const trimmed = symptom.trim();
    if (!trimmed) return;
    setSymptoms((prev) =>
      prev.includes(trimmed) ? prev : [...prev, trimmed]
    );
  }, []);

  const removeSymptom = useCallback((symptom) => {
    setSymptoms((prev) => prev.filter((s) => s !== symptom));
  }, []);

  const clearSymptoms = useCallback(() => setSymptoms([]), []);

  // Save current conversation to history and clear chat
  const saveAndClearChat = useCallback(() => {
    if (messages.length > 0) {
      const firstUserMsg = messages.find((m) => m.role === "user");
      const entry = {
        id: Date.now(),
        title: firstUserMsg?.content?.slice(0, 80) || "Consultation",
        symptoms: [...symptoms],
        messageCount: messages.length,
        timestamp: new Date().toISOString(),
        messages: messages,
      };
      setHistory((prev) => [entry, ...prev].slice(0, 50)); // keep last 50
    }
    setMessages([]);
  }, [messages, symptoms]);

  const clearChat = useCallback(() => {
    saveAndClearChat();
  }, [saveAndClearChat]);

  // Resume a past conversation
  const resumeChat = useCallback((entry) => {
    if (messages.length > 0) {
      saveAndClearChat();
    }
    setMessages(entry.messages || []);
    setSymptoms(entry.symptoms || []);
    setHistoryOpen(false);
  }, [messages, saveAndClearChat]);

  const deleteHistoryEntry = useCallback((id) => {
    setHistory((prev) => prev.filter((e) => e.id !== id));
  }, []);

  const clearHistory = useCallback(() => setHistory([]), []);

  return (
    <ChatContext.Provider
      value={{
        messages,
        setMessages,
        addMessage,
        clearChat,
        isLoading,
        setIsLoading,
        symptoms,
        addSymptom,
        removeSymptom,
        clearSymptoms,
        history,
        historyOpen,
        setHistoryOpen,
        resumeChat,
        deleteHistoryEntry,
        clearHistory,
      }}
    >
      {children}
    </ChatContext.Provider>
  );
}

export function useChatContext() {
  const ctx = useContext(ChatContext);
  if (!ctx) throw new Error("useChatContext must be used inside ChatProvider");
  return ctx;
}
