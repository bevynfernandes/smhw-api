import smhw_api as api

# Enter your account credentials
AUTH: str = ""
USER_ID: int = 0
SCHOOL_ID: int = 0


def main():
    # Enable debug mode on the module
    # This shows the requests sent to the API in the console
    api.set_debug(True)
    server = api.Client(AUTH, USER_ID, SCHOOL_ID)
    # Your code here


if __name__ == "__main__":
    main()
