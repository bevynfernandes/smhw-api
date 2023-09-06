from dataclasses import dataclass
from datetime import datetime
from typing import Any

from .tools import AM_OR_PM, convert_datetime


@dataclass(slots=True)
class AttendanceInsight:
    attendance_rate: float
    unauthorised_absences_count: int


@dataclass(slots=True)
class PunctualityInsight:
    punctuality_rate: float
    late_before_registration_count: int


@dataclass(slots=True)
class StudentInsight:
    id: int
    attendance: AttendanceInsight
    punctuality: PunctualityInsight


@dataclass(slots=True)
class DetailedAttendancePeriod:
    id: int
    name: str
    session: AM_OR_PM
    starts_at: datetime
    ends_at: datetime
    source_id: str
    school_id: int

    def __post_init__(self):
        self.starts_at = convert_datetime(self.starts_at)
        self.ends_at = convert_datetime(self.ends_at)


@dataclass(slots=True)
class DetailedAttendance:
    id: int
    student_name: str
    student_avatar: str
    student_category_ids: list[int]
    year_name: str
    registration_group_name: str
    attendance_rate: float
    possible_marks_count: int
    present_marks_count: int
    authorised_absences_count: int
    unauthorised_absences_count: int
    late_after_registration_count: int
    missing_marks_count: int
    session_marks: Any
    registers_info: list[Any]
    starts_on: Any
    ends_on: Any
    last_periods_info: list[DetailedAttendancePeriod]
    last_absences_info: list[Any]
    attendance_codes: list[Any]


@dataclass(slots=True)
class Detentions:
    """TBD"""  # TODO

    detentions: list[Any]
    selection_count: int
