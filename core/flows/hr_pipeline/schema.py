from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class HRPipelineState(BaseModel):
    """Shared state passed between steps of the HR pipeline flow."""

    # Database-mode identifiers.
    # Both are required when running the pipeline from database data.
    candidate_id: Optional[int] = None
    job_position_id: Optional[int] = None

    # Tells us whether the current execution is database mode or raw mode.
    database_mode: bool = False

    # Inputs consumed by the agents.
    candidate_resume: str = ""
    job_title: str = ""
    job_description: str = ""
    required_skills: List[str] = Field(default_factory=list)

    # Outputs produced by the agents.
    screening_output: Dict[str, Any] = Field(default_factory=dict)
    interview_output: Optional[Dict[str, Any]] = None
    final_output: Dict[str, Any] = Field(default_factory=dict)

    # IDs of database rows created in database mode.
    screening_result_id: Optional[int] = None
    interview_question_set_id: Optional[int] = None