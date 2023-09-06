import enum


class TaskTypes(str, enum.Enum):
    """All types of tasks"""

    HOMEWORK = "Homework"
    QUIZ = "Quiz"
    CLASSTEST = "ClassTest"
    CLASSWORK = "Classwork"
    FLEXIBLETASK = "FlexibleTask"
