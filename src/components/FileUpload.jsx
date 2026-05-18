import { useRef, useState } from "react";
import { useChatContext } from "../context/ChatContext";

export default function FileUpload() {
  const { setPdfText, setPdfName, pdfName } = useChatContext();
  const inputRef = useRef();
  const [extracting, setExtracting] = useState(false);
  const [error, setError] = useState("");

  const extractPDFText = async (file) => {
    setExtracting(true);
    setError("");
    try {
      if (!window.pdfjsLib) {
        await new Promise((resolve, reject) => {
          const script = document.createElement("script");
          script.src =
            "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js";
          script.onload = resolve;
          script.onerror = reject;
          document.head.appendChild(script);
        });
        window.pdfjsLib.GlobalWorkerOptions.workerSrc =
          "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js";
      }

      const arrayBuffer = await file.arrayBuffer();
      const pdf = await window.pdfjsLib.getDocument({ data: arrayBuffer }).promise;
      let fullText = "";

      for (let i = 1; i <= pdf.numPages; i++) {
        const page = await pdf.getPage(i);
        const content = await page.getTextContent();
        const pageText = content.items.map((item) => item.str).join(" ");
        fullText += `\n[Page ${i}]\n${pageText}\n`;
      }

      setPdfText(fullText);
      setPdfName(file.name);
    } catch (err) {
      setError("Could not extract text from PDF. Please try a text-based PDF.");
    } finally {
      setExtracting(false);
    }
  };

  const handleFile = (file) => {
    if (!file) return;
    if (file.type !== "application/pdf") {
      setError("Only PDF files are supported.");
      return;
    }
    if (file.size > 20 * 1024 * 1024) {
      setError("File too large. Please upload a PDF under 20MB.");
      return;
    }
    extractPDFText(file);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    handleFile(e.dataTransfer.files[0]);
  };

  return (
    <div
      className={`file-upload-zone ${extracting ? "extracting" : ""}`}
      onDrop={handleDrop}
      onDragOver={(e) => e.preventDefault()}
      onClick={() => !extracting && inputRef.current.click()}
    >
      <input
        ref={inputRef}
        type="file"
        accept=".pdf"
        style={{ display: "none" }}
        onChange={(e) => handleFile(e.target.files[0])}
      />
      {extracting ? (
        <div className="upload-extracting">
          <span className="material-symbols-outlined spinner" style={{ fontSize: '1.2rem' }}>progress_activity</span>
          <span>Extracting text from PDF…</span>
        </div>
      ) : pdfName ? (
        <div className="upload-success">
          <span className="material-symbols-outlined" style={{ fontSize: '1.5rem', color: 'var(--primary)' }}>picture_as_pdf</span>
          <span className="pdf-name">{pdfName}</span>
          <span className="upload-change">Click to change</span>
        </div>
      ) : (
        <div className="upload-idle">
          <span className="upload-icon material-symbols-outlined">upload_file</span>
          <span className="upload-text">Upload Ayurveda PDF</span>
          <span className="upload-hint">Drag & drop or click · PDF up to 20MB</span>
        </div>
      )}
      {error && <p className="upload-error">{error}</p>}
    </div>
  );
}
