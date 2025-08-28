from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class CandidateCreate(BaseModel):
    full_name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    experience_years: Optional[float] = None
    skills: Optional[str] = None
    notice_period_days: Optional[int] = None
    expected_salary: Optional[float] = None
    current_salary: Optional[float] = None
    resume_url: Optional[str] = None
    linkedin_url: Optional[str] = None


class CandidateOut(BaseModel):
    id: int
    full_name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    experience_years: Optional[float] = None
    skills: Optional[str] = None
    notice_period_days: Optional[int] = None
    expected_salary: Optional[float] = None
    current_salary: Optional[float] = None
    resume_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RequirementCreate(BaseModel):
    title: str
    client_name: Optional[str] = None
    location: Optional[str] = None
    min_experience: Optional[float] = None
    max_experience: Optional[float] = None
    skills_required: Optional[str] = None
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    job_type: Optional[str] = None
    description: Optional[str] = None


class RequirementOut(BaseModel):
    id: int
    title: str
    client_name: Optional[str] = None
    location: Optional[str] = None
    min_experience: Optional[float] = None
    max_experience: Optional[float] = None
    skills_required: Optional[str] = None
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    job_type: Optional[str] = None
    description: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ApplicationCreate(BaseModel):
    candidate_id: int
    requirement_id: int
    source: Optional[str] = None


class ApplicationOut(BaseModel):
    id: int
    candidate_id: int
    requirement_id: int
    stage: str
    source: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class InteractionCreate(BaseModel):
    candidate_id: int
    channel: str
    direction: Optional[str] = "outbound"
    content: Optional[str] = None
    metadata: Optional[dict] = None


class InteractionOut(BaseModel):
    id: int
    candidate_id: int
    channel: str
    direction: str
    content: Optional[str] = None
    metadata: Optional[dict] = Field(default=None, validation_alias="metadata_")
    created_at: datetime

    class Config:
        from_attributes = True


class ScreeningQuestionCreate(BaseModel):
    requirement_id: int
    text: str
    category: Optional[str] = None


class ScreeningQuestionOut(BaseModel):
    id: int
    requirement_id: int
    text: str
    category: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ScreeningResponseCreate(BaseModel):
    candidate_id: int
    requirement_id: int
    question_id: int
    answer_text: str
    score: Optional[float] = None


class ConfirmationCreate(BaseModel):
    application_id: int
    rate_or_salary: Optional[float] = None
    contract_duration: Optional[str] = None
    email_confirmed: Optional[bool] = False
    notes: Optional[str] = None


class ConfirmationOut(BaseModel):
    id: int
    application_id: int
    rate_or_salary: Optional[float] = None
    contract_duration: Optional[str] = None
    email_confirmed: bool
    notes: Optional[str] = None
    confirmed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SubmissionCreate(BaseModel):
    application_id: int
    notes: Optional[str] = None


class SubmissionOut(BaseModel):
    id: int
    application_id: int
    submitted_at: datetime
    status: str
    notes: Optional[str] = None

    class Config:
        from_attributes = True


class FeedbackCreate(BaseModel):
    candidate_id: int
    requirement_id: Optional[int] = None
    application_id: Optional[int] = None
    stage: Optional[str] = None
    rating: Optional[float] = None
    comments: Optional[str] = None


class FeedbackOut(BaseModel):
    id: int
    candidate_id: int
    requirement_id: Optional[int] = None
    application_id: Optional[int] = None
    stage: Optional[str] = None
    rating: Optional[float] = None
    comments: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class SourcingQuery(BaseModel):
    title: Optional[str] = None
    location: Optional[str] = None
    min_experience: Optional[float] = None
    max_experience: Optional[float] = None
    skills_required: Optional[str] = None
    limit: Optional[int] = 20
    providers: Optional[list[str]] = None  # ["linkedin", "naukri"]


class SourcedCandidate(BaseModel):
    full_name: str
    headline: Optional[str] = None
    location: Optional[str] = None
    skills: Optional[list[str]] = None
    source: str
    profile_url: Optional[str] = None
    score: Optional[float] = None



