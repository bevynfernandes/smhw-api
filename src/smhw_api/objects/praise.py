from dataclasses import dataclass, field
from datetime import datetime

from .tools import convert_datetime


@dataclass(slots=True)
class Praise:
    """The class "Praise" contains attributes related to a kudos event, including the staff member
    involved, the reason for the kudos, and the date it occurred."""

    id: int
    points: int
    academic_year_id: int
    staff_member_id: int
    kudos_reason_id: int
    description: str
    kudos_event_id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime
    staff_member_title: str
    staff_member_forename: str
    staff_member_surname: str
    comments: str
    positive: bool
    source_id: str
    happened_on: str
    serious_incident: bool
    full_name: str = field(default_factory=str, init=False)

    def __post_init__(self):
        self.created_at = convert_datetime(self.created_at)
        self.updated_at = convert_datetime(self.updated_at)
        self.deleted_at = convert_datetime(self.deleted_at)
        self.full_name: str = f"{self.staff_member_title}. {self.staff_member_forename} {self.staff_member_surname}"


@dataclass(slots=True)
class PraiseSummary:
    """The class "PraiseSummary" contains attributes related to positive and negative feedback counts for a
    student, including totals, monthly, weekly, and daily counts."""

    id: int
    student_id: int
    total_positive_count: int
    total_negative_count: int
    total_count: int
    month_positive_count: int
    month_negative_count: int
    month_count: int
    week_positive_count: int
    week_negative_count: int
    week_count: int
    day_count: int
    day_positive_count: int
    day_negative_count: int


@dataclass(slots=True)
class Behaviour:
    """The class "Behaviour" contains lists of student praises and badges, as well as a summary of student
    praises."""

    student_praises: list[Praise]
    student_badges: list
    student_praise_summary: PraiseSummary
