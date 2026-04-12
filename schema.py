from pydantic import BaseModel, Field, field_validator
from typing import Optional

class FinancialData(BaseModel):
    """
    Schema for extracting financial KPIs from unstructured text.
    All fields except company_name are Optional because not every
    financial text mentions every metric.
    """
    
    # ── Core Identity ──────────────────────────────────────────
    company_name: str = Field(
        description="Full official name of the company"
    )
    ticker_symbol: Optional[str] = Field(
        default=None,
        description="Stock ticker symbol like RELIANCE, TCS, AAPL"
    )
    
    # ── Revenue Metrics ────────────────────────────────────────
    revenue: Optional[float] = Field(
        default=None,
        description="Total revenue as a number in billions"
    )
    revenue_growth_percentage: Optional[float] = Field(
        default=None,
        description="Year over year revenue growth as percentage"
    )
    net_income: Optional[float] = Field(
        default=None,
        description="Net income or profit in billions"
    )
    operating_profit: Optional[float] = Field(
        default=None,
        description="Operating profit or EBITDA in billions"
    )
    profit_margin: Optional[float] = Field(
        default=None,
        description="Net profit margin as percentage"
    )
    
    # ── Time Period ────────────────────────────────────────────
    quarter: Optional[str] = Field(
        default=None,
        description="Quarter like Q1, Q2, Q3, Q4"
    )
    year: Optional[int] = Field(
        default=None,
        description="Fiscal year as 4 digit number like 2024"
    )
    period_type: Optional[str] = Field(
        default=None,
        description="Whether data is quarterly or annual"
    )
    
    # ── Business Details ───────────────────────────────────────
    top_segment: Optional[str] = Field(
        default=None,
        description="Best performing business segment or product line"
    )
    segment_growth: Optional[float] = Field(
        default=None,
        description="Growth percentage of the top performing segment"
    )
    headcount: Optional[int] = Field(
        default=None,
        description="Total number of employees if mentioned"
    )
    
    # ── Market Data ────────────────────────────────────────────
    currency: Optional[str] = Field(
        default=None,
        description="Currency code like USD, INR, EUR, GBP"
    )
    market_cap: Optional[float] = Field(
        default=None,
        description="Market capitalization in billions if mentioned"
    )
    guidance: Optional[str] = Field(
        default=None,
        description="Future guidance or outlook statement if mentioned"
    )
    
    # ── Sentiment ──────────────────────────────────────────────
    overall_sentiment: Optional[str] = Field(
        default=None,
        description="Overall tone of the report: positive, negative, or neutral"
    )

    # ── Validators ─────────────────────────────────────────────
    
    @field_validator("quarter")
    @classmethod
    def validate_quarter(cls, v):
        """Ensures quarter is always in correct format Q1/Q2/Q3/Q4"""
        if v is None:
            return v
        v = v.upper().strip()
        valid_quarters = ["Q1", "Q2", "Q3", "Q4"]
        if v not in valid_quarters:
            # Try to fix common variations like "Q 1" or "first quarter"
            if "1" in v or "ONE" in v.upper() or "FIRST" in v.upper():
                return "Q1"
            elif "2" in v or "TWO" in v.upper() or "SECOND" in v.upper():
                return "Q2"
            elif "3" in v or "THREE" in v.upper() or "THIRD" in v.upper():
                return "Q3"
            elif "4" in v or "FOUR" in v.upper() or "FOURTH" in v.upper():
                return "Q4"
        return v

    @field_validator("year")
    @classmethod
    def validate_year(cls, v):
        """Ensures year is a realistic fiscal year"""
        if v is None:
            return v
        if v < 2000 or v > 2030:
            raise ValueError(f"Year {v} seems unrealistic for a financial report")
        return v

    @field_validator("revenue_growth_percentage", "profit_margin", "segment_growth")
    @classmethod
    def validate_percentage(cls, v):
        """Ensures percentages are in realistic range"""
        if v is None:
            return v
        if v > 1000 or v < -100:
            raise ValueError(f"Percentage {v} seems unrealistic")
        return round(v, 2)

    @field_validator("currency")
    @classmethod
    def validate_currency(cls, v):
        """Standardizes currency codes to uppercase"""
        if v is None:
            return v
        return v.upper().strip()

    @field_validator("overall_sentiment")
    @classmethod
    def validate_sentiment(cls, v):
        """Ensures sentiment is one of three valid values"""
        if v is None:
            return v
        v = v.lower().strip()
        if v not in ["positive", "negative", "neutral"]:
            return "neutral"
        return v

    # ── Helper Methods ─────────────────────────────────────────

    def to_display_dict(self) -> dict:
        """
        Returns a clean dictionary for display in Streamlit.
        Renames fields to human-readable names and removes None values.
        """
        field_labels = {
            "company_name": "Company",
            "ticker_symbol": "Ticker",
            "revenue": "Revenue (B)",
            "revenue_growth_percentage": "Revenue Growth %",
            "net_income": "Net Income (B)",
            "operating_profit": "Operating Profit (B)",
            "profit_margin": "Profit Margin %",
            "quarter": "Quarter",
            "year": "Year",
            "period_type": "Period",
            "top_segment": "Top Segment",
            "segment_growth": "Segment Growth %",
            "headcount": "Employees",
            "currency": "Currency",
            "market_cap": "Market Cap (B)",
            "guidance": "Guidance",
            "overall_sentiment": "Sentiment"
        }
        
        result = {}
        data = self.model_dump()
        for field, label in field_labels.items():
            value = data.get(field)
            if value is not None:
                result[label] = value
        return result

    def summary(self) -> str:
        """
        Returns a one-line human readable summary of extracted data.
        Useful for logging and quick review.
        """
        parts = [f"{self.company_name}"]
        if self.quarter and self.year:
            parts.append(f"{self.quarter} {self.year}")
        if self.revenue:
            curr = self.currency or ""
            parts.append(f"Revenue: {self.revenue}B {curr}")
        if self.revenue_growth_percentage:
            parts.append(f"Growth: {self.revenue_growth_percentage}%")
        if self.overall_sentiment:
            parts.append(f"Sentiment: {self.overall_sentiment}")
        return " | ".join(parts)