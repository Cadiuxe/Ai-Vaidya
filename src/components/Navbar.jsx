import { useChatContext } from "../context/ChatContext";

export default function Navbar() {
  const { clearChat, sidebarOpen, setSidebarOpen } = useChatContext();

  return (
    <nav className="navbar">
      <button
        className="sidebar-toggle"
        onClick={() => setSidebarOpen((o) => !o)}
        title="Toggle sidebar"
      >
        <span className="material-symbols-outlined">
          {sidebarOpen ? "left_panel_close" : "left_panel_open"}
        </span>
      </button>

      <div className="nav-brand">
        <span className="nav-om material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 1" }}>
          self_improvement
        </span>
        <div className="nav-titles">
          <h1 className="nav-title">AI VAIDYA</h1>
          <p className="nav-subtitle">Sacred Digital Wisdom</p>
        </div>
      </div>

      <div className="nav-actions">
        <a href="/" className="nav-link">Home</a>
        <a href="/about" className="nav-link">About</a>
        <button className="nav-btn-clear" onClick={clearChat}>
          Clear Chat
        </button>
      </div>
    </nav>
  );
}
