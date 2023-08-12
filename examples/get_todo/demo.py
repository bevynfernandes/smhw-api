import smhw_api as api

# Enter your account credentials
AUTH: str = ""
USER_ID: int = 0
SCHOOL_ID: int = 0


def main():
    server = api.Client(AUTH, USER_ID, SCHOOL_ID)
    # Get the user's current task todo list
    # If you wish to get tasks from earlier dates, use the datetime module like so:
    # todo = server.get_todo(start=datetime.datetime.now() - datetime.timedelta(weeks=4))
    # this code ^ fetches tasks starting from 4 weeks ago to 3 weeks ahead (the end parameter's default)
    todo = server.get_todo()

    # All tasks are stored in todo.tasks
    # If you wish to access specific types of tasks, the todo is categorised into 5 different lists:
    # homework, quiz, test, classwork and flexible_task
    for task in todo.tasks:
        print(f"{task.id} | {task.teacher_name}, {task.subject} | {task.completed}")

    # As you might have noticed, the information is very limited. To fetch more information you must use the
    # `get_auto_detailed_task` function
    # This function automatically detects the type of task, fetches the data and returns the appropriate dataclass.
    detailed_task: api.objects.DetailedTask = server.get_auto_detailed_task(
        todo.homework[0]
    )  # Get detailed information about the first homework
    print(
        f"Submission type: {detailed_task.submission_type}\nWeb Links: {detailed_task.web_links}\nClass: {detailed_task.class_group_name}"
    )

    # Tasks like a quiz have much more detailed information such as the questions, etc...


if __name__ == "__main__":
    main()
