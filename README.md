# 🧠 TalkToTasks – Intelligent Meeting Summarizer & Action Item Extractor

A desktop-based NLP tool that automatically summarizes meeting transcripts and extracts actionable tasks, helping professionals stay organized and focused.

---

## 🚀 Features

- 📝 **Transcript Summarization** using NLP techniques
- ✅ **Action Item Extraction** with regex & keyword rules
- 📊 **Word Frequency Visualization** via Matplotlib
- 💡 **Keyword Filtering** to focus on key topics
- 🧱 **Offline Desktop App** built with Python & Tkinter
- 🌙 **Dark Mode UI** for better readability
- 📤 **Export Outputs** as CSV & PDF

---

## 🧰 Tech Stack

| Category    | Tools Used                                      |
|-------------|--------------------------------------------------|
| Language    | Python 3.13                                     |
| NLP         | Custom rules, keyword matching, TextRank/NLTK   |
| UI/UX       | Tkinter (Dark Mode, Responsive UI)              |
| Visualization | Matplotlib                                     |
| File Handling | PyMuPDF, CSV, PDF Export (fpdf)               |
| Deployment  | Offline executable (optional .exe build)        |

---

## 🗂️ Folder Structure
TalkToTasks/
├── talktotasks_gui.py # GUI main file
├── summarizer.py # Summary & keyword logic
├── extractor.py # Action item extraction
├── utils/ # Helper functions
├── transcripts/ # Sample meeting transcripts
├── outputs/ # Exported PDFs/CSVs
├── requirements.txt # All dependencies
└── README.md


---

## 🧪 How to Run

```bash
pip install -r requirements.txt
python talktotasks_gui.py
