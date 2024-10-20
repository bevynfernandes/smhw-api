"demo2.py is suggested over this method as it is more concise and easier to read."
import smhw_api as api


def main():
    email = input("Email: ")
    password = input("Password: ")
    school = input("School Name: ")
    school_results = api.Client.get_public_schools(
        school, limit=1
    )  # get the school with the most similar name as `school`

    # Attempt to login
    # If the login is invalid the `InvalidCredentials` exception is thrown.
    auth = api.Client.get_auth(email, password, school_results.schools[0].id)
    print(f"Logging into account with USER ID: {auth.user_id}")

    # Create the client instance
    client = api.Client(f"Bearer {auth.access_token}", auth.user_id, auth.school_id)
    # Your code


if __name__ == "__main__":
    main()
