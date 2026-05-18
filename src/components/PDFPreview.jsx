import { useChatContext } from "../context/ChatContext";

export default function PDFPreview() {
  const { pdfName, pdfText } = useChatContext();
  const preview = pdfText?.substring(0, 300) + "…";

  return (
    <div className="pdf-preview">
      <div className="pdf-preview-header">
        <span className="material-symbols-outlined" style={{ fontSize: '1rem', color: 'var(--primary)' }}>picture_as_pdf</span>
        <span className="pdf-preview-name">{pdfName}</span>
      </div>
      <p className="pdf-preview-text">{preview}</p>
    </div>
  );
}
