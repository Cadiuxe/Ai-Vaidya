import SourceCard from "./SourceCard";

export default function ChatMessage({ message }) {
  const { role, content, sourceChunk } = message;
  const isUser = role === "user";

  return (
    <div className={`chat-message ${isUser ? "user" : "assistant"}`}>
      <div className="msg-avatar">
        <span className="material-symbols-outlined" style={{ fontSize: '1.1rem', fontVariationSettings: "'FILL' 1" }}>
          {isUser ? "person" : "spa"}
        </span>
      </div>
      <div className="msg-content-wrap">
        <div className="msg-bubble">
          {content.split("\n").map((line, i) => (
            <span key={i}>
              {line}
              {i < content.split("\n").length - 1 && <br />}
            </span>
          ))}
        </div>
        {sourceChunk && <SourceCard text={sourceChunk} />}
      </div>
    </div>
  );
}
