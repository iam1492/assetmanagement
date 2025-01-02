from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

class ReportToJsonInput(BaseModel):
    """Input schema for ReportToJsonInput."""
    company: str = Field(..., description="company name which is a string.")
    ticker: str = Field(..., description="ticker of the company which is a string.")
    rating: str = Field(..., description="Description of the argumentrating of the company which is a string. (example: Buy, Sell, Hold)")
    final_result: str = Field(..., description="Full output of the translator")
    
class ReportToJsonTool(BaseTool):
    name: str = "Report to JSON Converter"
    description: str = "Convert a translated final report to JSON format."
    args_schema: Type[BaseModel] = ReportToJsonInput

    def _run(self, company: str, ticker: str, rating: str, final_result: str) -> str:
        as_json = {
            "company": company,
            "ticker": ticker,
            "rating": rating,
            "final_result": final_result
        }
        return str(as_json)