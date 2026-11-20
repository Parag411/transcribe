# Medical Dictation Transcription & SOAP Note Generator

Transcribes a provider dictation audio file using a **local Whisper model** and generates a structured SOAP note — no cloud APIs, no data leaves your machine.

## Tech Stack

| Task | Tool | Why |
|------|------|-----|
| Speech-to-Text | `faster-whisper` (medium) | Local, 4x faster than OpenAI Whisper, handles medical terminology |
| SOAP Generation | Ollama + llama3 (primary) | Local LLM, fully offline, privacy-preserving |
| SOAP Fallback | NLP extraction | Deterministic fallback if Ollama not available |

## Requirements

- Python 3.8+
- ~1.5 GB disk space for Whisper medium model

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/Parag411/transcribe.git
cd transcribe
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Download Whisper model (first run only, ~1.5 GB)
```bash
python -c "
import huggingface_hub
for f in ['config.json', 'model.bin', 'tokenizer.json', 'vocabulary.txt']:
    huggingface_hub.hf_hub_download(
        'Systran/faster-whisper-medium', f,
        local_dir='models/whisper-medium',
        local_dir_use_symlinks=False
    )
    print('Downloaded:', f)
"
```

### 4. (Optional) Install Ollama for LLM-based SOAP generation
Download from https://ollama.com/download, then:
```bash
ollama pull llama3
```
> If Ollama is not available, the notebook automatically falls back to deterministic NLP extraction.

### 5. Place the audio file
Copy `sample_dictation.mp3` into the project root directory.

## Run

```bash
jupyter notebook medical_soap_pipeline.ipynb
```

Run all cells top to bottom (`Kernel > Restart & Run All`).

Alternatively, run the standalone scripts:
```bash
python transcribe_test.py   # transcription only
python generate_soap.py     # SOAP note from transcript
```

## Output Files

| File | Description |
|------|-------------|
| `output/transcript.txt` | Verbatim transcription from Whisper |
| `output/soap_note.json` | Structured SOAP note in JSON |
| `output/soap_note.md` | Human-readable SOAP note in Markdown |

## Sample Output

**Diagnosis:** Lateral epicondylitis (Tennis Elbow) — right elbow

**SOAP Summary:**
- **S** — Lateral right elbow pain 4/10, achy/sharp, onset several months ago, worsened by repetitive wrist movements at work, no trauma
- **O** — Tenderness at lateral epicondyle, pain on wrist extension/flexion with elbow extended, no swelling/deformity/warmth
- **A** — Lateral epicondylitis (Tennis Elbow)
- **P** — Activity modification, ice, compression sleeve, physical therapy, continue NSAIDs

## Bonus: S/O Contamination Check

The notebook includes a validation step that scans the Objective section for patient-reported language and raises a warning if subjective content is detected in the wrong section.
