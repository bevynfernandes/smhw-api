import smhw_api as api

# Enter your account credentials
AUTH: str = ""
USER_ID: int = 0
SCHOOL_ID: int = 0


def main():
    client = api.Client(AUTH, USER_ID, SCHOOL_ID)
    attendance = client.get_detailed_attendance()  # get student's attendance detailed
    print(f"Total Attendance Rate: {attendance.attendance_rate}")
    print(f"Total Authorised Absences: {attendance.authorised_absences_count}")
    print(f"Total Unauthorised Absences: {attendance.unauthorised_absences_count}")
    print(f"Total School Days: {attendance.possible_marks_count}")
    print(f"Total Days In School: {attendance.present_marks_count}")

    print(
        f"Last {len(attendance.last_periods_info)} Periods:"
    )  # whatever was your last / current day of school
    for period in attendance.last_periods_info:
        print(
            f"Class name: {period.name} | Session During: {period.session} | Lasted: {divmod((period.ends_at - period.starts_at).total_seconds(), 60)[0]} minutes"
        )


if __name__ == "__main__":
    main()
