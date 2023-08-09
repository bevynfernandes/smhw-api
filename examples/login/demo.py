import smhw_api as api

# Enter your account credentials
AUTH: str = ""
USER_ID: int = 0
SCHOOL_ID: int = 0


def main():
    email = input("Email: ")
    password = input("Password: ")
    school = input("School Name: ")
    school_results = api.Server.get_public_schools(
        school, limit=1
    )  # get the school with the most similar name as `school`

    # Attempt to login
    # If the login is invalid the `InvalidCredentials` exception is thrown.
    auth = api.Server.get_auth(email, password, school_results.schools[0])
    print(f"Logging into account with USER ID: {auth.user_id}")

    # Create the server instance
    server = api.Server(f"Bearer {auth.access_token}", auth.user_id, auth.school_id)
    # Your code


if __name__ == "__main__":
    main()
