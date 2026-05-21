export default function SourceCard({ source }) {
  const { file, page, text, relevance } = source;
  const scorePct = `${Math.round(Math.abs(relevance) * 100)}%`;

  return (
    <div className="source-card">
      <div className="source-card__icon-wrap">
        <span className="material-symbols-outlined source-card__icon">
          description
        </span>
      </div>
      <div className="source-card__info">
        <span className="source-card__filename">{file}</span>
        <span className="source-card__meta">
          Page {page} • {scorePct} match
        </span>
      </div>
      <span className="source-card__badge">Verified</span>
    </div>
  );
}
