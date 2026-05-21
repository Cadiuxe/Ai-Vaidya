import { useState } from "react";
import { useChatContext } from "../context/ChatContext";

export default function ContextPanel() {
  const { symptoms, addSymptom, removeSymptom, clearSymptoms } = useChatContext();
  const [input, setInput] = useState("");

  const handleAdd = () => {
    if (input.trim()) {
      addSymptom(input.trim());
      setInput("");
    }
  };

  const handleKey = (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      handleAdd();
    }
  };

  return (
    <div className={`context-panel ${symptoms.length > 0 ? "context-panel--active" : ""}`}>
      <div className="context-panel__inner">
        <div className="context-panel__header">
          <span className="material-symbols-outlined context-panel__icon">
            medical_information
          </span>
          <span className="context-panel__label">Active Symptoms</span>
          {symptoms.length > 0 && (
            <button className="context-panel__clear" onClick={clearSymptoms} title="Clear all symptoms">
              <span className="material-symbols-outlined">close</span>
            </button>
          )}
        </div>

        <div className="context-panel__body">
          {/* Symptom Tags */}
          <div className="context-panel__tags">
            {symptoms.map((s) => (
              <span key={s} className="symptom-tag">
                {s}
                <button
                  className="symptom-tag__remove"
                  onClick={() => removeSymptom(s)}
                  title={`Remove ${s}`}
                >
                  <span className="material-symbols-outlined">close</span>
                </button>
              </span>
            ))}

            {/* Inline add input */}
            <div className="context-panel__add">
              <input
                className="context-panel__input"
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKey}
                placeholder="Add symptom..."
              />
              <button
                className="context-panel__add-btn"
                onClick={handleAdd}
                disabled={!input.trim()}
                title="Add symptom"
              >
                <span className="material-symbols-outlined">add</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
