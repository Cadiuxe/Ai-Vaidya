import { useState, useRef } from "react";

export default function VoiceInput({ onTranscript }) {
  const [listening, setListening] = useState(false);
  const recognitionRef = useRef(null);

  const toggleListening = () => {
    if (listening) {
      recognitionRef.current?.stop();
      setListening(false);
      return;
    }

    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert("Speech recognition is not supported in this browser.");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;
    recognitionRef.current = recognition;

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      onTranscript(transcript);
      setListening(false);
    };

    recognition.onerror = () => setListening(false);
    recognition.onend = () => setListening(false);

    recognition.start();
    setListening(true);
  };

  return (
    <button
      className={`mic-btn ${listening ? "mic-btn--active" : ""}`}
      onClick={toggleListening}
      title={listening ? "Stop listening" : "Voice input"}
      type="button"
    >
      <span className="material-symbols-outlined">
        {listening ? "hearing" : "mic"}
      </span>
      {listening && <span className="mic-btn__pulse" />}
    </button>
  );
}
