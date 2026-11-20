import json
from pathlib import Path

transcript = Path("output/transcript.txt").read_text(encoding="utf-8")

soap = {
    "Subjective": {
        "Chief Complaint": "Pain on the outside of the right elbow for several months, progressively worsening.",
        "History of Present Illness": (
            "Patient reports lateral right elbow pain onset several months ago with no trauma or trigger. "
            "Pain is achy and sometimes sharp (4/10), worsened by wrist flexion/extension and lifting heavy "
            "objects at work (repetitive assembly line work). Resting and ibuprofen provide relief. "
            "OTC topical ointment also helped. Pain is progressive and starting to affect work performance."
        ),
        "Pain Scale": "4/10",
        "Past Medical History": "C-section approximately 17 years ago (non-emergency). Otherwise healthy with no chronic conditions.",
        "Current Medications": "Tylenol (acetaminophen) and Advil (ibuprofen) PRN for pain.",
        "Allergies": "No known drug allergies.",
        "Review of Systems": (
            "Denies: weight loss, fever/chills, fatigue, rashes, sensory changes (vision/hearing/smell/taste), "
            "cough, shortness of breath, chest pain, palpitations, dizziness, nausea/vomiting, "
            "bowel/urinary changes, memory loss, numbness/tingling, radiation of pain, cold sensation in arm. "
            "Full ROM of right elbow and hand maintained. Pain isolated to lateral right elbow."
        )
    },
    "Objective": {
        "Vital Signs": "Not documented.",
        "Physical Examination": (
            "Right elbow: No redness, swelling, skin changes, or deformities. No asymmetry vs left elbow. "
            "No warmth on palpation. Tenderness on palpation of lateral epicondyle. "
            "No tenderness on medial aspect, forearm, or biceps. "
            "Pain reproduced with wrist extension and wrist flexion with elbow in full extension. "
            "No pain with elbow flexion, shoulder extension, shoulder adduction, "
            "forearm pronation or supination."
        ),
        "Diagnostic Results": (
            "No imaging ordered. Clinician determined imaging not necessary given absence of trauma "
            "and low concern for fracture."
        )
    },
    "Assessment": {
        "Primary Diagnosis": "Lateral epicondylitis (Tennis Elbow) — right elbow.",
        "Differential Diagnosis": "Radial tunnel syndrome, posterior interosseous nerve entrapment, elbow osteoarthritis."
    },
    "Plan": {
        "Treatment": (
            "1. Activity modification: avoid repetitive wrist extensor movements at work. "
            "2. Ice application for pain and swelling. "
            "3. Compression sleeve. "
            "4. Physical therapy to improve mobility and strength in right arm."
        ),
        "Medications Prescribed": "Continue Tylenol (acetaminophen) and NSAIDs (ibuprofen/Advil) PRN for pain.",
        "Follow Up": (
            "Expected resolution in a few months with conservative management; may take up to 6 months to 2 years. "
            "Consider splinting if symptoms persist."
        ),
        "Patient Education": (
            "Explained diagnosis of lateral epicondylitis (tennis elbow). Likely caused by repetitive strain "
            "and continuous contraction of wrist extensor muscle group at work. "
            "Reassured no fracture concern and no imaging required. "
            "Advised on activity modification, compression sleeve, ice therapy, and physical therapy."
        )
    }
}

# Save JSON
Path("output/soap_note.json").write_text(json.dumps(soap, indent=2), encoding="utf-8")
print("Saved: output/soap_note.json")

# Save Markdown
lines = ["# SOAP Note\n"]
icons = {"Subjective": "S", "Objective": "O", "Assessment": "A", "Plan": "P"}
for section, fields in soap.items():
    lines.append(f"## {icons[section]} — {section}\n")
    for key, value in fields.items():
        if value:
            lines.append(f"**{key}:** {value}\n")
    lines.append("")
Path("output/soap_note.md").write_text("\n".join(lines), encoding="utf-8")
print("Saved: output/soap_note.md")

# Validation: check for S/O contamination
subjective_keywords = ["patient reports", "patient states", "complains of", "rates pain", "denies", "reports", "states"]
obj_text = " ".join(soap["Objective"].values()).lower()
warnings = [kw for kw in subjective_keywords if kw in obj_text]
if warnings:
    print(f"WARNING - S/O contamination detected: {warnings}")
else:
    print("SOAP validation passed — no S/O contamination detected.")

print("\n--- SOAP NOTE ---")
print(json.dumps(soap, indent=2))
