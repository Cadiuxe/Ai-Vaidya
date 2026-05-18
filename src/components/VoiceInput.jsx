import { useState, useRef } from "react";

export default function VoiceInput({ onTranscript }) {
  const [listening, setListening] = useState(false);
  const recognitionRef = useRef(null);

  const supported =
    typeof window !== "undefined" &&
    ("SpeechRecognition" in window || "webkitSpeechRecognition" in window);

  const toggle = () => {
    if (!supported) {
      alert("Voice input is not supported in this browser. Try Chrome.");
      return;
    }

    if (listening) {
      recognitionRef.current?.stop();
      setListening(false);
      return;
    }

    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SR();
    recognition.lang = "en-IN";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onresult = (e) => {
      const transcript = e.results[0][0].transcript;
      onTranscript(transcript);
    };
    recognition.onend = () => setListening(false);
    recognition.onerror = () => setListening(false);

    recognition.start();
    recognitionRef.current = recognition;
    setListening(true);
  };

  return (
    <button
      className={`voice-btn ${listening ? "listening" : ""}`}
      onClick={toggle}
      title={listening ? "Stop listening" : "Voice input"}
      type="button"
    >
      <span className="material-symbols-outlined" style={{ fontSize: '1.2rem', fontVariationSettings: listening ? "'FILL' 1" : "'FILL' 0" }}>
        {listening ? "stop_circle" : "mic"}
      </span>
    </button>
  );
}
