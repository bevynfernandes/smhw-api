from dataclasses import dataclass
from datetime import datetime

from .user import User
from .subjects import Class


@dataclass(slots=True)
class Student(User):
    """The class "Student" contains attributes and methods related to a student user in a system, including
    their parent IDs, year, gender, class group IDs, activity timestamps, calendar token, enrolled
    classes, and invite code.
    """

    username: str
    mobile_device_id: int
    total_storage_used: int
    root_folder_id: int
    uid: str
    has_filled_details: bool
    intercom_enabled: bool
    left_at: bool
    sims_id: str
    anonymous: bool
    disabled: bool
    created_at: datetime
    parent_ids: list[int]
    year: str
    gender: str
    class_group_ids: list[int]
    last_activity_at: datetime
    last_user_activity_at: datetime
    calendar_token: str
    classes: list[Class]
    invite_code: str


@dataclass(slots=True)
class Employee(User):
    pass


@dataclass(slots=True)
class Parent(User):
    """The class "Parent" inherits from the class "User" and includes attributes for student IDs, student
    names, and parent consent.
    """

    student_ids: list[int]
    student_names: list[str]
    parent_consent: bool
