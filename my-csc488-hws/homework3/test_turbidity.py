import math
import pytest

from turbidity import (
    calculate_turbidity,
    calculate_safety_factor,
    is_safe,
    print_current_turbidity,
    calculate_decay_time
)

def test_calculate_turbidity():
    """ Tests calculate_turbidity() from turbidity.py
    
    Performs five tests on the calculate_turbidity() function. The tests include:
        - Test 1: Sanity Check - Checks if calculate_turbidity() outputs the correct value.
        - Test 2: Zero Inputs - Checks calculate_turbidity() returns 0 if either input is 0.
        - Test 3: Error Handling - Checks calculate_turbidity() returns correct errors when a string is entered.
        - Test 4: Negative Inputs - Checks calculate_turbidity() returns proper negative inputs. 
        - Test 5: Type Check - Check if return type is correct.
    """
    cal_const = 1.2
    detector_current = 1.5
    expected = calculate_safety_factor(1.8)
    result = calculate_turbidity(cal_const, detector_current)

    # Test 1: Output Test
    assert round(result, 4) == round(expected, 4)

    # Test 2: Zero Input Behavior Test
    assert calculate_turbidity(0, 2.5) == 0
    assert calculate_turbidity(2.5, 0) == 0
    
    # Test 3: Error Handling Test
    with pytest.raises(TypeError, match="can't multiply sequence by non-int of type 'float'"):
        calculate_turbidity("1.2", 1.5)
    with pytest.raises(TypeError, match="can't multiply sequence by non-int of type 'float'"):
        calculate_turbidity(1.2, "1.5")
    
    # Test 4: Negative Input Behavior Test
    assert round(calculate_turbidity(-2, 3), 4) == round(calculate_safety_factor(-6), 4)

    # Test 5: Return Type Test
    assert isinstance(result, (int, float))

def test_calculate_safety_factor():
    """ Tests calculate_safety_factor() from turbidity.py
    
    Performs five tests on the calculate_safety_factor() function. The tests include:
        - Test 1: Sanity Check - Checks if calculate_safety_factor() outputs the correct value.
        - Test 2: Zero Inputs - Checks calculate_safety_factor() returns expected output if either input is 0.
        - Test 3: Error Handling - Checks calculate_safety_factor() returns correct errors when a string is entered.
        - Test 4: Negative Inputs - Checks calculate_safety_factor() returns proper negative inputs. 
        - Test 5: Type Check - Checks the return type is correct.
    """
    # Test 1: Output Test
    assert round(calculate_safety_factor(1.0), 4) == round(1.0 * (0.98**5), 4)
    assert round(calculate_safety_factor(10, 1), 4) == round(10 * 0.98, 4)
    assert round(calculate_safety_factor(10, 10), 4) == round(10 * (0.98**10), 4)

    # Test 2: Zero Input Test
    assert calculate_safety_factor(0) == 0
    assert round(calculate_safety_factor(10, 0), 4) == 10
    
    # Test 3: Error Handling Test
    with pytest.raises(TypeError, match="can't multiply sequence by non-int of type 'float'"):
        calculate_safety_factor("10", 1)
    with pytest.raises(TypeError):
        calculate_safety_factor(10, "1")
    
    # Test 4: Negative Input Test
    assert round(calculate_safety_factor(-10, 0), 4) == -10

    # Test 5: Return Type Test
    assert isinstance(calculate_safety_factor(10, 1), (int, float))

def test_is_safe():
    """ Tests is_safe() from turbidity.py
    
    Performs five tests on the is_safe() function. The tests include:
        - Test 1: Sanity Check - Checks if is_safe() outputs the correct value.
        - Test 2: Zero Inputs - Checks is_safe() returns expected output if either input is 0.
        - Test 3: Error Handling - Checks is_safe() returns correct errors when a string is entered.
        - Test 4: Negative Inputs - Checks is_safe() returns proper negative inputs. 
        - Test 5: Type Check - Checks the return type is correct.
    """
    # Test 1: Output Test
    assert is_safe(0.5) == True
    assert is_safe(1.0) == False
    assert is_safe(1.5, safety_threshold=2.0) == True

    # Test 2: Zero Input Test
    assert calculate_safety_factor(0) == 0
    assert round(calculate_safety_factor(10, 0), 4) == 10
    
    # Test 3: Error Handling Test
    with pytest.raises(TypeError):
        is_safe("1.0")
    with pytest.raises(TypeError):
        is_safe(1.0 ,"1.0")
    
    # Test 4: Negative Input Test
    assert is_safe(-1.0) == True
    assert is_safe(1.0, -1.0) == False

    # Test 5: Return Type Test
    assert isinstance(is_safe(0.5), (bool))

def test_print_current_turbidity():
    """ Tests print_current_turbidity() from turbidity.py
    
    Performs five tests on the print_current_turbidity() function. The tests include:
        - Test 1: Sanity Check - Checks if print_current_turbidity() outputs the correct value.
        - Test 2: Zero Inputs - Checks if print_current_turbidity() outputs the correct value when given 0 as inputs.
        - Test 3: Less than 5 inputs - Checks if print_current_turbidity() behaves correctly when given less than 5 data points 
        - Test 4: Missing keys - Tests print_current_turbidity() behavior when some keys are missing.
        - Test 5: Wrong data types - Checks print_current_turbidity() returns correct errors when data entries are the incorrect type.
        - Test 6: Type Check - Checks the return type is correct.
    """
    # Test 1: Output Test
    sample_data = [
        {"calibration_constant": 1.0, "detector_current": 1.0},
        {"calibration_constant": 1.1, "detector_current": 1.0},
        {"calibration_constant": 1.2, "detector_current": 1.0},
        {"calibration_constant": 1.3, "detector_current": 1.0},
        {"calibration_constant": 1.4, "detector_current": 1.0},
    ]

    result = print_current_turbidity(sample_data)
    expected = calculate_safety_factor((1.0 + 1.1 + 1.2 + 1.3 + 1.4) / 5)
    assert round(result, 4) == round(expected, 4)

    # Test 2: Zero Input Test
    data_zero = [{"calibration_constant": 0.0, "detector_current": 0.0} for _ in range(5)]
    assert print_current_turbidity(data_zero) == 0.0

    # Test 3: Index Error Test
    short_data = [
        {"calibration_constant": 1.0, "detector_current": 1.0},
        {"calibration_constant": 1.1, "detector_current": 1.0},
    ]
    with pytest.raises(IndexError):
        print_current_turbidity(short_data)

    # Test 4: Missing Key Test
    missing_key_data = [
        {"calibration_constant": 1.0, "detector_current": 1.0},
        {"calibration_constant": 1.1},  # Missing "detector_current"
        {"calibration_constant": 1.2, "detector_current": 1.0},
        {"calibration_constant": 1.3, "detector_current": 1.0},
        {"calibration_constant": 1.4, "detector_current": 1.0},
    ]
    with pytest.raises(KeyError):
        print_current_turbidity(missing_key_data)

    # Test 5: Improper Data Type Test
    bad_type_data = [
        {"calibration_constant": "1.0", "detector_current": 1.0},  # String instead of float
        {"calibration_constant": 1.1, "detector_current": 1.0},
        {"calibration_constant": 1.2, "detector_current": 1.0},
        {"calibration_constant": 1.3, "detector_current": 1.0},
        {"calibration_constant": 1.4, "detector_current": 1.0},
    ]
    with pytest.raises(TypeError):
        print_current_turbidity(bad_type_data)

    # Test 6: Return type is float
    valid_data = [
        {"calibration_constant": 2.0, "detector_current": 1.0},
        {"calibration_constant": 2.0, "detector_current": 1.0},
        {"calibration_constant": 2.0, "detector_current": 1.0},
        {"calibration_constant": 2.0, "detector_current": 1.0},
        {"calibration_constant": 2.0, "detector_current": 1.0},
    ]
    result = print_current_turbidity(valid_data)
    assert isinstance(result, float)

def test_calculate_decay_time():
    """ Tests calculate_decay_time() from turbidity.py
    
    Performs five tests on the calculate_decay_time() function. The tests include:
        - Test 1: Sanity Check - Checks if calculate_decay_time() outputs the correct value.
        - Test 2: Input Test - Checks if calculate_decay_time() outputs the correct value when given inputs.
        - Test 3: Invalid Input Test - Checks if calculate_decay_time() behaves correctly when given incorret input types. 
        - Test 4: Decay Rate Bounds Test - Tests calculate_decay_time() behavior when decay rate is either 0 or 100%.
        - Test 5: Return Type Test - Checks calculate_decay_time() returns correct value types.
    """
    # Test 1: Sanity Check
    result = calculate_decay_time(2.0)
    expected = math.log(1.0 / 2.0) / math.log(1 - 0.02)
    assert round(result, 4) == round(expected, 4)
    assert calculate_decay_time(1.0) == 0.0

    # Test 2: Input Test
    result = calculate_decay_time(3.0, threshold_turbidity=1.5, decay_rate_percent=5)
    expected = math.log(1.5 / 3.0) / math.log(1 - 0.05)
    assert round(result, 4) == round(expected, 4)

    # Test 3: Invalid Input Test
    with pytest.raises(TypeError):
        calculate_decay_time("high")
    with pytest.raises(TypeError):
        calculate_decay_time(2.0, threshold_turbidity="low")
    with pytest.raises(TypeError):
        calculate_decay_time(2.0, decay_rate_percent="fast")

    # Test 4: Decay Rate Bounds Test
    with pytest.raises(ZeroDivisionError):
        calculate_decay_time(2.0, decay_rate_percent=0)
    with pytest.raises(ValueError):
        calculate_decay_time(2.0, decay_rate_percent=100)

    # Test 5: Return Type Test
    assert isinstance(result, float)