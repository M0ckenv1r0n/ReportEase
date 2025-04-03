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
    key: str = Field(description="A placeholder for the paragraph key (title)")
    text: str = Field(description="A placeholder for the paragraph text")

class Report(BaseModel):
    """
    Output schema for the report.

    Attributes:
        Title (str): The title of the report.
        paragraphs (List[Paragraph]): A list of paragraphs, each represented as a dictionary 
            containing 'key' and 'text' entries.
    """
    Title: str = Field(..., description="The title of the report")
    paragraphs: List[Paragraph] = Field([], description="A list of paragraphs with keys and text")

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
            "Create a clear, formal, and well-structured report based on the following input: {input_text}. The report should look official."
        )

        self.section_writer_instructions = (
            "You are a professional technical writer. Your task is to generate a formal, structured, and official-looking report."
            "Format your response as JSON. Include a fixed 'Title' field and additional paragraph sections as separate keys."
            "Your output must follow the given JSON schema."
        )
        logger.info("Initializing ReportAgent with model_choice=%s", LLM_MODEL)
        # self.llm = ChatOpenAI(model=LLM_MODEL, temperature=temperature, **model_kwargs)
        self.llm = ChatOllama(model=LLM_MODEL, temperature=temperature, **model_kwargs)
        self.model_with_structure = self.llm.with_structured_output(Report)

    def generate(self, text: str) -> Dict[str, Any]:
        """Generate a structured report from the given input text."""
        try:
            final_msg = self.human_msg.format(input_text = text)
            result = self.model_with_structure.invoke([
                SystemMessage(content=self.section_writer_instructions),
                HumanMessage(content=final_msg)
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
