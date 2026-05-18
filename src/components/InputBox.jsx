import { useState, useRef } from "react";
import { useChat } from "../hooks/useChat";
import { useChatContext } from "../context/ChatContext";
import VoiceInput from "./VoiceInput";

export default function InputBox() {
  const [value, setValue] = useState("");
  const { sendMessage } = useChat();
  const { isLoading } = useChatContext();
  const textareaRef = useRef();

  const handleSend = () => {
    if (!value.trim() || isLoading) return;
    sendMessage(value.trim());
    setValue("");
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
    }
  };

  const handleKey = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleInput = (e) => {
    setValue(e.target.value);
    e.target.style.height = "auto";
    e.target.style.height = Math.min(e.target.scrollHeight, 140) + "px";
  };

  return (
    <div className="input-box-area">
      <div className="input-row">
        <textarea
          ref={textareaRef}
          className="question-input"
          value={value}
          onInput={handleInput}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={handleKey}
          placeholder="Ask a question about Ayurveda…"
          rows={1}
          disabled={isLoading}
        />
        <VoiceInput onTranscript={(t) => setValue((v) => v + t)} />
        <button
          className="send-btn"
          onClick={handleSend}
          disabled={!value.trim() || isLoading}
          title="Send"
        >
          <span className="material-symbols-outlined" style={{ fontSize: '1.3rem', fontVariationSettings: "'FILL' 1" }}>send</span>
        </button>
      </div>
      <p className="input-hint">
        Answers are grounded in your uploaded knowledge base only · Enter to send
      </p>
    </div>
  );
}
