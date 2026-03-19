from groq import Groq
from dotenv import load_dotenv
from schema import FinancialData
import os
import json

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def extract_financial_data(text: str):
    
    prompt = f"""
    You are a financial data extraction expert.
    
    Extract financial KPIs from the text below and return 
    ONLY a valid JSON object with these exact fields:
    - company_name (string)
    - revenue (float or null)
    - growth_percentage (float or null)
    - quarter (string or null)
    - year (integer or null)
    - net_income (float or null)
    - top_segment (string or null)
    - currency (string or null)
    
    Return ONLY the JSON object. No explanation, no extra text.
    No markdown, no backticks, just pure JSON.
    
    Text to extract from:
    {text}
    """
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    
    result = response.choices[0].message.content
    
    # Print raw response so we can see what AI returned
    print("Raw AI response:")
    print(result)
    print("---")
    
    # Clean response in case AI added backticks
    result = result.strip()
    if result.startswith("```"):
        result = result.split("```")[1]
        if result.startswith("json"):
            result = result[4:]
    result = result.strip()
    
    # Convert to Python dictionary
    data = json.loads(result)
    
    # Validate against schema
    financial_data = FinancialData(**data)
    
    return financial_data


if __name__ == "__main__":
    test_text = """
    Reliance Industries reported quarterly revenue of 
    2.31 lakh crore rupees for Q3 2024, up 10.4% 
    year-over-year. Net income stood at 17,265 crore INR. 
    Jio platforms led growth with 28% segment increase.
    """
    
    result = extract_financial_data(test_text)
    print(result)