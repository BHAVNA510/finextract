from pydantic import BaseModel, Field
from typing import Optional

class FinancialData(BaseModel):
    """Schema for extracting financial KPIs from text"""
    
    company_name: str = Field(
        description="Full name of the company"
    )
    revenue: Optional[float] = Field(
        default=None,
        description="Total revenue in billions USD or INR crores"
    )
    growth_percentage: Optional[float] = Field(
        default=None,
        description="Year over year growth percentage"
    )
    quarter: Optional[str] = Field(
        default=None,
        description="Quarter like Q1, Q2, Q3, Q4"
    )
    year: Optional[int] = Field(
        default=None,
        description="Fiscal year as a number like 2024"
    )
    net_income: Optional[float] = Field(
        default=None,
        description="Net income or profit in billions"
    )
    top_segment: Optional[str] = Field(
        default=None,
        description="Best performing business segment or product"
    )
    currency: Optional[str] = Field(
        default=None,
        description="Currency used like USD or INR"
    )