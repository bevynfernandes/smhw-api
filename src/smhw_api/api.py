import datetime
import time
from dataclasses import asdict

import httpx
from loguru import logger

from smhw_api import exceptions, objects


class Client:
    """The Client class provides methods for interacting with the SatchelOne API to retrieve information about a student's tasks, classes, school, and more."""

    session = httpx.Client(http2=True)
    base_headers = {
        "Accept": "application/smhw.v2021.5+json",
        "Connection": "keep-alive",
    }
    current_client = "web"
    clients = {
        "web": {
            "client_id": "55283c8c45d97ffd88eb9f87e13f390675c75d22b4f2085f43b0d7355c1f",
            "client_secret": "c8f7d8fcd0746adc50278bc89ed6f004402acbbf4335d3cb12d6ac6497d3",
        },
        "android": {
            "client_id": "a44486a71714841f51744b66582427f2c094e48675b40530341d470c26d63bbd",
            "client_secret": "243a91065893d1e701d7f5d4ddf6d564a0e0559dfe872e6e6dfba849440af81d",
        },
    }
    api_url = "https://api.satchelone.com/api"

    def __init__(self, auth: str, user_id: int, school_id: int):
        """
        This is a constructor function that initializes various attributes including session, auth, user_id,
        school_id, and headers.

        Args:
            auth (str): The authentication token used to access the API. It is required to start with the
        string "Bearer ".
            user_id (int): The user ID is an integer that identifies a specific user in the system. It is
        likely used to retrieve or manipulate data related to that user.
            school_id (int): The school ID is an integer that identifies a specific school within the system.
        It is used to retrieve data specific to that school.
        """
        if auth[:7] != "Bearer ":
            raise exceptions.InvalidAuth(
                "Auth needs to start with 'Bearer' (with capitalization)."
            )

        self.auth = auth
        self.user_id = user_id
        self.school_id = school_id
        self._data: dict[objects.School, objects.Student] = {}

        self.headers = {
            "Authorization": self.auth,
        } | self.base_headers

        logger.debug("Obtaining information via self._get_data...")
        self._get_data()

    def _get_request(self, url, *args, **kwargs) -> httpx.Response:
        """
        This function sends an HTTP GET request to the specified URL with the custom headers and returns
        the response.

        Args:
            url: The URL of the HTTP request that the function will send a GET request to.

        Returns:
            A HTTP response object of the type `httpx.Response`.
        """
        logger.debug(f"[GET] request: {url=}, {kwargs}")
        return self.session.get(
            f"{self.api_url}{url}", headers=self.headers, *args, **kwargs
        )

    def _put_request(self, url, *args, **kwargs) -> httpx.Response:
        """
        This function sends an HTTP PUT request to the specified URL with the custom headers and returns
        the response.

        Args:
            url: The URL of the HTTP request that the function will send a PUT request to.

        Returns:
            A HTTP response object of the type `httpx.Response`.
        """
        logger.debug(f"[PUT] request: {url=}, {kwargs}")
        return self.session.put(
            f"{self.api_url}{url}", headers=self.headers, *args, **kwargs
        )

    def _post_request(self, url, *args, **kwargs) -> httpx.Response:
        """
        This function sends an HTTP POST request to the specified URL with the custom headers and returns
        the response.

        Args:
            url: The URL of the HTTP request that the function will send a POST request to.

        Returns:
            A HTTP response object of the type `httpx.Response`.
        """
        logger.debug(f"[POST] request: {url=}, {kwargs}")
        return self.session.post(
            f"{self.api_url}{url}", headers=self.headers, *args, **kwargs
        )

    def _delete_request(self, url, *args, **kwargs) -> httpx.Response:
        """
        This function sends an HTTP DELETE request to the specified URL with the custom headers and returns
        the response.

        Args:
            url: The URL of the HTTP request that the function will send a DELETE request to.

        Returns:
            A HTTP response object of the type `httpx.Response`.
        """
        logger.debug(f"[DELETE] request: {url=}, {kwargs}")
        return self.session.delete(
            f"{self.api_url}{url}", headers=self.headers, *args, **kwargs
        )

    def get_todo(
        self,
        add_dateless: bool = True,
        completed: bool = None,
        start: datetime.datetime = None,
        end: datetime.datetime = None,
    ) -> objects.Todo:
        """
        The `get_todo` function retrieves a list of todos from the API based on specified parameters, such as
        add_dateless, completed, start date, and end date.

        #### API Requests: 1

        Args:
            add_dateless (bool): The `add_dateless` parameter is a boolean flag that determines whether or not
        to include dateless todos in the result. Defaults to True
            completed (bool): The `completed` parameter is a boolean flag that indicates whether to include
        completed todos in the result. If `completed` is set to `True`, the API will return both completed
        and incomplete todos. If `completed` is set to `False`, only incomplete todos will be
        returned. If completed is set to `None`, completed and incomplete todos will be returned.
            start (datetime.datetime): The `start` parameter is a `datetime.datetime` object that represents
        the start date for filtering the todos. If no start date is provided, it defaults to the current
        date and time.
            end (datetime.datetime): The `end` parameter is a `datetime.datetime` object that represents the
        end date for filtering todos. If no `end` date is provided, it defaults to the current date plus 3
        weeks.

        Returns:
            An object of type `objects.Todo`.
        """
        if start is None:
            start = datetime.datetime.now()
        if end is None:
            end = datetime.datetime.now() + datetime.timedelta(weeks=3)
        params = {
            "add_dateless": add_dateless,
            "from": start.strftime("%Y-%m-%d"),
            "to": end.strftime("%Y-%m-%d"),
        }
        if completed is not None:
            params["completed"] = completed
        r = self._get_request("/todos", params=params).json()
        return objects.make_todo(r["todos"])

    def get_detailed_task(
        self, task: objects.Task, obj: list = None
    ) -> objects.DetailedTask:
        """
        This function retrieves a detailed task object from the API based on a given task object and a list
        of objects.

        #### API Requests: 1

        Args:
            task (objects.Task): A task.
            obj (list): The `obj` parameter is a list that contains two elements: the first element is the
        class of the object that will be created and the second element is the type of task (e.g.
        "homework", "test", "quiz"). If `obj` is not provided, it defaults to [objects.DetailedTask, objects.TaskTypes.HOMEWORK].

        Returns:
            An instance of the `DetailedTask` class.
        """
        if obj is None:
            obj = [objects.DetailedTask, objects.TaskTypes.HOMEWORK]
        if obj[1].lower()[-1] != "s":
            api_path = f"{obj[1].lower()}s"
        else:
            api_path = obj[1].lower()

        r = self._get_request(f"/{api_path}/{task.class_task_id}")
        if r.status_code == 404:
            raise exceptions.InvalidTask(
                f"Task is not found! ({task.class_task_type=})"
            )
        r = r.json()
        return objects.Create.instantiate(obj[0], r[obj[1].lower()] | asdict(task))

    def get_auto_detailed_task(
        self, task: objects.Task
    ) -> (
        objects.DetailedTask
        | objects.Quiz
        | objects.ClassTest
        | objects.Classwork
        | objects.FlexibleTask
    ):
        """
        This function takes in a task object and returns a more detailed task object based on its type.

        #### API Requests: 1

        Args:
            task (objects.Task): The task parameter is an instance of the Task class from the objects module.
        It represents a task that needs to be retrieved or processed.

        Returns:
            An object of one of the following types:
        `objects.DetailedTask`, `objects.Quiz`, `objects.ClassTest`, `objects.Classwork`, or
        `objects.FlexibleTask`. The specific type of object returned depends on the `class_task_type`
        attribute of the `task` object passed as an argument to the function.
        """
        if task.class_task_type == objects.TaskTypes.HOMEWORK:
            return self.get_detailed_task(task)
        elif task.class_task_type == objects.TaskTypes.QUIZ:
            return self.get_quiz(task)
        elif task.class_task_type == objects.TaskTypes.CLASSTEST:
            return self.get_detailed_task(
                task, [objects.ClassTest, "class_test"]
            )  # no special details
        elif task.class_task_type == objects.TaskTypes.CLASSWORK:
            return self.get_detailed_task(
                task, [objects.Classwork, objects.TaskTypes.CLASSWORK]
            )  # no special details
        elif task.class_task_type == objects.TaskTypes.FLEXIBLETASK:
            return self.get_detailed_task(
                task, [objects.FlexibleTask, "flexible_task"]
            )  # no special details
        else:
            raise exceptions.InvalidTask(
                f"Task could not be auto-detected! ({task.class_task_type=})"
            )

    def get_quiz(self, task: objects.Task) -> objects.Quiz:
        """
        This function retrieves a quiz from the API and creates a Quiz object with its associated questions.

        #### API Requests: 2

        Args:
            task (objects.Task): The `task` parameter is an object of type `objects.Task`.
        The `task` object is also passed to the `objects.Quiz` constructor as additional data.

        Returns:
            an instance of the `Quiz` class.
        """
        if task.is_detailed():
            raise exceptions.TaskAlreadyDetailed(
                f"Task ID: {task.id} | Is already a detailed task!"
            )
        r = self._get_request(f"/quizzes/{task.class_task_id}").json()["quiz"]
        params = {"ids[]": r["question_ids"]}
        nr = self._get_request("/quiz_questions", params=params).json()

        nqq = [
            objects.Create.instantiate(objects.Question, question)
            for question in nr["quiz_questions"]
        ]
        return objects.Create.instantiate(
            objects.Quiz, r | {"questions": nqq} | asdict(task)
        )

    def get_user(self, user_id: int = None) -> objects.User:
        """
        Retrieves user information from an API and returns a User object.

        #### API Requests: 1

        Args:
            user_id (int): The `user_id` parameter is an optional integer that represents the ID of a user.

        Returns:
            an instance of the `objects.User` class.
        """
        r = self._get_request(f"/users/{user_id}")
        if r.status_code == 404:
            raise exceptions.InvalidUser(user_id)
        return objects.Create.instantiate(objects.User, r.json()["user"])

    def get_current_student(
        self,
        cached: bool = True,
        user_private_info: bool = True,
        school: bool = False,
        package: bool = False,
        premium_features: bool = False,
    ) -> objects.Student:
        """
        Retrieves student information from the API, including optional additional
        data such as user private info, school info, package info, and premium features.

        #### API Requests: 2 (0 if cached)

        Args:
            cached (bool): The `cached` parameter is a boolean flag that determines whether to retrieve the
        student information from a cache or make a new API request. If `cached` is set to `True` and the
        `user_id` matches `self.user_id`, the method will return the student information from the cache. Defaults to True
            user_private_info (bool): The `user_private_info` parameter determines whether to include the
        user's private information in the response. Defaults to True
            school (bool): The "school" parameter determines whether to include the school information of the
        student in the response. Defaults to False
            package (bool): The "package" parameter determines whether to include information about the
        student's package in the response. Defaults to False
            premium_features (bool): The `premium_features` parameter is a boolean flag that determines
        whether to include premium features in the returned student object. Defaults to False

        Returns:
            an instance of the `objects.Student` class.
        """

        if cached:
            return self._data["student"]

        include = ""
        if user_private_info:
            include += "user_private_info,"
        if school:
            include += "school,"
        if package:
            include += "package,"
        if premium_features:
            include += "premium_features,"

        params = {"include": include}
        response = self._get_request(f"/students/{self.user_id}", params=params)
        response = response.json()

        params = {
            "student_ids[]": self.user_id,
        }

        classes = [
            objects.Create.instantiate(objects.Class, c)
            for c in self._get_request("/class_groups", params=params).json()[
                "class_groups"
            ]
        ]
        return objects.Create.instantiate(
            objects.Student,
            response["student"]
            | response["user_private_infos"][0]
            | {"classes": classes},
        )

    def get_current_school(self, cached: bool = True) -> objects.School:
        """
        This function returns the current school object.
        This data was fetched when the class was created.

        #### API Requests: 2 (0 if cached)

        Returns:
            an instance of the `School` class.
        """
        if cached:
            return self._data["school"]

        params = {"include": "school"}
        response = self._get_request(f"/students/{self.user_id}", params=params)
        if response.status_code == 401:
            raise exceptions.InvalidAuth(self.auth, self.user_id, self.school_id)
        response = response.json()
        subjects = [
            objects.Create.instantiate(objects.Subject, subject)
            for subject in self._get_request(
                "/subjects",
                params={"school_id": self.school_id},
            ).json()["subjects"]
        ]
        return objects.Create.instantiate(
            objects.School, response["schools"][0] | {"subjects": subjects}
        )

    def get_current_parents(self) -> list[objects.Parent]:
        """
        This function retrieves the current parents associated with a student from an API and returns them
        as a list of Parent objects.

        #### API Requests: 1

        Returns:
            an instance of the `Parent` class.
        """
        params = {"ids[]": self._data["student"].parent_ids}
        r = self._get_request("/parents", params=params)
        return [
            objects.Create.instantiate(objects.Parent, user)
            for user in r.json()["parents"]
        ]

    def get_task_comments(self, task_id: int) -> dict:
        """
        This function retrieves comments for a given task from the API.

        #### API Requests: 1

        Args:
            task (int): The task's id.

        Returns:
            The comments as a dict object. # TODO AS ITS OWN OBJECT
        """
        params = {
            "commentable_id": task_id,
            "commentable_type": "ClassTask",
        }

        r = self._get_request("/comments", params=params)
        r = r.json()["comments"]
        logger.info(
            """If you are using this feature and you have data from it, please open a Github Issue with this data!
            (Reason: return data is currently a dict, want to make it a dataclass)"""
        )
        return r

    def get_employee(self, id: int | list[int]) -> objects.Employee:
        """
        This function retrieves an employee's data from the API using their ID and returns it as an Employee
        object or a list of Employee objects.

        #### API Requests: 1

        Args:
            id (int): The id parameter is an integer that represents the employee.

        Returns:
            The function `get_employee` returns an instance of `objects.Employee` if the `id` parameter
        matches a single employee, or a list of `objects.Employee` instances if the `id` parameter is a list
        and contains multiple employee ids. If the `id` parameter does not match any employee, the function raises an
        `exceptions.InvalidUser` exception.
        """

        r = self._get_request(f"/users/{id}")
        if r.status_code == 404:
            raise exceptions.InvalidUser(f"Employee not found! ({id=})")
        try:
            r = r.json()["user"]
            return objects.Create.instantiate(objects.Employee, r)
        except KeyError:
            r = r.json()["users"]
            return [objects.Create.instantiate(objects.Employee, user) for user in r]

    def get_calendar(
        self, date: datetime.datetime = None
    ) -> list[objects.PersonalCalendarTask]:
        """
        The `get_calendar` function retrieves personal calendar tasks from the API based on a specified date
        or the current date if none is provided.

        #### API Requests: 1

        Args:
            date (datetime.datetime): The `date` parameter is an optional parameter of type
        `datetime.datetime`. If no value is provided for `date`, it defaults to the current date and time.

        Returns:
            A list of objects of type `objects.PersonalCalendarTask`.
        """
        if date is None:
            date = datetime.datetime.now()
        params = {"date": date.strftime("%Y-%m-%d")}
        r = self._get_request("/personal_calendar_tasks", params=params)
        return [
            objects.Create.instantiate(objects.PersonalCalendarTask, data)
            for data in r.json()["personal_calendar_tasks"]
        ]

    def get_school_calendar(  # TODO: ADD FILTERS
        self, date: datetime.datetime = None
    ) -> list[objects.SchoolCalendarTask]:
        """
        The `get_school_calendar` function retrieves the school calendar tasks for a given date or the
        current date if none is provided.

        #### API Requests: 1

        Args:
            date (datetime.datetime): The `date` parameter is an optional parameter of type
        `datetime.datetime`. If no value is provided for `date`, it defaults to the current date and time
        obtained using `datetime.datetime.now()`.

        Returns:
            A list of `objects.SchoolCalendarTask` objects.
        """
        if date is None:
            date = datetime.datetime.now()
        params = {
            "date": date.strftime("%Y-%m-%d"),
            "subdomain": self._data["school"].subdomain,
        }
        r = self._get_request("/calendars", params=params)
        return [
            objects.Create.instantiate(objects.SchoolCalendarTask, data)
            for data in r.json()["calendars"]
        ]

    def get_behaviour(self, limit: int = 20, offset: int = 0) -> objects.Behaviour:
        """
        This function retrieves behaviour data for a student from the API.

        #### API Requests: 2

        Args:
            limit (int): The maximum number of behaviour report entries to retrieve in a single
        request. Defaults to 20
            offset (int): The offset parameter is used to specify the starting point of the data to be
        retrieved from the API. Defaults to 0

        Returns:
            an instance of the `Behaviour` class
        """
        params = {
            "student_id": self.user_id,
            "limit": limit,
            "offset": offset,
        }

        r = self._get_request(
            "/behaviour_breakdown_report_entries",
            params=params,
        )
        r = r.json()
        praises = [
            objects.Create.instantiate(objects.Praise, praise)
            for praise in r["student_kudos"]["student_praises"]
        ]
        psum = objects.Create.instantiate(
            objects.PraiseSummary,
            self._get_request(f"/student_praise_summaries/{self.user_id}").json()[
                "student_praise_summary"
            ],
        )
        return objects.Create.instantiate(
            objects.Behaviour,
            r["student_kudos"]
            | {"student_praises": praises}
            | {"student_praise_summary": psum},
        )

    def get_quiz_submission(self, quiz: objects.Quiz) -> objects.QuizSubmission:
        """
        The function `get_quiz_submission` retrieves a detailed quiz submission object from an API.

        #### API Requests: 1

        Args:
            quiz (objects.Quiz): The parameter "quiz" is an object of type "objects.Quiz".

        Returns:
            an instance of the `objects.QuizSubmission` class.
        """
        if not quiz.is_detailed():
            raise exceptions.TaskNotDetailed(
                f"Quiz ID: {quiz.id} | Is not a detailed task, you can fetch it's detailed version by using the function self.get_quiz()!"
            )
        r = self._get_request(f"/quiz_submissions/{quiz.submission_ids[0]}")
        return objects.Create.instantiate(
            objects.QuizSubmission, r.json()["quiz_submission"]
        )  # more sections: submission_events and submission_comments

    def put_quiz_answer(
        self, quiz: objects.Quiz, question_id: int, answer: str, delay: int = 0
    ) -> bool:
        """
        The `send_quiz_answer` function sends a quiz answer to the API and returns whether the
        answer was correct or not.

        #### API Requests: 2

        Args:
            quiz (objects.Quiz): Represents a quiz that a user is taking.
            question_id (int): The `question_id` parameter represents the ID of the question in the quiz that
        the user is answering.
            answer (str): The `answer` parameter is the answer that the user wants to submit for the quiz
        question.
            delay (int): How long to wait before sending the answer to the API.

        Returns:
            The function `send_quiz_answer` returns a boolean value indicating whether the answer provided for
        a quiz question was correct or not.
        """
        if not quiz.is_detailed():
            raise exceptions.TaskNotDetailed(
                f"Quiz ID: {quiz.id} | Is not a detailed task, you can fetch it's detailed version by using the function self.get_quiz()!"
            )

        api_id = f"{quiz.id}-{question_id}"

        question_data = self._get_request(f"/quiz_submission_questions/{api_id}")
        question_data = question_data.json()
        # check if question already done
        attempts = 0
        atts_keys = list(question_data["quiz_submission_question"].keys())
        max_attempts = max(int(a.replace("attempt", "")) for a in atts_keys)

        for i in range(max_attempts):
            try:
                question_data["quiz_submission_question"][f"attempt{i}"].get("correct")
                attempts += 1
                if attempts == quiz.max_attempts:
                    raise exceptions.QuestionAlreadyComplete(
                        f"Question {api_id=} is already complete!"
                    )
            except AttributeError:
                attempt = f"attempt{i}"
                break

        question_data["quiz_submission_question"][attempt] = {
            "answer": None,
            "start": datetime.datetime.now().isoformat(),
            "correct": False,
        }

        question_data = self._put_request(
            f"/quiz_submission_questions/{api_id}",
            json=question_data,
        ).json()

        question_data["quiz_submission_question"][attempt] = {
            "answer": answer,  # answer can be obtained by using: quiz.get_question(question_id).correct_answer
        }

        if delay:
            logger.debug(f"Waiting for {delay} seconds before sending answer...")
            time.sleep(delay)

        question_data = self._put_request(
            f"/quiz_submission_questions/{api_id}",
            json=question_data,
        ).json()

        return question_data["quiz_submission_question"][attempt][
            "correct"
        ]  # was it correct or not

    # TODO: I HAVE NO WAY OF TESTING THIS RIGHT NOW
    def post_comment(
        self, message: str, task: objects.Task, skip_profanity_check: bool = False
    ):
        """
        Post a comment on a task, with an option to skip profanity check.

        #### API Requests: 1

        Args:
            message (str): The `message` parameter is a string that represents the content of the comment that
        you want to post.
            task (objects.Task): The `task` parameter is an object of type `objects.Task`. It represents the
        task to which the comment is being posted.
            skip_profanity_check (bool): The `skip_profanity_check` parameter is a boolean flag that indicates
        whether the profanity check should be skipped when posting a comment. Defaults to False

        Returns:
            An instance of the `objects.Comments` class.
        """
        data = {
            "comment": {
                "message": message,
                "created_at": None,
                "skip_profanity_check": skip_profanity_check,
                "user_id": None,
                "user_type": None,
                "attachment_ids": [],
                "commentable_id": task.id,
                "commentable_type": task.class_task_type,
            }
        }

        r = self._post_request("/comments", data=data)
        r = r.json()
        users = [
            objects.Create.instantiate(objects.CommentUser, user) for user in r["users"]
        ]
        commentable = {
            "commentable": objects.Create.instantiate(
                objects.CommentableTask, r["comment"]["commentable"]
            )
        }
        del r["comment"]["commentable"]
        comments = [
            objects.Create.instantiate(
                objects.Comment, r["comment"] | {"commentable": commentable}
            )
        ]
        return objects.Create.instantiate(
            objects.Comments, {"users": users, "comments": comments}
        )

    def get_student_insight(self) -> objects.StudentInsight:
        data: dict = self._get_request(f"/student_insights/{self.user_id}").json()[
            "student_insight"
        ]
        attendance = objects.Create.instantiate(
            objects.AttendanceInsight, data["attendance"]
        )
        punctuality = objects.Create.instantiate(
            objects.PunctualityInsight, data["punctuality"]
        )
        return objects.Create.instantiate(
            objects.StudentInsight,
            data | {"attendance": attendance, "punctuality": punctuality},
        )

    def get_detailed_attendance(self) -> objects.DetailedAttendance:
        params = {"include": "attendance_codes,detailed_view"}
        data: dict = self._get_request(
            f"/attendance_students/{self.user_id}", params=params
        ).json()
        last_periods = [
            objects.Create.instantiate(objects.DetailedAttendancePeriod, period)
            for period in data["attendance_student"]["last_periods_info"]
        ]
        return objects.Create.instantiate(
            objects.DetailedAttendance,
            data["attendance_student"]
            | {"last_periods_info": last_periods}
            | data["meta"],
        )

    def get_detentions(
        self,
        start: datetime.datetime = None,
        end: datetime.datetime = None,
        limit: int = None,
        offset: int = 0,
        reasons: bool = True,
        employee: bool = True,
        detention_template: bool = True,
    ) -> objects.Detentions:
        if start is None:
            start = datetime.datetime.now() - datetime.timedelta(
                weeks=52.1429
            )  # minus 1 year
        if end is None:
            end = datetime.datetime.now() + datetime.timedelta(
                weeks=52.1429
            )  # plus 1 year

        include = ""
        if reasons:
            include += "reasons,"
        if employee:
            include += "employee,"
        if detention_template:
            include += "detention_template,"

        params = {
            "start_date": start,
            "end_date": end,
            "limit": limit,
            "offset": offset,
            "include": include,
        }
        data: dict = self._get_request("/detentions", params=params).json()
        return objects.Create.instantiate(
            objects.Detentions, {"detentions": data["detentions"]} | data["meta"]
        )

    def complete_task(self, task_id: int, state: bool):
        """
        Updates the completion state of a task with the given task ID.

        #### API Requests: 1

        Args:
            task_id (int): The task_id parameter is an integer that represents the unique identifier of the
        task that needs to be completed.
            state (bool): The `state` parameter is a boolean value that represents the completion state of the
        task.
        """
        json_data = {
            "todo": {
                "completed": state,
            },
        }

        self._put_request(f"/todos/{task_id}", json=json_data)

    def view_task(self, task_id: int, eventable_type: str) -> bool:
        """
        A "viewed" event for a specific task, and returns a boolean indicating the success of the request.

        #### API Requests: 1

        Args:
            task_id (int): The `task_id` parameter is an integer that represents the unique identifier of a
        task. It is used to identify the specific task that has been viewed.
            eventable_type (str): The `eventable_type` parameter is a string that represents the type of the
        eventable object. In this case, it is used to specify the type of the object that is being viewed.

        Returns:
            a boolean value.
        """
        json_data = {
            "event": {
                "event_type": "viewed",
                "eventable_type": eventable_type,
                "eventable_id": task_id,
            },
        }

        r = self._post_request("/events", json=json_data)
        return bool(r.text)

    def search_task(self, filter: str, limit: int = 7) -> objects.TaskSearchResults:
        """
        The `search_task` function searches for task submissions based on a filter and returns the results
        in a structured format.

        #### API Requests: 1


        Args:
            filter (str): The "filter" parameter is a string that specifies the search filter for the task. It
        is used to filter the tasks based on the task name.
            limit (int): The `limit` parameter is an optional parameter that specifies the maximum number of
        search results to return. Defaults to 7

        Returns:
            an instance of the `TaskSearchResults` class.
        """
        params = {
            "filter": filter,
            "limit": limit,
            "sort": "-created_at",
            "student_id": self.user_id,
        }

        r: dict = self._get_request("/submissions", params=params).json()
        data: dict[list, list] = {
            "homework_submissions": [],
            "quiz_submissions": [],
            "spelling_test_submissions": [],
            "class_test_submissions": [],
            "flexible_task_submissions": [],
            "classwork_submissions": [],
            "selection_count": r["meta"]["selection_count"],
        }
        for submission_type in r:
            for submission in r[submission_type]:
                if submission != "selection_count":
                    data[submission_type].append(
                        objects.Create.instantiate(objects.TaskSearchResult, submission)
                    )

        return objects.Create.instantiate(objects.TaskSearchResults, data)

    def get_task_from_id(
        self, task_id: int, type: str = "homeworks"
    ) -> objects.SearchedTask:
        r = self._get_request(f"/{type}/{task_id}")
        if r.status_code == 404:
            raise exceptions.InvalidTask(f"Task is not found! ({type=} | {task_id=})")
        return objects.Create.instantiate(objects.SearchedTask, r.json()["homework"])

    def get_notifications(
        self, limit: int = 21, offset: int = 0
    ) -> objects.Notifications:
        """
        Retrieves notifications for a user with a specified limit and offset.

        #### API Requests: 1

        Args:
            limit (int): The `limit` parameter specifies the maximum number of notifications to retrieve. Defaults to 21
            offset (int): The `offset` parameter is used to specify the starting point of the notifications to
        retrieve. It determines the number of notifications to skip before returning the results. Defaults to 0

        Returns:
            An instance of the `objects.Notifications` class.
        """
        params = {
            "limit": limit,
            "offset": offset,
            "recipient_id": self.user_id,
        }

        r = self._get_request("/events", params=params).json()
        notifs = []
        for notif in r["events"]:
            if "notice" in notif:
                notif["notice"] = objects.Create.instantiate(
                    objects.NotificationNotice, notif["notice"]
                )
            notifs.append(objects.Create.instantiate(objects.Notification, notif))
        return objects.Create.instantiate(
            objects.Notifications, {"events": notifs} | r["meta"]
        )

    def delete_notifications(self):
        """
        Deletes all notifications, this is an irreversible action!

        #### API Requests: 1

        """
        self._delete_request("/events/destroy_all")

    def get_calendar_token(self) -> str:
        """
        Return the calendar token stored in the cache. This can be used to link 3rd party calendars to your Homeworks.

        #### API Requests: 0

        """
        return self._data["student"].calendar_token

    def reset_calendar_token(self):
        """
        Resets the calendar token and refresh the class cache.

        #### API Requests: 1

        """
        self._post_request("/icalendars/reset_calendar_token")
        self._get_data()  # refresh cache

    def get_timetable(
        self, requestDate: datetime.datetime = None
    ) -> objects.TimetableInterface:
        """
        Retrieves a timetable for the current week.

        #### API Requests: 1

        Args:
            requestDate (datetime.datetime): The `requestDate` parameter is an optional parameter of type
        `datetime.datetime`. If no `requestDate` is provided, the current date is used.

        Returns:
            An instance of the `TimetableInterface` class from the `objects` module.
        """
        if requestDate is None:
            now = datetime.datetime.now()
            requestDate = now - datetime.timedelta(days=now.weekday())

        params = {
            "requestDate": requestDate.strftime("%Y-%m-%d"),
        }

        r = self._get_request(
            f"/timetable/school/{self.school_id}/student/{self.user_id}",
            params=params,
        )
        r = r.json()
        days = []
        for day in r["weeks"][0]["days"]:
            lessons = []
            for lesson in day["lessons"]:
                lesson["classGroup"] = objects.Create.instantiate(
                    objects.TimetableClassGroup, lesson["classGroup"]
                )
                lesson["period"] = objects.Create.instantiate(
                    objects.TimetablePeriod, lesson["period"]
                )
                lesson["teacher"] = objects.Create.instantiate(
                    objects.TimetableTeacher, lesson["teacher"]
                )
                ctasks = [
                    objects.Create.instantiate(objects.TimetableHomework, ctask)
                    for ctask in lesson["dueClassTasks"]
                ]
                lesson["dueClassTasks"] = ctasks
                lessons.append(
                    objects.Create.instantiate(objects.TimetableLesson, lesson)
                )
            days.append(
                objects.Create.instantiate(
                    objects.TimetableDay, day | {"lessons": lessons}
                )
            )
        timetable = objects.Create.instantiate(
            objects.Timetable, r["weeks"][0] | {"days": days}
        )
        return objects.Create.instantiate(
            objects.TimetableInterface, r | {"weeks": [timetable]}
        )

    @classmethod
    def change_client(cls, client: str):
        clients = ["web", "android"]
        client = client.casefold()
        if client not in clients:
            raise ValueError(f"{client} is a valid client! ({clients})")
        Client.current_client = client
        logger.info(f"Switched to using '{client}' client ids.")

    @classmethod
    def get_public_schools(
        cls, filter: str = "", limit: int = 20
    ) -> objects.PublicSchoolSearch:
        """
        The function `get_public_schools` retrieves a list of public schools based on a filter and limit,
        and returns an object containing the schools and metadata.

        #### API Requests: 1

        Args:
            filter (str): The "filter" parameter is used to specify a string search filter for the public schools.
            limit (int): The `limit` parameter specifies the maximum number of public schools to retrieve from
        the API. Defaults to 20.

        Returns:
            an instance of the `objects.PublicSchoolSearch` class.
        """
        params = {"filter": filter, "limit": limit}
        r = cls.session.get(
            f"{cls.api_url}/public/school_search",
            params=params,
            headers=cls.base_headers,
        )
        r = r.json()
        schools = [
            objects.Create.instantiate(objects.PublicSchool, school)
            for school in r["schools"]
        ]
        return objects.Create.instantiate(
            objects.PublicSchoolSearch, {"schools": schools} | r["meta"]
        )

    @classmethod
    def get_auth(cls, username: str, password: str, school_id: int) -> objects.Auth:
        """
        The function `get_auth` sends a POST request to the Satchel One API to authenticate a user with
        their username, password, and school ID.

        #### API Requests: 3 (+2, get_current_student)

        Args:
            username (str): The `username` parameter is a string that represents the username of the user
        trying to authenticate.
            password (str): The `password` parameter is a string that represents the user's password.
            school_id (int): The `school_id` parameter is an integer that represents the unique identifier of
        a school.

        Returns:
            an instance of the `Auth` class from the `objects` module.
        """
        data = {
            "grant_type": "password",
            "username": username,
            "password": password,
            "school_id": school_id,
            "verification_token": "",
        }

        params = cls.clients[cls.current_client]

        response = cls.session.post(
            "https://api.satchelone.com/oauth/token",
            params=params,
            data=data,
        )
        r = response.json()

        if response.status_code == 401:
            raise exceptions.InvalidCredentials(r, username, password, school_id)
        return objects.Create.instantiate(objects.Auth, r)

    def _get_data(self) -> dict:
        self._data["school"] = self.get_current_school(False)
        self._data["student"] = self.get_current_student(False)
        return self._data


def login(username: str, password: str, school_id: int) -> Client:
    """
    The `login` function takes a username, password, and school ID as input, uses them to authenticate
    the user, and returns a `Client` object with the necessary credentials.

    Args:
        username (str): The username is a string that represents the username of the user trying to log
    in. It is used to authenticate the user's identity. This can either be a email or a username.
        password (str): The `password` parameter is a string that represents the user's password.
            school_id (int): The `school_id` parameter is an integer that represents the unique identifier of
    the school. It is used to authenticate the user and ensure that they are associated with the correct
    school.

    Returns:
        an instance of the `Client` class.
    """
    auth = Client.get_auth(username, password, school_id)
    return Client(f"Bearer {auth.access_token}", auth.user_id, auth.school_id)
