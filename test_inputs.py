from user_input_validations import validate_string

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
     
