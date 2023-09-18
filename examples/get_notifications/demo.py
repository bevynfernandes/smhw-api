# TODO

import smhw_api as api

# Enter your account credentials
AUTH: str = ""
USER_ID: int = 0
SCHOOL_ID: int = 0


def main():
    client = api.Client(AUTH, USER_ID, SCHOOL_ID)
    notifications = client.get_notifications()
    for notification in notifications.events:
        task_id = notification.assignment_id
        task = client.get_task_from_id(task_id)
        print(task)


if __name__ == "__main__":
    main()
