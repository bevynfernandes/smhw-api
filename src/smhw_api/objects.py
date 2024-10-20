"""
If a variable has the type `Any`, this means that I haven't be able to check what the type is.
If you know, make a pull request or an issue.
"""

import enum
from dataclasses import dataclass, field, fields
from datetime import datetime
from typing import Any, Literal

from loguru import logger

# Custom Types
AM_OR_PM = Literal["am", "pm"]


def convert_datetime(var: str | datetime) -> datetime:
    """
    This function converts a string or datetime object to a datetime object.

    Args:
        var (str | datetime): The parameter `var` can be either a string or a `datetime` object.

    Returns:
        The function `convert_datetime` takes a variable `var` which can be either a string or a datetime
    object and returns a datetime object. If `var` is already a datetime object, it is returned as is.
    Otherwise, it is assumed to be a string in ISO format and converted to a datetime object using the
    `fromisoformat` method.
    """
    if isinstance(var, datetime) or not isinstance(var, str):
        return var
    else:
        return datetime.fromisoformat(var)


class Create:
    classFieldCache = {}

    @classmethod
    def instantiate(cls, classToInstantiate: object, argDict: dict):
        """
        The function takes in a class and a dictionary of arguments, filters the arguments based on the
        class's fields, and returns an instance of the class with the filtered arguments.

        Args:
            classToInstantiate (object): The class object that needs to be instantiated.
            argDict (dict): argDict is a dictionary that contains the arguments to be passed to the
        constructor of the class that is being instantiated. The keys of the dictionary represent the names
        of the arguments, and the values represent the values to be passed for those arguments.

        Returns:
            An instance of the class specified in the `classToInstantiate` parameter, with the arguments
        specified in the `argDict` parameter. The function first checks if the class has already been cached
        in `classFieldCache`, and if not, it caches the fields of the class that can be initialized. It then
        filters the arguments in `argDict` to only include those that correspond to the class fields.
        """
        if classToInstantiate not in cls.classFieldCache:
            cls.classFieldCache[classToInstantiate] = {
                f.name for f in fields(classToInstantiate) if f.init
            }

        fieldSet = cls.classFieldCache[classToInstantiate]
        filteredArgDict = {k: v for k, v in argDict.items() if k in fieldSet}

        # Autofill missing fields to None
        for field in fieldSet:
            if field not in filteredArgDict:
                filteredArgDict[field] = None

        return classToInstantiate(**filteredArgDict)


class TaskTypes(str, enum.Enum):
    """All types of tasks"""

    HOMEWORK = "Homework"
    QUIZ = "Quiz"
    CLASSTEST = "ClassTest"
    CLASSWORK = "Classwork"
    FLEXIBLETASK = "FlexibleTask"


@dataclass(slots=True)
class BearerUser:
    """The class BearerUser has attributes related to user information and activity, and uses a
    post-initialization method to convert datetime objects.
    """

    id: int
    email: str
    last_activity_at: datetime
    username: str
    calendar_token: str
    uid: str
    last_user_activity_at: datetime

    def __post_init__(self):
        self.last_activity_at = convert_datetime(self.last_activity_at)
        self.last_user_activity_at = convert_datetime(self.last_user_activity_at)


@dataclass(slots=True)
class CommentUser:
    id: int
    title: str
    backend_type: str
    forename: str
    surname: str
    avatar: str

    full_name: str = field(default_factory=str, init=False)

    def __post_init__(self):
        self.full_name: str = f"{self.title}. {self.forename} {self.surname}"


@dataclass(slots=True)
class CommentableTask:
    id: int
    type: str


@dataclass(slots=True)
class Comment:
    id: int
    message: str
    created_at: datetime
    commentable: CommentableTask
    user_id: int
    attachment_ids: list[int]


@dataclass(slots=True)
class Comments:
    users: list[CommentUser]
    comments: list[Comment]


@dataclass(slots=True)
class User:
    """The class defines a User object with various attributes and methods, including a full name attribute
    that is automatically generated based on the user's title, forename, and surname.
    """

    id: int
    avatar: str
    forename: str
    school_id: int
    surname: str
    created_at: datetime
    backend_type: str
    updated_at: datetime
    title: str
    user_private_info_id: int
    user_identity_id: int

    disabled: bool = field(default_factory=bool, init=False)
    full_name: str = field(default_factory=str, init=False)

    def __post_init__(self):
        self.created_at = convert_datetime(self.created_at)
        self.updated_at = convert_datetime(self.updated_at)
        self.full_name: str = f"{self.title}. {self.forename} {self.surname}"


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


@dataclass(slots=True)
class Auth:
    smhw_token: str
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
    created_at: int
    user_id: int
    school_id: int
    user_type: str
    account_switch_enabled: bool


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


@dataclass(slots=True)
class _SchoolPremiumFeatures:
    welfare_notes: bool
    white_label_enabled: bool
    custom_theme_enabled: bool
    collins_content: bool
    sanctions: bool
    on_call_enabled: bool


@dataclass(slots=True)
class _CollinsSettings:
    public_calendar_advert: bool
    teacher_class_task_advert: bool
    parent_class_task_advert: bool
    student_class_task_advert: bool


@dataclass(slots=True)
class PublicSchool:
    "Used for when searching for schools."
    id: int
    name: str
    address: str
    town: str
    post_code: str
    subdomain: str
    is_active: bool
    brand_color: str | None


@dataclass(slots=True)
class School:
    """The class "School" contains attributes related to a school, such as its ID, name, address, and
    employee and student IDs, as well as a list of subjects and a boolean indicating whether the school
    has praise points enabled.
    """

    id: int
    name: str
    subdomain: str
    address: str
    town: str
    post_code: str
    country: str
    phone_number: Any
    email: str
    website: str
    twitter: str
    facebook: str
    instagram: str
    school_phase_name: str
    latitude: int
    longitude: int
    created_at: datetime
    updated_at: datetime
    logo_url: str
    logo_name: str
    premium_features: _SchoolPremiumFeatures
    prospectus_url: str
    prospectus_name: str
    homepage_background_image_name: str
    homepage_background_image_url: str
    homepage_zones: bool
    homepage_active: bool
    homepage_background: str
    student_zone_root_id: int
    school_zone_root_id: int
    parent_zone_root_id: int
    links: dict  # may be used?
    employee_ids: list[int]
    collins_settings: _CollinsSettings
    brand_color: str
    only_positive_kudos_enabled: bool
    is_discussion_enabled: bool
    share_classroom_enabled: bool
    share_task_to_teams_enabled: bool
    domains_for_email_import: str
    domain = str  # domains_for_email_import
    school_private_info_id: int
    time_zone: str
    registration_group_ids: list[int]
    has_o365_integration: bool
    active_directory_enabled: bool
    google_enabled: bool
    google_drive_uploads_disabled: bool
    dropbox_uploads_disabled: bool
    one_drive_uploads_disabled: bool
    hide_session_marks: bool
    hide_lesson_marks: bool
    satchel_classes_homework_ad: bool
    root_directory_id: int
    school_praise_info_id: int
    is_active: bool
    import_external_type: str
    imports_enabled: bool
    attendance_settings_id: int
    class_group_ids: list[int]
    seating_label_ids: list[int]
    import_photos_type: str
    early_access_enabled: bool
    account_switch_enabled: bool
    praise_points: bool  # if school has praise_points enabled
    kudos: bool
    kudos_import: bool
    kudos_writeback: bool
    smart_seating: bool
    core: bool
    homework: bool
    timetables: bool
    attendance: bool
    attendance_import_sessions: bool
    attendance_writeback_sessions: bool
    attendance_import_lessons: bool
    attendance_writeback_lessons: bool
    assessment: bool
    detentions: bool
    detentions_writeback: bool
    documents: bool
    xod_documents: bool
    address_scope_consented: bool
    show_staff_codes_for_public: bool
    referred_incidents_enabled: bool
    partners_page_enabled: bool
    sanction_rule_ids: list[int]
    classroom_emails_scope_enabled: bool
    student_ids: list[int]
    parent_ids: list[int]
    pulse_promo: bool
    announcement_category_ids: list[int]
    subjects: list[Subject]
    notice_types_enabled: bool = field(default_factory=bool)

    def __post_init__(self):
        self.created_at = convert_datetime(self.created_at)
        self.updated_at = convert_datetime(self.updated_at)


@dataclass(slots=True)
class PublicSchoolSearch:
    schools: list[PublicSchool]
    selection_count: int
    offset: int


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
class NotificationNotice:
    id: int
    title: str
    message: str


@dataclass(slots=True)
class Notification:
    id: int
    user_id: Any
    recipient_id: int
    read: bool
    event_type: str
    student_id: int
    created_at: datetime
    updated_at: datetime
    user_name: str
    eventable_type: str
    assignment_id: Any
    assignment_type: Any
    submission_id: Any
    parent_forename: Any
    parent_surname: Any
    student_forename: str
    truancy_count: Any
    notice: NotificationNotice | None = None

    def __post_init__(self):
        self.created_at = convert_datetime(self.created_at)
        self.updated_at = convert_datetime(self.updated_at)


@dataclass(slots=True)
class Notifications:
    events: list[Notification]
    selection_count: int


@dataclass(slots=True)
class Parent(User):
    """The class "Parent" inherits from the class "User" and includes attributes for student IDs, student
    names, and parent consent.
    """

    student_ids: list[int]
    student_names: list[str]
    parent_consent: bool


@dataclass(slots=True)
class SearchedTask:
    """The class Task defines attributes and methods for a task, including due date, completion status,
    task details, and submission information. (Contains less infomation than a normal `Task`)
    """

    id: int
    due_on: datetime
    submission_type: bool
    submission_status: Any
    class_group_name: str
    subject: str
    teacher_name: str
    submission_status: bool | None

    def __post_init__(self):
        self.due_on = convert_datetime(self.due_on)

    def is_detailed(self) -> bool:
        """Is the task detailed or not?

        This task is not detailed."""
        return False


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
    submission_status: bool | None
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


@dataclass(slots=True)
class TaskSearchResult:
    id: int
    status: Any
    student_id: int
    student_name: str
    student_name_sims_format: str
    grade: Any
    student_avatar: str
    completed: bool
    overdue: bool
    marked: bool
    handed_in_on: Any
    grade_sent: bool
    created_at: datetime
    updated_at: datetime
    event_ids: list[Any]
    comment_ids: list[Any]
    version_ids: list[Any]
    homework_id: int = None
    flexible_task_id: int = None
    # Just guessing the names
    quiz_task_id: int = None
    class_test_task_id: int = None
    classwork_task_id: int = None
    grading_comment: Any = field(default_factory=lambda: None)

    def __post_init__(self):
        self.created_at = convert_datetime(self.created_at)
        self.updated_at = convert_datetime(self.updated_at)


@dataclass(slots=True)
class TaskSearchResults:
    homework_submissions: list[TaskSearchResult] = None
    quiz_submissions: list[TaskSearchResult] = None
    spelling_test_submissions: list[TaskSearchResult] = None
    class_test_submissions: list[TaskSearchResult] = None
    flexible_task_submissions: list[TaskSearchResult] = None
    classwork_submissions: list[TaskSearchResult] = None
    selection_count: int = 0


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
        self.full_name: str = (
            f"{self.staff_member_title}. {self.staff_member_forename} {self.staff_member_surname}"
        )


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
    detentions: list[Any] = field(default_factory=list)

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


@dataclass(slots=True)
class Todo:
    """The Todo class contains all tasks and categorizes tasks into different types such as homework, quiz, test, classwork, and
    flexible tasks."""

    tasks: list[Task] = field(default_factory=list)
    homework: list[Task] = field(default_factory=list)
    quiz: list[Task] = field(default_factory=list)
    test: list[Task] = field(default_factory=list)
    classwork: list[Task] = field(default_factory=list)
    flexible_task: list[Task] = field(default_factory=list)

    def categorize(self):
        """
        This function categorizes tasks based on their type and appends them to their respective lists.

        (This should not be run more than once as it may cause the catagories to have duplicate tasks!)
        """
        for task in self.tasks:
            if task.class_task_type == TaskTypes.HOMEWORK:
                self.homework.append(task)
            elif task.class_task_type == TaskTypes.QUIZ:
                self.quiz.append(task)
            elif task.class_task_type == TaskTypes.CLASSTEST:
                self.test.append(task)
            elif task.class_task_type == TaskTypes.CLASSWORK:
                self.classwork.append(task)
            elif task.class_task_type == TaskTypes.FLEXIBLETASK:
                self.flexible_task.append(task)
            else:
                logger.info(f"Task could not be categorized! ({task.class_task_type})")


def make_todo(raw_tasks: list[dict]) -> Todo:
    """
    The function takes a list of dictionaries representing tasks, creates Task objects from them, adds
    them to a Todo object, categorizes the tasks, and returns the Todo object.

    Args:
        raw_tasks (list[dict]): A list of dictionaries representing raw task data. Each dictionary should
    contain information about a single task, such as its title, description, due date, and priority
    level.

    Returns:
        The function `make_todo` is returning an instance of the `Todo` class.
    """
    td = Todo()
    for task in raw_tasks:
        td.tasks.append(Create.instantiate(Task, task))
    td.categorize()
    return td
