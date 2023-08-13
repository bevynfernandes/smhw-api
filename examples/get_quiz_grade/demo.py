import smhw_api as api

# Enter your account credentials
AUTH: str = ""
USER_ID: int = 0
SCHOOL_ID: int = 0


def main():
    client = api.Client(AUTH, USER_ID, SCHOOL_ID)
    todo = (
        client.get_todo()
    )  # get all the tasks from the todo (current date to 3 weeks ahead,)
    quiz = client.get_auto_detailed_task(
        todo.quiz[0]
    )  # Get the first available quiz from the todo and get its detailed information (see the get_todo demo for more information)
    quiz_submission = client.get_quiz_submission(
        quiz
    )  # get the student's quiz submission data, passing the quiz as a param
    print(
        f"{quiz_submission.student_name} | Grade: {quiz_submission.grade} | Status: {quiz_submission.status}"
    )  # Print the student's name, quiz grade and the status of the quiz.


if __name__ == "__main__":
    main()
