from user_input_validations import validate_string
from user_input_validations import get_num_jobs

import pytest
from unittest import mock

import pytest
from unittest import mock

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