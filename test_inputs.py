from user_input_validations import validate_string, get_num_jobs, get_distance,get_sortby_choice, validate_email

import pytest
from unittest import mock

#run test $ py -m pytest -s 
#run cove $ py -m pytest -s --cov=test_inputs --cov-report=html
@pytest.fixture
def mock_input():
    with mock.patch('builtins.input') as mocked:
        yield mocked

def test_validate_string(mock_input, capsys):
    # Test case 1: Input with only letters
    mock_input.return_value = "Developer"
    assert validate_string() == "Developer"

    #Test case 2: Input with only letters
    mock_input.side_effect = [666,44]
    assert validate_string() == None #nothing is return

    # Test case 3: Input with letters and spaces
    mock_input.side_effect = ["It Technician"]
    assert validate_string() == "It Technician"
    captured = capsys.readouterr()
    assert captured.out.strip() == "Invalid input. Please enter a non-numeric string."

    # Test case 4: Input with text with spaces and numbers
    mock_input.side_effect = [ "Los Angeles",888," Hambung "]
    assert validate_string() == "Los Angeles"
    captured = capsys.readouterr()
    #No error detected  No output produced 
    assert captured.out.strip()== ""
    #Test for second item in side_effect
    assert validate_string() == None
    #Test for third item in side_effect
    assert validate_string() == " Hambung "

     # Capture the output when error produced
    captured = capsys.readouterr()
    assert captured.out.strip() == "Invalid input. Please enter a non-numeric string."
 
@pytest.mark.parametrize("input_values, expected_output", [
    (["12", "8", "99"], [12, 8, 99]),  # Test case 1: Valid input
    (["10", "abc", "101", "50"], [10, None, None, 50]),  # Test case 2: Invalid input followed by valid input
    (["100", "-5", "200", ""], [100, None, None, None]),  # Test case 3: Empty input followed by invalid input and valid input
])
def test_get_num_jobs(input_values, expected_output, monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: input_values.pop(0))
    assert get_num_jobs() == expected_output.pop(0)
    captured = capsys.readouterr()
    assert captured.out.strip() == ""  # Ensure no output is produced

@pytest.mark.parametrize("input_value, expected_output", [
    ("8", 5),
    ("18", 10),
    ("40", 25),
    ("80", 50),
    ("160", 100),
    ("08", ""),
    ("1", ""),
    ("068", ""),
    ("a66", ""),
])
def test_get_distance(input_value, expected_output, monkeypatch, capsys):
    monkeypatch.setattr('builtins.input', lambda x: input_value)
    assert get_distance() == expected_output
    captured = capsys.readouterr()


@pytest.mark.parametrize("input_value, expected_output", [
    ("job title", "JOB_TITLE"),
    ("company name", "COMPANY_NAME"),
    ("main location", "MAIN_LOCATION"),
    ("work place type", "WORK_PLACE_TYPE"),
    ("date posted", "DATE_POSTED"),
    ("skills", "SKILLS"),
    ("distance traveltime", "INT_MIN_DURATION"),
    (None, None) # input not in options returns None
])
def test_get_sortby_choice(input_value, expected_output, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: input_value)
    assert get_sortby_choice() == expected_output

    



@pytest.mark.parametrize("input_value, expected_output", [
    ("anemail@gmail.com", "anemail@gmail.com"),
    ("joeemail123@yahoo.com", "joeemail123@yahoo.com"),
    ("1977jane_2@hotmail.com", "1977jane_2@hotmail.com"),
    ("missing@domain",None),
    ("invalid@.com",None)
])
def test_validate_email(input_value, expected_output, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda: input_value)
    assert validate_email() == expected_output
