import { useEffect, useRef } from "react";
import { useChatContext } from "../context/ChatContext";
import ChatMessage from "./ChatMessage";
import Loader from "./Loader";
import SuggestedQuestions from "./SuggestedQuestions";

export default function ChatHistory() {
  const { messages, isLoading } = useChatContext();
  const bottomRef = useRef();

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  if (messages.length === 0) {
    return (
      <div className="chat-welcome">
        <div className="welcome-card">
          <span className="welcome-lotus material-symbols-outlined" style={{ fontSize: '2.5rem', fontVariationSettings: "'FILL' 1" }}>
            local_florist
          </span>
          <h2 className="welcome-title">Namaste. I am your AI Vaidya.</h2>
          <p className="welcome-desc">
            Upload an Ayurvedic PDF or paste text in the sidebar, then ask me
            anything. I will answer only from your provided knowledge base.
          </p>
          <SuggestedQuestions />
        </div>
      </div>
    );
  }

  return (
    <div className="chat-history">
      {messages.map((msg) => (
        <ChatMessage key={msg.id} message={msg} />
      ))}
      {isLoading && <Loader />}
      <div ref={bottomRef} />
    </div>
  );
}
