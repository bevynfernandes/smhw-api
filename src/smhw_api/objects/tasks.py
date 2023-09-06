from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from .tools import convert_datetime


@dataclass(slots=True)
class Task:
    """The class Task defines attributes and methods for a task, including due date, completion status,
    task details, and submission information.
    """

    id: int
    user_id: int
    due_on: datetime
    completed: bool
    class_task_id: int
    submission_type: bool
    submission_status: Any
    submission_grade: Any
    class_task_title: str
    class_task_description: str  # only the start (in html)
    class_group_name: str
    class_task_type: str
    subject: str
    teacher_name: str
    issued_on: datetime
    submission_status: bool | None  # not sure what this does
    has_attachments: bool

    def __post_init__(self):
        self.due_on = convert_datetime(self.due_on)
        self.issued_on = convert_datetime(self.issued_on)

    def is_detailed(self) -> bool:
        """Is the task detailed or not?

        This task is not detailed."""
        return False


@dataclass(slots=True)
class DetailedTask(Task):
    """The class "DetailedTask" inherits from "Task" and includes additional attributes such as teacher_id,
    submission_type, attachment_ids, web_links, description, and class_year.

    This class is only used when getting the task data from the Task page API itself and not todo.
    """

    teacher_id: int
    class_group_name: str
    submission_type: str
    attachment_ids: list
    web_links: list
    description: str
    class_year: str
    class_group_name: str

    def is_detailed(self) -> bool:
        """Is the task detailed or not?

        This task is not detailed."""
        return True


@dataclass(slots=True)
class QuizSubmission:
    id: int
    status: str
    student_id: int
    student_name: str
    grade: str
    student_avatar: str
    created_at: datetime
    quiz_id: int
    updated_at: datetime
    question_ids: list[int]
    event_ids: list[int]
    comment_ids: list[int]

    def __post_init__(self):
        self.created_at = convert_datetime(self.created_at)
        self.updated_at = convert_datetime(self.updated_at)


@dataclass(slots=True)
class Question:
    """The class "Question" contains various attributes such as id, correct and incorrect answers, image
    URLs, description, and creation date."""

    id: int
    correct_answer: str
    incorrect_answers: list[str]
    image_upload_id: int  # assuming data types based off name
    image_small_url: str  # assuming data types based off name
    image_xsmall_url: str  # assuming data types based off name
    image_large_url: str  # assuming data types based off name
    image_file_name: str  # assuming data types based off name
    description: str
    created_at: datetime
    position: int


@dataclass(slots=True)
class Quiz(DetailedTask):
    """The Quiz class represents a quiz with various properties and methods, including the ability to
    retrieve a specific question by its ID."""

    completed: bool
    questions_time_limit: int
    random_order: bool
    max_attempts: int
    answered_by_students: bool
    questions: list[Question]
    submission_method_id: int  # which attempt it is
    submission_ids: list[int]
    question_ids: list = field(default_factory=list)

    def get_question(self, question_id: int) -> Question:
        for question in self.questions:
            if question_id == question.id:
                return question


@dataclass(slots=True)
class ClassTest(DetailedTask):
    pass


@dataclass(slots=True)
class FlexibleTask(DetailedTask):
    pass


@dataclass(slots=True)
class Classwork(DetailedTask):
    pass
