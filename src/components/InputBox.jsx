import { useState, useRef } from "react";
import { useChat } from "../hooks/useChat";
import { useChatContext } from "../context/ChatContext";
import VoiceInput from "./VoiceInput";

export default function InputBox() {
  const [value, setValue] = useState("");
  const { sendMessage } = useChat();
  const { isLoading, symptoms } = useChatContext();
  const inputRef = useRef();

  const handleSend = () => {
    if (!value.trim() || isLoading) return;
    sendMessage(value.trim());
    setValue("");
    inputRef.current?.focus();
  };

  const handleKey = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const placeholder = symptoms.length > 0
    ? `Ask about your ${symptoms[0]}${symptoms.length > 1 ? " and more" : ""}...`
    : "Describe your symptoms or ask about Ayurveda...";

  return (
    <div className="input-area">
      <div className="input-area__inner">
        <div className="input-row">
          <VoiceInput onTranscript={(t) => setValue((v) => (v ? v + " " + t : t))} />
          <input
            ref={inputRef}
            className="input-field"
            type="text"
            value={value}
            onChange={(e) => setValue(e.target.value)}
            onKeyDown={handleKey}
            placeholder={placeholder}
            disabled={isLoading}
          />
          <button
            className="send-btn"
            onClick={handleSend}
            disabled={!value.trim() || isLoading}
            title="Send"
          >
            <span className="material-symbols-outlined">arrow_upward</span>
          </button>
        </div>
        <p className="input-hint">
          <span className="material-symbols-outlined input-hint__icon">
            verified_user
          </span>
          Answers grounded in your knowledge base only
          {symptoms.length > 0 && (
            <span className="input-hint__context">
              &nbsp;• {symptoms.length} symptom{symptoms.length !== 1 ? "s" : ""} tracked
            </span>
          )}
        </p>
      </div>
    </div>
  );
}
