import { useRef, useEffect } from "react";
import { useChatContext } from "../context/ChatContext";
import { useChat } from "../hooks/useChat";
import ContextPanel from "./ContextPanel";
import SymptomChips from "./SymptomChips";
import ChatMessage from "./ChatMessage";
import ChatHistory from "./ChatHistory";
import InputBox from "./InputBox";
import Loader from "./Loader";

const SUGGESTIONS = [
  "What are the three doshas in Ayurveda?",
  "How does turmeric help in healing?",
  "What is Panchakarma?",
  "Herbs for cough and cold?",
];

export default function ChatScreen() {
  const { messages, isLoading, clearChat, setHistoryOpen, history } = useChatContext();
  const { sendMessage } = useChat();
  const chatEndRef = useRef(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  const isEmpty = messages.length === 0;

  return (
    <>
      {/* Header */}
      <header className="header">
        <div className="header__inner">
          <div className="header__brand">
            <span
              className="material-symbols-outlined header__icon"
              style={{ fontVariationSettings: "'FILL' 1" }}
            >
              eco
            </span>
            <h1 className="header__title">AI Vaidya</h1>
          </div>
          <div className="header__actions">
            {messages.length > 0 && (
              <button
                className="header__btn"
                onClick={clearChat}
                title="New conversation"
              >
                <span className="material-symbols-outlined">add</span>
                <span className="header__btn-label">New Chat</span>
              </button>
            )}
            <button
              className="header__btn header__btn--history"
              onClick={() => setHistoryOpen(true)}
              title="Chat history"
            >
              <span className="material-symbols-outlined">history</span>
              {history.length > 0 && (
                <span className="header__badge">{history.length}</span>
              )}
            </button>
          </div>
        </div>
      </header>

      {/* Context Panel (symptoms strip) */}
      <ContextPanel />

      {/* Chat Area */}
      <main className="chat-area">
        {isEmpty ? (
          /* Hero / Welcome Screen */
          <div className="hero">
            <div className="hero__icon-wrap">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="#775a19">
                <path d="M12 2C9.5 5 7 7 7 10c0 2.2 1.3 4 3.3 4.8C9.5 15.5 9 16.7 9 18h6c0-1.3-.5-2.5-1.3-3.2C15.7 14 17 12.2 17 10c0-3-2.5-5-5-8z" />
                <circle cx="12" cy="9" r="2" fill="#c5a059" />
              </svg>
            </div>
            <h2 className="hero__heading">
              Namaste. I am
              <br />
              your AI Vaidya.
            </h2>
            <p className="hero__subtitle">
              Describe your symptoms or ask about Ayurveda.
              <br />I will guide you with wisdom from ancient texts.
            </p>

            {/* Symptom Quick-Select */}
            <SymptomChips />

            <div className="hero__suggestions">
              <p className="hero__try-label">Or Ask Directly</p>
              <div className="hero__pills">
                {SUGGESTIONS.map((q) => (
                  <button
                    key={q}
                    className="suggestion-pill"
                    onClick={() => sendMessage(q)}
                  >
                    {q}
                  </button>
                ))}
              </div>
            </div>
          </div>
        ) : (
          /* Messages */
          <div className="messages">
            {messages.map((msg) => (
              <ChatMessage key={msg.id} message={msg} />
            ))}
            {isLoading && (
              <div className="message message--assistant">
                <div className="message__bubble message__bubble--assistant">
                  <Loader />
                </div>
              </div>
            )}
            <div ref={chatEndRef} />
          </div>
        )}
      </main>

      {/* Bottom Input */}
      <InputBox />

      {/* Chat History Sidebar */}
      <ChatHistory />
    </>
  );
}
