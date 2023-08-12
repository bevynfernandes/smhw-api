import smhw_api as api

# Enter your account credentials
AUTH: str = ""
USER_ID: int = 0
SCHOOL_ID: int = 0


def main():
    # Mark a task as complete

    server = api.Client(AUTH, USER_ID, SCHOOL_ID)
    todo = server.get_todo()  # get all current tasks
    task = todo.tasks[0]  # Get the first task

    # Complete the task with that id, second parameter is the state
    # If second param is True, the task will be set as completed, if False it will not be completed.
    server.complete_task(task.id, True)


if __name__ == "__main__":
    main()
