from groq import Groq
from dotenv import load_dotenv
from schema import FinancialData
import os
import json
import time
import logging

# Setup logging so we can track what's happening
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()

# Initialize Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def clean_llm_response(response: str) -> str:
    """
    Cleans LLM response by removing markdown formatting.
    LLMs often wrap JSON in backticks even when told not to.
    This function handles all common formatting patterns.
    """
    response = response.strip()
    
    # Remove ```json ... ``` wrapping
    if response.startswith("```"):
        lines = response.split("\n")
        # Remove first line (```json or ```)
        lines = lines[1:]
        # Remove last line (```)
        if lines[-1].strip() == "```":
            lines = lines[:-1]
        response = "\n".join(lines)
    
    return response.strip()


def extract_financial_data(text: str, max_retries: int = 3) -> FinancialData:
    """
    Extracts financial KPIs from any unstructured text.
    
    Args:
        text: Any financial news article or earnings report text
        max_retries: Number of times to retry if API fails (default 3)
    
    Returns:
        FinancialData object with extracted KPIs
    
    Raises:
        ValueError: If extraction fails after all retries
    """
    
    prompt = f"""
    You are a financial data extraction expert specializing in 
    earnings reports and financial news analysis.
    
    Extract financial KPIs from the text below and return 
    ONLY a valid JSON object with these exact fields:
    
    {{
        "company_name": "string - full company name",
        "revenue": "float or null - revenue as a number in billions",
        "growth_percentage": "float or null - YoY growth as percentage number",
        "quarter": "string or null - Q1/Q2/Q3/Q4",
        "year": "integer or null - fiscal year as 4 digit number",
        "net_income": "float or null - net income/profit as number in billions",
        "top_segment": "string or null - best performing business segment",
        "currency": "string or null - USD or INR or other currency code"
    }}
    
    STRICT RULES:
    - Return ONLY the JSON object
    - No explanation, no markdown, no backticks
    - Use null for fields not mentioned in the text
    - Convert all revenue/income to billions (divide crores by 10000)
    - Extract the most prominent company if multiple are mentioned
    
    Text to extract from:
    {text}
    """
    
    # Retry logic — try up to max_retries times
    for attempt in range(max_retries):
        try:
            logger.info(f"Extraction attempt {attempt + 1} of {max_retries}")
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a financial data extraction expert. Always return pure JSON only."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                temperature=0,      # Deterministic output
                max_tokens=500,     # KPIs don't need more than 500 tokens
            )
            
            # Get raw response
            raw_result = response.choices[0].message.content
            logger.info("Successfully received response from Groq")
            
            # Clean the response
            cleaned_result = clean_llm_response(raw_result)
            
            # Parse JSON
            data = json.loads(cleaned_result)
            
            # Validate against Pydantic schema
            financial_data = FinancialData(**data)
            
            logger.info(f"Successfully extracted data for: {financial_data.company_name}")
            return financial_data
            
        except json.JSONDecodeError as e:
            logger.warning(f"JSON parsing failed on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                logger.info("Retrying in 2 seconds...")
                time.sleep(2)
            else:
                raise ValueError(f"Failed to parse LLM response as JSON after {max_retries} attempts")
                
        except Exception as e:
            logger.warning(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                logger.info("Retrying in 2 seconds...")
                time.sleep(2)
            else:
                raise ValueError(f"Extraction failed after {max_retries} attempts: {str(e)}")


def extract_multiple_companies(text: str) -> list:
    """
    Extracts data when text mentions multiple companies.
    Splits extraction into separate calls per company.
    
    Args:
        text: Financial text mentioning multiple companies
    
    Returns:
        List of FinancialData objects
    """
    
    # First ask LLM to identify companies mentioned
    company_prompt = f"""
    List all company names mentioned in this financial text.
    Return ONLY a JSON array of company name strings.
    Example: ["Apple", "Microsoft", "Google"]
    No explanation, just the JSON array.
    
    Text: {text}
    """
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": company_prompt}],
        temperature=0
    )
    
    raw = clean_llm_response(response.choices[0].message.content)
    companies = json.loads(raw)
    
    logger.info(f"Found {len(companies)} companies: {companies}")
    
    # Extract data for each company
    results = []
    for company in companies:
        company_text = f"Focus only on {company}. {text}"
        try:
            data = extract_financial_data(company_text)
            results.append(data)
        except Exception as e:
            logger.warning(f"Failed to extract data for {company}: {e}")
    
    return results


# Test the extractor directly
if __name__ == "__main__":
    
    print("=" * 50)
    print("TEST 1: Single Company Extraction")
    print("=" * 50)
    
    test_text_1 = """
    Reliance Industries reported quarterly revenue of 
    2.31 lakh crore rupees for Q3 2024, up 10.4% 
    year-over-year. Net income stood at 17,265 crore INR. 
    Jio platforms led growth with 28% segment increase.
    """
    
    result1 = extract_financial_data(test_text_1)
    print(f"Company: {result1.company_name}")
    print(f"Revenue: {result1.revenue}")
    print(f"Growth: {result1.growth_percentage}%")
    print(f"Quarter: {result1.quarter} {result1.year}")
    print(f"Net Income: {result1.net_income}")
    print(f"Top Segment: {result1.top_segment}")
    print()
    
    print("=" * 50)
    print("TEST 2: TCS Extraction")
    print("=" * 50)
    
    test_text_2 = """
    TCS reported revenue of $29.1 billion for FY2024,
    representing 4.1% growth year-over-year.
    Net income came in at $4.6 billion.
    BFSI segment led with 31% of total revenue.
    """
    
    result2 = extract_financial_data(test_text_2)
    print(f"Company: {result2.company_name}")
    print(f"Revenue: {result2.revenue}B")
    print(f"Growth: {result2.growth_percentage}%")
    print(f"Currency: {result2.currency}")