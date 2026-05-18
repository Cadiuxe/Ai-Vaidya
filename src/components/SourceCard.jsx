import { useState } from "react";

export default function SourceCard({ text }) {
  const [expanded, setExpanded] = useState(false);
  const short = text.length > 120 ? text.substring(0, 120) + "…" : text;

  return (
    <div className="source-card">
      <div className="source-card-header">
        <span className="source-label">
          <span className="material-symbols-outlined" style={{ fontSize: '0.85rem', marginRight: '4px', verticalAlign: 'text-bottom' }}>description</span>
          Reference from Knowledge Base
        </span>
        {text.length > 120 && (
          <button
            className="source-toggle"
            onClick={() => setExpanded((e) => !e)}
          >
            {expanded ? "Show less" : "Show more"}
          </button>
        )}
      </div>
      <p className="source-text">{expanded ? text : short}</p>
    </div>
  );
}
