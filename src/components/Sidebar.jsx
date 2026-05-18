import { useChatContext } from "../context/ChatContext";
import FileUpload from "./FileUpload";
import PDFPreview from "./PDFPreview";

const SAMPLE_TEXT = `FUNDAMENTALS OF AYURVEDA

Chapter 1: The Three Doshas

Ayurveda, the ancient Indian system of medicine, is founded on the theory of three biological energies called Doshas: Vata, Pitta, and Kapha. These three doshas govern all physiological and psychological functions of the body and mind.

Vata Dosha is composed of Space (Akasha) and Air (Vayu) elements. It governs movement, breathing, circulation, and nerve impulses. When Vata is in balance, it promotes creativity, flexibility, and vitality. Imbalanced Vata leads to anxiety, dry skin, constipation, and insomnia.

Pitta Dosha is composed of Fire (Agni) and Water (Jala) elements. It governs transformation, digestion, metabolism, and intelligence. When Pitta is balanced, it promotes intelligence, courage, and good digestion. Excess Pitta leads to inflammation, acid reflux, anger, and skin rashes.

Kapha Dosha is composed of Water (Jala) and Earth (Prithvi) elements. It provides structure, cohesion, and lubrication. When Kapha is balanced, it promotes love, patience, and immunity. Excess Kapha leads to weight gain, congestion, and lethargy.

Chapter 2: The Three Gunas

Sattva represents clarity, harmony, and purity. Foods that are sattvic include fresh fruits, vegetables, milk, and honey. A sattvic lifestyle leads to wisdom, compassion, and spiritual growth.

Rajas represents activity, passion, and stimulation. Rajasic foods include spicy, salty, and sour items. Excessive Rajas leads to restlessness, aggression, and greed.

Tamas represents inertia, heaviness, and darkness. Tamasic foods include meat, alcohol, and stale foods. Excessive Tamas leads to confusion, laziness, and ignorance.

Chapter 3: Agni — Digestive Fire

Agni, the digestive fire, is considered the most important factor in Ayurvedic medicine. The central Agni is called Jatharagni, located in the stomach and small intestine. When Jatharagni is balanced (Sama Agni), food is properly digested, nutrients are absorbed, and waste is efficiently eliminated.

Chapter 4: Medicinal Herbs

Turmeric (Haridra): Turmeric has powerful anti-inflammatory, antibacterial, and wound-healing properties. The active compound curcumin inhibits inflammatory pathways and promotes tissue regeneration. For wound healing, a paste of turmeric with ghee is applied topically.

Tulsi (Holy Basil): For cough and cold, Tulsi leaves boiled with ginger and black pepper creates a powerful decoction (Kashayam) that relieves congestion, reduces fever, and boosts immunity.

Ginger (Shunthi): Dry ginger is a powerful expectorant that removes excess Kapha from the lungs. Trikatu — dry ginger, black pepper, and long pepper — is a classical formula for cough, cold, and asthma.

Ashwagandha: A powerful adaptogen that strengthens the immune system, reduces stress, and improves stamina. Classified as a Rasayana (rejuvenating herb).

Chapter 5: Panchakarma

Panchakarma consists of five therapeutic procedures: Vamana (emesis), Virechana (purgation), Basti (enema), Nasya (nasal administration), and Raktamokshana (bloodletting). These cleanse the body of accumulated toxins (Ama) and restore doshic balance.`;

export default function Sidebar() {
  const {
    knowledgeBase,
    setKnowledgeBase,
    pdfName,
    pdfText,
    clearKnowledge,
    effectiveKnowledge,
  } = useChatContext();

  const charCount = effectiveKnowledge.length;

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <span className="sidebar-icon material-symbols-outlined" style={{ fontSize: '1.1rem' }}>auto_stories</span>
        <span className="sidebar-label">Knowledge Base</span>
        {effectiveKnowledge && (
          <button className="clear-kb-btn" onClick={clearKnowledge} title="Clear knowledge base">
            <span className="material-symbols-outlined" style={{ fontSize: '1rem' }}>close</span>
          </button>
        )}
      </div>

      <FileUpload />

      {pdfName && <PDFPreview />}

      {!pdfText && (
        <>
          <textarea
            className="knowledge-textarea"
            value={knowledgeBase}
            onChange={(e) => setKnowledgeBase(e.target.value)}
            placeholder="Or paste Ayurvedic text here — from books, scriptures, or research papers. The Vaidya will answer only from this knowledge..."
          />
          <div className="sidebar-footer">
            <span className="char-count">
              {charCount > 0 ? `${charCount.toLocaleString()} characters` : "No text loaded"}
            </span>
            <button
              className="sample-btn"
              onClick={() => setKnowledgeBase(SAMPLE_TEXT)}
            >
              <span className="material-symbols-outlined" style={{ fontSize: '0.9rem', marginRight: '4px', verticalAlign: 'text-bottom' }}>menu_book</span>
              Load Sample Text
            </button>
          </div>
        </>
      )}

      {pdfText && (
        <div className="sidebar-footer">
          <span className="char-count">{charCount.toLocaleString()} characters from PDF</span>
        </div>
      )}
    </aside>
  );
}
