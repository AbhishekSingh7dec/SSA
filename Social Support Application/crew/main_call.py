import os, json
from crew.agents import EligibilityCrew

def main(input):
    # Threshold configuration
    DEFAULT_THRESHOLDS = {
        "income_cap": 25000.0,
        "employment_months_min": 12,
        "family_size_max": 6,
        "wealth_cap": 40000.0,
        "demographic_allowed": ["rural", "urban", "minority", "disabled", "female"]
    }
    
    crew = EligibilityCrew().crew()
    input_data = {
        "raw_text": input,
        **DEFAULT_THRESHOLDS  # Pass thresholds for evaluator
    }
    output = crew.kickoff(inputs=input_data)
    return json.dumps(output.raw['process_application'], indent=2)
