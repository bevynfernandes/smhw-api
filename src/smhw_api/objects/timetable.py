from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from .subjects import BaseSubject
from .tools import convert_datetime


@dataclass(slots=True)
class TimetableClassGroup(BaseSubject):
    subject: str


@dataclass(slots=True)
class TimetablePeriod:
    startDateTime: datetime
    endDateTime: datetime
    utcStartTime: datetime
    utcEndTime: datetime
    session: str

    def __post_init__(self):
        self.startDateTime = convert_datetime(self.startDateTime)
        self.endDateTime = convert_datetime(self.endDateTime)
        self.utcStartTime = convert_datetime(self.utcStartTime)
        self.utcEndTime = convert_datetime(self.utcEndTime)


@dataclass(slots=True)
class TimetableHomework:
    id: int
    title: str
    type: str


@dataclass(slots=True)
class TimetableTeacher:
    title: str
    forename: str
    surname: str

    full_name: str = field(default_factory=str, init=False)

    def __post_init__(self):
        self.full_name: str = f"{self.title}. {self.forename} {self.surname}"


@dataclass(slots=True)
class TimetableLesson:
    id: int
    url: str
    classGroup: TimetableClassGroup
    period: TimetablePeriod
    room: str
    teacher: TimetableTeacher
    dueClassTasks: list[TimetableHomework]


@dataclass(slots=True)
class TimetableDay:
    order: int
    date: datetime
    lessons: list[TimetableLesson]
    registration_group: str
    detentions: list[Any]

    def __post_init__(self):
        self.date = datetime.strptime(self.date, "%Y-%m-%d")


@dataclass(slots=True)
class Timetable:
    order: int
    startDate: datetime
    prevWeekStartDate: datetime
    days: list[TimetableDay]

    def __post_init__(self):
        self.startDate = datetime.strptime(self.startDate, "%Y-%m-%d")
        self.prevWeekStartDate = datetime.strptime(self.prevWeekStartDate, "%Y-%m-%d")


@dataclass(slots=True)
class TimetableInterface:
    numWeeks: int
    earliestRequestDate: datetime
    latestRequestDate: datetime
    requestDate: datetime
    firstDayOfWeekDate: datetime
    weeks: list[Timetable]

    def __post_init__(self):
        self.earliestRequestDate = datetime.strptime(
            self.earliestRequestDate, "%Y-%m-%d"
        )
        self.latestRequestDate = datetime.strptime(self.latestRequestDate, "%Y-%m-%d")
        self.requestDate = datetime.strptime(self.requestDate, "%Y-%m-%d")
        self.firstDayOfWeekDate = datetime.strptime(self.firstDayOfWeekDate, "%Y-%m-%d")
