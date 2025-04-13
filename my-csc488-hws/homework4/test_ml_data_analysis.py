from ml_data_analysis import compute_average_mass
from ml_data_analysis import check_hemisphere
from ml_data_analysis import count_classes
import pytest
from typing import List
"""
data = [{'thing':1},{'thing':2}]
assert(compute_average_mass(data,'thing') == 1.5)    # Test assert statement
print(compute_average_mass(data,'thing'))


data = [{'thing':4},{'thing':6}]
assert(compute_average_mass(data,'thing') == 5)    # Test: Average of 4,6 is 5
print(compute_average_mass(data,'thing'))

data = [{'thing':5},{'thing':5},{'thing':5}]
assert(compute_average_mass(data,'thing') == 5)    # Test: Average of 5,5,5 is 5
print(compute_average_mass(data,'thing'))

data = [{'thing':1},{'thing':2},{'thing':3},{'thing':4}]
assert(compute_average_mass(data,'thing') == 3)    # Test (FAIL): Average of 1,2,3,4 is 3
print(compute_average_mass(data,'thing'))
"""

def test_compute_average_mass():
    assert compute_average_mass([{'a':1}], 'a') == 1
    assert compute_average_mass([{'a':1}, {'a':2}], 'a') == 1.5
    assert compute_average_mass([{'a':1}, {'a':2}, {'a':3}], 'a') == 2
    assert compute_average_mass([{'a':10}, {'a':1}, {'a':1}], 'a') == 4
    assert isinstance(compute_average_mass([{'a':1}, {'a':2}], 'a'), float) == True

def test_compute_average_mass_exceptions():
    with pytest.raises(ZeroDivisionError):
        compute_average_mass([], 'a')                       # send an empty list
    with pytest.raises(KeyError):
        compute_average_mass([{'a':1}, {'b':1}], 'a')       # dictionaries not uniform
    with pytest.raises(ValueError):
        compute_average_mass([{'a':1}, {'a':'x'}], 'a')     # value not a float
    with pytest.raises(KeyError):
        compute_average_mass([{'a':1}, {'a':2}], 'b')       # key not in dicts

def test_check_hemisphere():
    assert check_hemisphere(1,1) == 'Northern & Eastern'
    assert check_hemisphere(-1,1) == 'Southern & Eastern'
    assert check_hemisphere(-1,-1) == 'Southern & Western'
    assert check_hemisphere(1,-1) == 'Northern & Western'
    assert isinstance(check_hemisphere(1,1), str) == True

def test_check_hemisphere_exceptions():
    with pytest.raises(TypeError):
        check_hemisphere(1,'f')

sample = [{"a": "a","b": "a"}, {"a": "b","b": "a"}, {"a": "c", "b": "b"}]
def test_count_classes(): 
    result1 = {'a':1, 'b':1, 'c':1}
    result2 = {'a':2, 'b':1}

    assert count_classes(sample, 'a') == result1
    assert count_classes(sample, 'b') == result2
    assert (type(count_classes(sample, 'a')) == dict) == True

def test_compute_count_classes_exceptions(): 
    with pytest.raises(KeyError):
        count_classes(sample, '')                           # no key sent
    with pytest.raises(KeyError):
        count_classes(sample, 2.0)                          # value not string
    with pytest.raises(KeyError):
        count_classes(sample, 'c')                          # key not in dict
    
