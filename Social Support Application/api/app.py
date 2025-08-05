
### incomplete


from fastapi import FastAPI
from typing import List
from pydantic import BaseModel
from crew.main_call import main

app = FastAPI()

# Define the application data model for incoming requests
class ApplicationData(BaseModel):
    income: float
    family_size: int
    address: str
    employment_status: str
    credit_score: int
    assets_to_liabilities_ratio: float
    documents: List[str]  # List of document paths (Emirates ID, bank statement, etc.)

@app.post("/process_application/")
async def process_application(data: ApplicationData):
    """
    Process the application data through extraction, validation, eligibility assessment, and recommendations.

    Args:
        data (ApplicationData): The applicant's data to process.

    Returns:
        dict: Processed status and details of the results.
    """
    
    # Convert incoming data to dictionary format for agents
    application_data = data
    

    # Orchestrate agents using CrewAI

    # Process the inputs using the crew agents
    inputs = {
        "validated_data": application_data  # In a real case, this would be data from extraction and validation
    }
    
    # Run the agents and get the result
    result = main.run(inputs)

    # Return the result of the processing
    return {"status": "Processed", "result": result}
