from datetime import datetime

from pydantic import BaseModel, Field


class PatientCreate(BaseModel):
    display_name: str = Field(min_length=1, max_length=120)


class PatientOut(BaseModel):
    id: str
    display_name: str
    created_at: datetime

    model_config = {"from_attributes": True}


class VisitCreate(BaseModel):
    patient_id: str
    notes: str = Field(min_length=1, max_length=10000)


class VisitOut(BaseModel):
    id: str
    patient_id: str
    notes: str
    ai_summary: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
