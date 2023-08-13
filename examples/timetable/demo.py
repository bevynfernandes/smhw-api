import smhw_api as api

# Enter your account credentials
AUTH: str = ""
USER_ID: int = 0
SCHOOL_ID: int = 0


def main():
    # Some notes:
    # The TimetableInterface object is very confusing, even for me, hopefully I will have the time to redesign it

    client = api.Client(AUTH, USER_ID, SCHOOL_ID)
    timetable = (
        client.get_timetable()
    )  # Get the TimetableInterface object from the start of this week (Monday)
    print(
        timetable.weeks[0].days[0].lessons
    )  # All the lessons for the first day (Monday)
    print(
        timetable.weeks[0].days[1].lessons
    )  # All the lessons for the second day (Tuesday)
    lesson = timetable.weeks[0].days[1].lessons[0]  # The first lesson of the second day
    print(lesson.room, lesson.period, lesson.teacher)


if __name__ == "__main__":
    main()
