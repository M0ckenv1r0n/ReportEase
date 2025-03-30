from config import logger
from typing import Any, Dict
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

class Report(BaseModel):
    """Output schema for the report. The 'Title' field is fixed; additional keys are allowed."""
    Title: str = Field(..., description="The title of the report")
    
    class Config:
        extra = "allow"

class ReportAgent:
    def __init__(self, model_choice: str = "gpt-4o-mini", temperature: float = 0.0, **model_kwargs: Any) -> None:
        self.human_msg = (
            "Generate a structured report in JSON format with a fixed 'Title' field and additional paragraph keys. "
            "Your output must follow the JSON schema provided. Based on the following input: {input_text}"
        )
        self.section_writer_instructions = (
            "You are an expert technical writer. Your task is to create a short, well-structured, and officially looking report."
        )
        logger.info("Initializing ReportAgent with model_choice=%s", model_choice)
        self.llm = ChatOpenAI(model=model_choice, temperature=temperature, **model_kwargs)
        self.model_with_structure = self.llm.with_structured_output(Report, method="function_calling")

    def generate(self, text: str) -> Dict[str, Any]:
        """Generate a structured report from the given input text."""
        try:
            result = self.model_with_structure.invoke([
                SystemMessage(content=self.section_writer_instructions),
                HumanMessage(content=self.human_msg.format(input_text=text))
            ])
            logger.info("LLM returned structured report: %s", result)
            return result
        except Exception as e:
            logger.exception("Error during report generation: %s", e)
            return {}

def create_structured_report(text_input: str, model_choice: str) -> Dict[str, Any]:
    """Generate a structured report dictionary from input text."""
    try:
        agent = ReportAgent(model_choice=model_choice)
        return agent.generate(text_input).dict()
    except Exception as e:
        logger.exception("An error occurred during report generation: %s", e)
        return {}
