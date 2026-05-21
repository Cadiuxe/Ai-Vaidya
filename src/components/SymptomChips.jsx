import { useChatContext } from "../context/ChatContext";

const SYMPTOM_CHIPS = [
  { icon: "gastroenterology", label: "Digestive Issues" },
  { icon: "psychology", label: "Stress & Anxiety" },
  { icon: "rheumatology", label: "Joint Pain" },
  { icon: "dermatology", label: "Skin Problems" },
  { icon: "bedtime", label: "Sleep Issues" },
  { icon: "pulmonology", label: "Respiratory" },
  { icon: "headphones", label: "Headache" },
  { icon: "favorite", label: "Heart Health" },
];

export default function SymptomChips() {
  const { addSymptom, symptoms } = useChatContext();

  return (
    <div className="symptom-chips">
      <p className="symptom-chips__label">Common Concerns</p>
      <div className="symptom-chips__row">
        {SYMPTOM_CHIPS.map((chip) => {
          const isActive = symptoms.includes(chip.label);
          return (
            <button
              key={chip.label}
              className={`symptom-chip ${isActive ? "symptom-chip--active" : ""}`}
              onClick={() => addSymptom(chip.label)}
              disabled={isActive}
            >
              <span className="material-symbols-outlined symptom-chip__icon">
                {chip.icon}
              </span>
              <span className="symptom-chip__text">{chip.label}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
