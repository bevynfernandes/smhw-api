import smhw_api as api

# Enter your account credentials
AUTH: str = ""
USER_ID: int = 0
SCHOOL_ID: int = 0


def main():
    server = api.Server(AUTH, USER_ID, SCHOOL_ID)
    behaviour = (
        server.get_behaviour()
    )  # Get the last 20 (limit default) behaviour points (positive and negative)
    for (
        praise
    ) in (
        behaviour.student_praises
    ):  # loop through each behaviour point (positive and negative)
        print(
            f"Positive: {praise.positive} | Points: {praise.points} | Reason: {praise.description} | Comments: {praise.comments} | Teacher: {praise.full_name}"
        )


if __name__ == "__main__":
    main()
