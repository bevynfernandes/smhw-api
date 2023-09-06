from dataclasses import dataclass


@dataclass(slots=True)
class BaseSubject:
    """The class BaseSubject has two attributes, id and name."""

    id: int
    name: str


@dataclass(slots=True)
class Subject(BaseSubject):
    """The Subject class inherits from the BaseSubject class and has two integer attributes,
    school_private_info_id and standard_subject_id.
    """

    school_private_info_id: int
    standard_subject_id: int


@dataclass(slots=True)
class Class(BaseSubject):
    """This is a class that represents a group of students and teachers for a specific subject in a school,
    with additional attributes such as class year, academic year ID, and group type.
    """

    class_year: str
    academic_year_id: int
    school_id: int
    is_registration_group: bool
    student_ids: list[int]
    teacher_ids: list[int]
    left_at: str
    group_type: str
    subject: str
