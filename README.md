# FinExtract 💰
> Extract structured financial KPIs from unstructured text using LangChain + Groq LLaMA3

## 🔗 Live Demo
Coming soon...

## 📌 What it does
- Paste any financial news article or earnings report
- Automatically extracts structured KPIs like Revenue, Growth %, Net Income, Quarter
- Upload PDF files directly
- Download extracted data as CSV

## 🛠️ Tech Stack
| Tool | Purpose |
|------|---------|
| LangChain | LLM orchestration and extraction chain |
| Groq + LLaMA3 | Free and fast LLM inference |
| Pydantic | Structured output schema definition |
| Streamlit | Web interface |
| PyPDF | PDF text extraction |
| Pandas | Data handling and CSV export |

## 🚀 Run Locally
1. Clone the repo
   git clone https://github.com/YOUR_USERNAME/finextract.git

2. Create virtual environment
   python -m venv venv
   venv\Scripts\activate

3. Install dependencies
   pip install -r requirements.txt

4. Add your Groq API key
   Create a .env file and add:
   GROQ_API_KEY=your-groq-key-here

5. Run the app
   streamlit run app.py

## 📁 Project Structure
finextract/
├── app.py              → Main Streamlit web app
├── extractor.py        → LangChain extraction logic
├── schema.py           → Pydantic data models
├── requirements.txt    → Project dependencies
├── .env                → API key (not pushed to GitHub)
├── .gitignore          → Files excluded from GitHub
└── README.md           → Project documentation

## 🧠 Concepts Demonstrated
- Prompt Engineering with structured output
- LangChain Extraction Chain
- Pydantic schema design
- Free LLM integration via Groq
- Streamlit web app development

## 👩‍💻 Author
Bhavna | [LinkedIn](www.linkedin.com/in/bhavna51020) | [GitHub](https://github.com/BHAVNA510)
