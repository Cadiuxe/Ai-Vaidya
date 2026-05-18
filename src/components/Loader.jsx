export default function Loader() {
  return (
    <div className="chat-message assistant">
      <div className="msg-avatar">
        <span className="material-symbols-outlined" style={{ fontSize: '1.1rem', fontVariationSettings: "'FILL' 1" }}>spa</span>
      </div>
      <div className="loader-bubble">
        <span className="loader-text">Consulting the ancient texts</span>
        <div className="dot-pulse">
          <span /><span /><span />
        </div>
      </div>
    </div>
  );
}
