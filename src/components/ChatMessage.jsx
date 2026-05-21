import SourceCard from "./SourceCard";
import ChakraDisplay from "./ChakraDisplay";

export default function ChatMessage({ message }) {
  const { role, content, sources, chakras } = message;
  const isUser = role === "user";

  // Parse markdown-style bold (**text**) and bullet points
  function renderContent(text) {
    if (!text) return null;

    const lines = text.split("\n");
    const elements = [];
    let bulletGroup = [];

    const flushBullets = () => {
      if (bulletGroup.length > 0) {
        elements.push(
          <ul key={`ul-${elements.length}`} className="message__list">
            {bulletGroup.map((item, i) => (
              <li key={i} dangerouslySetInnerHTML={{ __html: formatBold(item) }} />
            ))}
          </ul>
        );
        bulletGroup = [];
      }
    };

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim();
      if (!line) continue;

      if (line.startsWith("- ") || line.startsWith("* ")) {
        bulletGroup.push(line.replace(/^[-*]\s+/, ""));
      } else {
        flushBullets();
        elements.push(
          <p
            key={`p-${i}`}
            className="message__text"
            dangerouslySetInnerHTML={{ __html: formatBold(line) }}
          />
        );
      }
    }
    flushBullets();
    return elements;
  }

  function formatBold(text) {
    return text.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
  }

  return (
    <div className={`message message--${isUser ? "user" : "assistant"}`}>
      <div
        className={`message__bubble ${
          isUser ? "message__bubble--user" : "message__bubble--assistant"
        }`}
      >
        {isUser ? (
          <p className="message__text">{content}</p>
        ) : (
          renderContent(content)
        )}
      </div>

      {/* Chakra display (assistant only) */}
      {!isUser && chakras && chakras.length === 7 && (
        <ChakraDisplay chakras={chakras} />
      )}

      {/* Source cards (assistant only) */}
      {!isUser && sources && sources.length > 0 && (
        <div className="message__sources">
          {sources.map((src, i) => (
            <SourceCard key={i} source={src} />
          ))}
        </div>
      )}
    </div>
  );
}
