import { useNavigate } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="home-page">
      <div className="home-content">
        <div className="home-om">
          <span className="material-symbols-outlined" style={{ fontSize: '3rem', fontVariationSettings: "'FILL' 1" }}>
            self_improvement
          </span>
        </div>
        <h1 className="home-title">AI VAIDYA</h1>
        <p className="home-tagline">
          An Intelligent Q&A Assistant for Ayurveda Knowledge
        </p>
        <p className="home-desc">
          Upload any Ayurvedic book, scripture, or research paper and ask
          questions in plain English. Every answer is grounded exclusively in
          your uploaded text — no hallucinations, no internet.
        </p>

        <div className="home-features">
          {[
            { icon: "upload_file", title: "PDF Upload", desc: "Ingest any Ayurveda book or research paper" },
            { icon: "travel_explore", title: "Semantic Q&A", desc: "Ask natural language questions about text" },
            { icon: "menu_book", title: "Source Citations", desc: "Every answer shows the reference passage" },
            { icon: "mic", title: "Voice Input", desc: "Ask questions by speaking to the assistant" },
          ].map((f) => (
            <div className="feature-card" key={f.title}>
              <span className="feature-icon material-symbols-outlined">{f.icon}</span>
              <h3 className="feature-title">{f.title}</h3>
              <p className="feature-desc">{f.desc}</p>
            </div>
          ))}
        </div>

        <button className="home-cta" onClick={() => navigate("/chat")}>
          Begin Consultation
          <span className="material-symbols-outlined" style={{ fontSize: '1rem' }}>arrow_forward</span>
        </button>
      </div>
    </div>
  );
}
