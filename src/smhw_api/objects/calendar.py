from dataclasses import dataclass
from datetime import datetime

from .tools import convert_datetime


@dataclass(slots=True)
class BaseCalendarTask:
    id: int
    due_on: datetime
    issued_on: datetime
    subject: str
    teacher_id: int
    teacher_name: str
    class_task_type: str

    def __post_init__(self):
        self.due_on = convert_datetime(self.due_on)
        self.issued_on = convert_datetime(self.issued_on)


@dataclass(slots=True)
class PersonalCalendarTask(BaseCalendarTask):
    id: int
    class_task_id: int
    class_group_name: str
    class_task_title: str
    submissions_count: int
    for_partial_group: bool


@dataclass(slots=True)
class SchoolCalendarTask(BaseCalendarTask):
    id: int
    due_on: datetime
    issued_on: datetime
    subject: str
    teacher_id: int
    teacher_name: str
    class_task_type: str
    title: str
    year: str
