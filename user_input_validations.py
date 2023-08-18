import re

def validate_string():
    """
    Prompt the user to input a string that is not a numeric value (i.e., int or float).
    Parameters:
    prompt (str): The prompt to display to the user.
    Returns:
    str: The validated string input by the user.
    """
    while True:
        user_input = input()
        try:
            float(user_input)
            print("Invalid input. Please enter a non-numeric string.")
        except ValueError:
            return user_input


def get_num_jobs():
    """
    Prompt the user to input the maximum number of jobs to get (between 1 and 100).
    Returns:
    int: The validated number of jobs input by the user.
    """
    while True:
        try:
            num_of_jobs = input("Enter max number of jobs to get (1-100): ")
            if num_of_jobs.startswith("0") or not num_of_jobs.isnumeric():
                raise ValueError
            num_of_jobs = int(num_of_jobs)
            if num_of_jobs < 1 or num_of_jobs > 100:
                raise ValueError
            break
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 100.")
    return num_of_jobs


def get_distance():
    """
    Prompt the user to input the distance in km (8, 18, 40, 80, or 160).
    Returns:
    int: The distance in miles corresponding to the validated distance in km input by the user.
    """
    # 5=8k 10=18k 25=40k 50=80k 100=160
    distances = {8: 5, 18: 10, 40: 25, 80: 50, 160: 100}

    while True:
        try:
            distance_km = input("Enter distance in km (8 - 18 - 40 - 80 - 160): ")
            if distance_km.startswith("0") or not distance_km.isnumeric():
                raise ValueError
            distance_km = int(distance_km)
            if distance_km not in distances:
                raise ValueError
            distance = distances[distance_km]
            break
        except ValueError:
            print("Invalid input. Please enter a valid distance.")

    return distance


def get_sortby_choice():
    """
    Prompts the user to select a sorting option from a predefined list.
    Returns the selected sorting option after cleaning and formatting it.
    """
    # Define list of valid sorting options
    options = [
        "job title",
        "company name",
        "main location",
        "work place type",
        "date posted",
        "skills",
        "distance",
    ]
    while True:
        sortby_choice = input(f"Sort by? options: {', '.join(options)}\n")
        if sortby_choice in options:
            # clean leadin ending spaces and insert _
            sortby_choice = sortby_choice.strip().replace(" ", "_")
            sortby_choice = sortby_choice.upper()
            # use INT_MIN_DURATION column for this sorting
            if sortby_choice == "DISTANCE":
                sortby_choice = "INT_MIN_DURATION"
            return sortby_choice
        else:
            print("Invalid choice. Please enter a valid sorting option.")


def validate_email(prompt):
    """
    Prompts the user to enter an email address and validates its format.
    Returns the email address if it is valid.
    """
    while True:
        email_input = input(prompt)
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email_input):
            print("Invalid email. Please enter a valid email address.")
        else:
            return email_input
