import { useChatContext } from "../context/ChatContext";

export default function ChatHistory() {
  const { history, historyOpen, setHistoryOpen, resumeChat, deleteHistoryEntry, clearHistory } =
    useChatContext();

  function formatDate(isoStr) {
    try {
      const d = new Date(isoStr);
      return d.toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    } catch {
      return "";
    }
  }

  return (
    <>
      {/* Overlay */}
      {historyOpen && (
        <div className="history-overlay" onClick={() => setHistoryOpen(false)} />
      )}

      {/* Sidebar */}
      <aside className={`history-sidebar ${historyOpen ? "history-sidebar--open" : ""}`}>
        <div className="history-sidebar__header">
          <h2 className="history-sidebar__title">
            <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 1" }}>
              history
            </span>
            Consultations
          </h2>
          <button
            className="history-sidebar__close"
            onClick={() => setHistoryOpen(false)}
            title="Close"
          >
            <span className="material-symbols-outlined">close</span>
          </button>
        </div>

        <div className="history-sidebar__body">
          {history.length === 0 ? (
            <div className="history-empty">
              <span className="material-symbols-outlined history-empty__icon">
                auto_stories
              </span>
              <p className="history-empty__text">
                No past consultations yet.
                <br />
                Start a conversation to build your history.
              </p>
            </div>
          ) : (
            <>
              <p className="history-sidebar__count">
                {history.length} consultation{history.length !== 1 ? "s" : ""}
              </p>

              {history.map((entry) => (
                <div key={entry.id} className="history-card">
                  <div className="history-card__top">
                    <span className="history-card__date">{formatDate(entry.timestamp)}</span>
                    <button
                      className="history-card__delete"
                      onClick={() => deleteHistoryEntry(entry.id)}
                      title="Delete"
                    >
                      <span className="material-symbols-outlined">delete_outline</span>
                    </button>
                  </div>
                  <p className="history-card__title">{entry.title}</p>
                  {entry.symptoms.length > 0 && (
                    <div className="history-card__symptoms">
                      {entry.symptoms.slice(0, 3).map((s) => (
                        <span key={s} className="history-card__tag">{s}</span>
                      ))}
                      {entry.symptoms.length > 3 && (
                        <span className="history-card__tag">+{entry.symptoms.length - 3}</span>
                      )}
                    </div>
                  )}
                  <div className="history-card__footer">
                    <span className="history-card__msgs">
                      {entry.messageCount} messages
                    </span>
                    <button
                      className="history-card__resume"
                      onClick={() => resumeChat(entry)}
                    >
                      Resume
                      <span className="material-symbols-outlined">arrow_forward</span>
                    </button>
                  </div>
                </div>
              ))}

              <button className="history-sidebar__clear" onClick={clearHistory}>
                <span className="material-symbols-outlined">delete_sweep</span>
                Clear All History
              </button>
            </>
          )}
        </div>
      </aside>
    </>
  );
}
