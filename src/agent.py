from config import logger, LLM_MODEL
from typing import Any, Dict, List
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

class Paragraph(BaseModel):
    """
    Model representing a single paragraph in the report.

    Attributes:
        key (str): A unique identifier or title for the paragraph.
        text (str): The content of the paragraph.
    """
    key: str = Field("your key placeholder", description="A placeholder for the paragraph key (title)")
    text: str = Field("your text placeholder", description="A placeholder for the paragraph text")

class Report(BaseModel):
    """
    Output schema for the report.

    Attributes:
        Title (str): The title of the report.
        paragraphs (List[Paragraph]): A list of paragraphs, each represented as a dictionary 
            containing 'key' and 'text' entries.
    
    Note:
        Additional fields are allowed in the output due to the 'extra = "allow"' configuration.
    """
    Title: str = Field(..., description="The title of the report")
    paragraphs: List[Paragraph] = Field([], description="A list of paragraphs with keys and text")

    class Config:
        extra = "allow"
def flatten_report(report: Report) -> dict:
    data = report.__dict__

    flat = {"Title": data.get("Title")}
    
    paragraphs = data.get("paragraphs")
    
    for paragraph in paragraphs:
        paragraph_dict= paragraph.__dict__
        key = paragraph_dict.get("key")
        text = paragraph_dict.get("text")
        if key and text:
            flat[key] = text

    return flat

class ReportAgent:
    def __init__(self, temperature: float = 0.0, **model_kwargs: Any) -> None:
        self.human_msg = (
            "Generate a structured report in JSON format with a fixed 'Title' field and additional paragraph keys."
            "Your output must follow the JSON schema provided. Based on the following input: {input_text}"
        )
        self.section_writer_instructions = (
            "You are an expert technical writer. Your task is to create a short, well-structured, and officially looking report."
        )
        logger.info("Initializing ReportAgent with model_choice=%s", LLM_MODEL)
        # self.llm = ChatOpenAI(model=LLM_MODEL, temperature=temperature, **model_kwargs)
        self.llm = ChatOllama(model=LLM_MODEL, temperature=1.0, **model_kwargs)
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

def create_structured_report(text_input: str) -> Dict[str, Any]:
    """Generate a structured report dictionary from input text."""
    try:
        agent = ReportAgent()
        output = agent.generate(text_input)
        return flatten_report(output)
    except Exception as e:
        logger.exception("An error occurred during report generation: %s", e)
        return {}
