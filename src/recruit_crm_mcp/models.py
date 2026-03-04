"""Pydantic models for Recruit CRM API entities."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict


RelatedToType = Literal["candidate", "company", "contact", "job", "deal"]

_JOB_LOCATION_LABELS = {"0": "On-site", "1": "Remote", "2": "Hybrid"}


# ---------------------------------------------------------------------------
# Summary models (read responses)
# ---------------------------------------------------------------------------


class CandidateSummary(BaseModel):
    slug: str | None = None
    name: str = ""
    email: str | None = None
    position: str | None = None
    company: str | None = None
    city: str | None = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> CandidateSummary:
        first = data.get("first_name") or ""
        last = data.get("last_name") or ""
        return cls(
            slug=data.get("slug"),
            name=f"{first} {last}".strip(),
            email=data.get("email"),
            position=data.get("position"),
            company=data.get("current_organization"),
            city=data.get("city"),
        )


class JobSummary(BaseModel):
    slug: str | None = None
    name: str | None = None
    status: str | None = None
    city: str | None = None
    country: str | None = None
    job_type: str | None = None
    job_location_type: str = ""
    minimum_experience: str | None = None
    maximum_experience: str | None = None
    min_annual_salary: str | None = None
    max_annual_salary: str | None = None
    pay_rate: str | None = None
    bill_rate: str | None = None
    job_category: str | None = None
    note_for_candidates: str | None = None
    job_description_file: str | None = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> JobSummary:
        job_status = data.get("job_status")
        status_label = job_status.get("label") if isinstance(job_status, dict) else None

        raw_loc = data.get("job_location_type")
        if raw_loc is None:
            loc_label = ""
        else:
            loc_label = _JOB_LOCATION_LABELS.get(str(raw_loc), str(raw_loc))

        return cls(
            slug=data.get("slug"),
            name=data.get("name"),
            status=status_label,
            city=data.get("city"),
            country=data.get("country"),
            job_type=data.get("job_type"),
            job_location_type=loc_label,
            minimum_experience=data.get("minimum_experience"),
            maximum_experience=data.get("maximum_experience"),
            min_annual_salary=data.get("min_annual_salary"),
            max_annual_salary=data.get("max_annual_salary"),
            pay_rate=data.get("pay_rate"),
            bill_rate=data.get("bill_rate"),
            job_category=data.get("job_category"),
            note_for_candidates=data.get("note_for_candidates"),
            job_description_file=data.get("job_description_file"),
        )


class ContactSummary(BaseModel):
    slug: str | None = None
    name: str = ""
    email: str | None = None
    contact_number: str | None = None
    designation: str | None = None
    company_slug: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    linkedin: str | None = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> ContactSummary:
        first = data.get("first_name") or ""
        last = data.get("last_name") or ""
        return cls(
            slug=data.get("slug"),
            name=f"{first} {last}".strip(),
            email=data.get("email"),
            contact_number=data.get("contact_number"),
            designation=data.get("designation"),
            company_slug=data.get("company_slug"),
            city=data.get("city"),
            state=data.get("state"),
            country=data.get("country"),
            linkedin=data.get("linkedin"),
        )


class CompanySummary(BaseModel):
    slug: str | None = None
    company_name: str | None = None
    about_company: str | None = None
    website: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    linkedin: str | None = None
    industry_id: int | None = None
    is_parent_company: int | None = None
    is_child_company: int | None = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> CompanySummary:
        return cls(
            slug=data.get("slug"),
            company_name=data.get("company_name"),
            about_company=data.get("about_company"),
            website=data.get("website"),
            city=data.get("city"),
            state=data.get("state"),
            country=data.get("country"),
            linkedin=data.get("linkedin"),
            industry_id=data.get("industry_id"),
            is_parent_company=data.get("is_parent_company"),
            is_child_company=data.get("is_child_company"),
        )


class NoteSummary(BaseModel):
    id: int | None = None
    note_type: str | None = None
    description: str | None = None
    related_to: str | None = None
    related_to_type: str | None = None
    created_on: str | None = None
    updated_on: str | None = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> NoteSummary:
        note_type = data.get("note_type")
        type_label = note_type.get("label") if isinstance(note_type, dict) else None
        return cls(
            id=data.get("id"),
            note_type=type_label,
            description=data.get("description"),
            related_to=data.get("related_to"),
            related_to_type=data.get("related_to_type"),
            created_on=data.get("created_on"),
            updated_on=data.get("updated_on"),
        )


class TaskSummary(BaseModel):
    id: int | None = None
    title: str | None = None
    task_type: str | None = None
    status: int | None = None
    start_date: str | None = None
    related_to: str | None = None
    related_to_type: str | None = None
    related_to_name: str | None = None
    owner: int | None = None
    reminder_date: str | None = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> TaskSummary:
        task_type = data.get("task_type")
        type_label = task_type.get("label") if isinstance(task_type, dict) else None
        return cls(
            id=data.get("id"),
            title=data.get("title"),
            task_type=type_label,
            status=data.get("status"),
            start_date=data.get("start_date"),
            related_to=data.get("related_to"),
            related_to_type=data.get("related_to_type"),
            related_to_name=data.get("related_to_name"),
            owner=data.get("owner"),
            reminder_date=data.get("reminder_date"),
        )


class MeetingSummary(BaseModel):
    id: int | None = None
    title: str | None = None
    meeting_type: str | None = None
    status: int | None = None
    start_date: str | None = None
    end_date: str | None = None
    all_day: int | None = None
    address: str | None = None
    related_to: str | None = None
    related_to_type: str | None = None
    owner: int | None = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> MeetingSummary:
        meeting_type = data.get("meeting_type")
        type_label = (
            meeting_type.get("label") if isinstance(meeting_type, dict) else None
        )
        return cls(
            id=data.get("id"),
            title=data.get("title"),
            meeting_type=type_label,
            status=data.get("status"),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            all_day=data.get("all_day"),
            address=data.get("address"),
            related_to=data.get("related_to"),
            related_to_type=data.get("related_to_type"),
            owner=data.get("owner"),
        )


class UserSummary(BaseModel):
    id: int | None = None
    name: str = ""
    email: str | None = None
    role: str | None = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> UserSummary:
        first = data.get("first_name") or ""
        last = data.get("last_name") or ""
        return cls(
            id=data.get("id"),
            name=f"{first} {last}".strip(),
            email=data.get("email"),
            role=data.get("role"),
        )


class AssignedCandidateSummary(CandidateSummary):
    hiring_status: str | None = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> AssignedCandidateSummary:
        candidate = data.get("candidate") or {}
        first = candidate.get("first_name") or ""
        last = candidate.get("last_name") or ""
        status = data.get("status") or {}
        return cls(
            slug=candidate.get("slug"),
            name=f"{first} {last}".strip(),
            email=candidate.get("email"),
            position=candidate.get("position"),
            company=candidate.get("current_organization"),
            city=candidate.get("city"),
            hiring_status=status.get("label") if isinstance(status, dict) else None,
        )


# ---------------------------------------------------------------------------
# Input models (for write operations)
# ---------------------------------------------------------------------------


class CustomField(BaseModel):
    model_config = ConfigDict(extra="forbid")

    field_id: int
    value: str


class NoteCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    description: str
    related_to: str
    related_to_type: RelatedToType
    note_type_id: int | None = None
    associated_candidate: str | None = None
    associated_company: str | None = None
    associated_contact: str | None = None
    associated_job: str | None = None
    associated_deal: str | None = None
    created_by: int | None = None


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    reminder: int
    start_date: str
    description: str | None = None
    task_type_id: int | None = None
    related_to: str | None = None
    related_to_type: RelatedToType | None = None
    associated_candidate: str | None = None
    associated_company: str | None = None
    associated_contact: str | None = None
    associated_job: str | None = None
    associated_deal: str | None = None
    owner_id: int | None = None


class MeetingCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    reminder: int
    start_date: str
    end_date: str
    description: str | None = None
    meeting_type_id: int | None = None
    address: str | None = None
    related_to: str | None = None
    related_to_type: RelatedToType | None = None
    attendee_candidate: str | None = None
    attendee_company: str | None = None
    attendee_contact: str | None = None
    associated_candidate: str | None = None
    associated_company: str | None = None
    associated_contact: str | None = None
    associated_job: str | None = None
    associated_deal: str | None = None
    owner_id: int | None = None


class CandidateCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    first_name: str
    last_name: str | None = None
    email: str | None = None
    position: str | None = None
    contact_number: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    linkedin: str | None = None
    current_organization: str | None = None
    skill: str | None = None
    source: str | None = None
    candidate_summary: str | None = None
    owner_id: int | None = None
    custom_fields: list[CustomField] | None = None


class ContactCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    first_name: str
    last_name: str
    email: str | None = None
    contact_number: str | None = None
    designation: str | None = None
    company_slug: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    linkedin: str | None = None
    stage_id: int | None = None
    owner_id: int | None = None
    custom_fields: list[CustomField] | None = None


class CompanyCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    company_name: str
    about_company: str | None = None
    website: str | None = None
    industry_id: int | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    linkedin: str | None = None
    owner_id: int | None = None
    custom_fields: list[CustomField] | None = None
