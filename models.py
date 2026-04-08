from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field


class IssueObservation(BaseModel):
    issue_id: int = Field(..., description="Unique identifier for the issue.")
    title: str = Field(..., description="Issue title.")
    body: str = Field(..., description="Issue body.")


class AgentAction(BaseModel):
    action_type: Literal["AddLabel", "RequestMoreInfo"] = Field(
        ...,
        description="Triage action type.",
    )
    label: Optional[str] = Field(
        default=None,
        description="Label for AddLabel action (bug|enhancement).",
    )
    comment: Optional[str] = Field(
        default=None,
        description="Optional comment text.",
    )
