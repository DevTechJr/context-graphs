from pydantic import BaseModel, Field

class FinalOutput(BaseModel):
    """Respond to the user in this format."""
    response: str = Field(description="answer the question in 300 tokens")
