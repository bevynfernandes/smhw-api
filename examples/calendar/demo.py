import smhw_api as api

# Enter your account credentials
AUTH: str = ""
USER_ID: int = 0
SCHOOL_ID: int = 0


def main():
    client = api.Client(AUTH, USER_ID, SCHOOL_ID)
    calender = client.get_calendar()  # get the student's personal calender from today
    for (
        ctask
    ) in (
        calender
    ):  # Loop through each calender task in the list and print it's information
        print(
            f"{ctask.id} | Subject: {ctask.subject} | Teacher: {ctask.teacher_name} | Name: {ctask.class_task_title} | Due on: {ctask.due_on}"
        )


def public_calender():
    # The entire school's calender
    # It's the same code as above but with a different client function

    client = api.Client(AUTH, USER_ID, SCHOOL_ID)
    calender = client.get_school_calendar()  # <-- The different client function
    for ctask in calender:
        print(
            f"{ctask.id} | Subject: {ctask.subject} | Teacher: {ctask.teacher_name} | Name: {ctask.title} | Due on: {ctask.due_on}"
        )


if __name__ == "__main__":
    main()
    public_calender()
