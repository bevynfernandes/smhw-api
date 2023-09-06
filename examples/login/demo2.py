import smhw_api as api

# Enter your account credentials
AUTH: str = ""
USER_ID: int = 0
SCHOOL_ID: int = 0


def main():
    "This method merges the fetching of the Bearer auth and creating the client instance into one by using the login() function."
    email = input("Email: ")
    password = input("Password: ")
    school = input("School Name: ")
    school_results = api.Client.get_public_schools(
        school, limit=1
    )  # get the school with the most similar name as `school`

    # Attempt to login
    # If the login is invalid the `InvalidCredentials` exception is thrown.
    # And create the client instance
    client = api.login(email, password, school_results.schools[0].id)
    # Your code


if __name__ == "__main__":
    main()
