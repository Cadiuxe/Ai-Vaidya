import { useState, useEffect } from "react";

const CHAKRA_INFO = [
  { name: "Root",        sanskrit: "Mūlādhāra",   color: "#E53935", position: "Base of spine",   element: "Earth" },
  { name: "Sacral",      sanskrit: "Svādhiṣṭhāna", color: "#FB8C00", position: "Below navel",     element: "Water" },
  { name: "Solar Plexus", sanskrit: "Maṇipūra",    color: "#FDD835", position: "Stomach",         element: "Fire"  },
  { name: "Heart",       sanskrit: "Anāhata",      color: "#43A047", position: "Heart center",     element: "Air"   },
  { name: "Throat",      sanskrit: "Viśuddha",     color: "#1E88E5", position: "Throat",           element: "Ether" },
  { name: "Third Eye",   sanskrit: "Ājñā",         color: "#5E35B1", position: "Forehead",         element: "Light" },
  { name: "Crown",       sanskrit: "Sahasrāra",    color: "#AB47BC", position: "Top of head",      element: "Cosmic" },
];

export default function ChakraDisplay({ chakras }) {
  const [visible, setVisible] = useState(false);
  const [animStep, setAnimStep] = useState(0);

  useEffect(() => {
    const t1 = setTimeout(() => setVisible(true), 300);
    const t2 = setTimeout(() => setAnimStep(1), 600);  // start glow
    const t3 = setTimeout(() => setAnimStep(2), 1200); // full reveal
    return () => { clearTimeout(t1); clearTimeout(t2); clearTimeout(t3); };
  }, []);

  if (!chakras || chakras.length !== 7) return null;

  const blockedCount = chakras.filter((c) => c.blocked).length;

  return (
    <div className={`chakra-display ${visible ? "chakra-display--visible" : ""}`}>
      <div className="chakra-display__header">
        <span className="material-symbols-outlined chakra-display__icon">
          self_improvement
        </span>
        <span className="chakra-display__title">Chakra Analysis</span>
      </div>

      <div className="chakra-display__spine">
        {/* Energy line connecting chakras */}
        <div className="chakra-spine-line" />

        {/* Chakras rendered bottom-to-top (Root at bottom, Crown at top) */}
        {[...CHAKRA_INFO].reverse().map((info, visualIdx) => {
          const dataIdx = 6 - visualIdx; // map visual position to data index
          const data = chakras[dataIdx];
          const isBlocked = data?.blocked;

          return (
            <div
              key={info.name}
              className={`chakra-node ${isBlocked ? "chakra-node--blocked" : "chakra-node--balanced"} ${animStep >= 1 ? "chakra-node--animate" : ""}`}
              style={{ animationDelay: `${visualIdx * 0.1}s` }}
            >
              {/* Glow ring */}
              <div
                className="chakra-node__glow"
                style={{
                  borderColor: isBlocked ? "rgba(186, 26, 26, 0.4)" : info.color,
                  boxShadow: isBlocked
                    ? "0 0 12px rgba(186, 26, 26, 0.2)"
                    : `0 0 16px ${info.color}40`,
                }}
              />

              {/* Core circle */}
              <div
                className="chakra-node__core"
                style={{
                  background: isBlocked
                    ? "rgba(186, 26, 26, 0.15)"
                    : `${info.color}20`,
                  borderColor: isBlocked ? "var(--error)" : info.color,
                }}
              >
                {isBlocked ? (
                  <span className="material-symbols-outlined chakra-node__status" style={{ color: "var(--error)" }}>
                    block
                  </span>
                ) : (
                  <span className="material-symbols-outlined chakra-node__status" style={{ color: info.color }}>
                    check_circle
                  </span>
                )}
              </div>

              {/* Label */}
              <div className="chakra-node__info">
                <span className="chakra-node__name">{info.name}</span>
                <span className="chakra-node__sanskrit">{info.sanskrit}</span>
              </div>

              {/* Status badge */}
              <span className={`chakra-node__badge ${isBlocked ? "chakra-node__badge--blocked" : ""}`}>
                {isBlocked ? "Imbalanced" : "Balanced"}
              </span>
            </div>
          );
        })}
      </div>

      {/* Summary */}
      {animStep >= 2 && blockedCount > 0 && (
        <div className="chakra-display__summary">
          <span className="material-symbols-outlined">info</span>
          <p>
            {blockedCount === 1 ? "1 chakra needs" : `${blockedCount} chakras need`} attention.
            Focus on balancing through appropriate Ayurvedic practices.
          </p>
        </div>
      )}
    </div>
  );
}
