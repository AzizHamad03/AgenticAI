from typing import Dict, Optional

from pydantic import BaseModel


class HRPipelineState(BaseModel):
    """Shared state passed between steps of the HR pipeline flow."""

    # Inputs
    candidate_resume: str = ""
    job_title: str = ""
    job_description: str = ""
    required_skills: str = ""

    # Outputs
    screening_output: Dict = {}
    interview_output: Optional[Dict] = None
    final_output: Dict = {}