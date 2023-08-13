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
    print(quiz.description)  # Print the quiz description
    input("Proceed? ")
    for question in quiz.questions:  # Loop through each question from the quiz
        print(f"Answering question: {question.description}")  # Print the question
        try:
            print(
                client.put_quiz_answer(quiz, question.id, question.correct_answer)
            )  # Send the correct quiz answer with no delay, this may be a bit suspicious though
            #    so the delay= parameter can be used wait X seconds to "answer the question".
        except (
            api.exceptions.QuestionAlreadyComplete
        ) as e:  # If the question already been completed before
            print(e)


if __name__ == "__main__":
    main()
