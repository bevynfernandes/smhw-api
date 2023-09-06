from dataclasses import dataclass, field

from .tasks import Task
from .types import TaskTypes
from .tools import Create

from loguru import logger


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
