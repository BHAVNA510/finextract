# FinExtract 💰
> An AI-powered financial KPI extractor that converts unstructured 
text into structured data using Groq LLaMA3 + Streamlit

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0-red)
![Groq](https://img.shields.io/badge/Groq-LLaMA3-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

## 🔗 Live Demo
Coming soon — deploying on Streamlit Cloud

## 📌 What problem does it solve?
Financial analysts waste hours manually reading earnings reports 
and news articles to extract key numbers like revenue, growth %, 
and net income. FinExtract automates this entirely using AI —
paste any financial text and get a clean structured table in seconds.

## ✨ Features
- Paste any financial news article or earnings report
- AI automatically extracts: Company, Revenue, Growth %, 
  Quarter, Year, Net Income, Top Segment, Currency
- Upload PDF files directly
- Download extracted data as CSV
- Works with both Indian (INR) and US (USD) financial data

## 🛠️ Tech Stack
| Tool | Purpose | Why I chose it |
|------|---------|----------------|
| Groq + LLaMA3 | Free LLM inference | Fast, free, no credit card needed |
| Pydantic | Structured output schema | Ensures consistent data extraction |
| Streamlit | Web interface | Build web apps in pure Python |
| PyPDF | PDF text extraction | So users can upload PDFs directly |
| Python dotenv | API key management | Keeps secrets safe from GitHub |

## 🏗️ Project Architecture
```
User Input (Text/PDF)
        ↓
   app.py (Streamlit UI)
        ↓
   extractor.py (Core Logic)
        ↓
   Groq API (LLaMA3 Model)
        ↓
   schema.py (Pydantic Validation)
        ↓
   Structured Output (Table + CSV)
```

## 📁 File Structure
```
finextract/
├── app.py          → Streamlit web interface
├── extractor.py    → AI extraction logic + prompt engineering
├── schema.py       → Pydantic data models
├── test.py         → API connection test
├── requirements.txt → Project dependencies
├── .env            → API key (not on GitHub)
└── .gitignore      → Files excluded from GitHub
```

## 🚀 Run Locally
1. Clone the repo
```bash
git clone https://github.com/BHAVNA510/finextract.git
cd finextract
```

2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Get free Groq API key from console.groq.com
   and create .env file:
```
GROQ_API_KEY=your-key-here
```

5. Run the app
```bash
streamlit run app.py
```

## 🧠 Key Concepts I Learned

<img width="866" height="498" alt="_- visual selection" src="https://github.com/user-attachments/assets/cfa6f9ee-f0e1-4f17-87d5-d829c2c137c2" />

## 📊 Sample Output

Input text:
```
TCS reported revenue of $29.1B for FY2024, 
up 4.1% YoY. Net income was $4.6B.
BFSI segment led with 31% of total revenue.
```

Output table:
| company | revenue | growth % | quarter | year | net_income | segment | currency |
|---------|---------|----------|---------|------|------------|---------|----------|
| TCS | 29.1 | 4.1 | null | 2024 | 4.6 | BFSI | USD |

## 👩‍💻 Author
**Bhavna** — Data & AI enthusiast
- GitHub: [@BHAVNA510](https://github.com/BHAVNA510)
- LinkedIn: [www.linkedin.com/in/bhavna51020]
- Email: bhavna51020@gmail.com

## 🗓️ Build Log
| Day | What I built |
|-----|-------------|
| Day 1 | Project setup, Groq API connection, core extraction engine |
| Day 2 | Streamlit UI, PDF support, GitHub push, documentation |
| Day 3 | GitHub push, documentation |
| Day 4 | Cloud deployment, GitHub push, documentation |
| Day 5 | GitHub changes |
| Day 6 | Extraction engine |
| Day 7 | GitHub changes |

