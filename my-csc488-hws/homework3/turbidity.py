import json
import math
import logging

logging.basicConfig(level=logging.DEBUG)

def calculate_turbidity(cal_const, detector_current):
    """ Calculates the turbidity of a given sample.
    
    This function takes in the calibration contsant and ninety 
    degree detector current and multiplies them to get the 
    current turbidity of the water sample. 

    Example usage:
        turbidity = calculate_turbidity(float, float)
    """
    turb = cal_const * detector_current
    return calculate_safety_factor(turb)

def calculate_safety_factor(curr_turbidity, hours_elapsed = 5):
    """ Calculates safety factor for water sample.
    
    Calculates the current safety factor using the current turbidity of
    the sample and the number of hours passed, with a default value of 
    5 assuming the input is based on the last 5 data points. Returns 
    the safety factor.

    Example Usage:
        boolean_value = calculate_safety_factor(float)
        boolean_value = calculate_safety_factor(float, float)
    """
    decay = 0.02 # per hour
    safety_factor = curr_turbidity * ((1 - decay)**hours_elapsed)
    return safety_factor

def is_safe(curr_turbidity, safety_threshold = 1.0):
    """ Determines if the sample is safe to drink.
    
    Compares the safety factor with the safety threshold to determine
    whether the water is safe to drink. Returns True if safety factor is 
    below the safety threshold. Otherwise, returns False.

    Example Usage: 
        turbidity = 0.99
        if (is_safe(turbidity):
        ...
    """
    # safety_factor = calculate_safety_factor(curr_turbidity, hours_elapsed)
    if (curr_turbidity < safety_threshold):
        return True
    else: 
        return False


def print_current_turbidity(turbility_data):
    """ Prints the current turbidity of the water based on the last 5 samples.

    Reads the last 5 data points from the turbidity data and calculates 
    the current turbidity of the water.

    Example Usage: 
        print_current_turbidity(data_dict)
    """
    sum = 0
    elements = 5
    
    # Calculates the turbidity of the last 5 datapoints and sums them
    for i in range(-1, -6, -1):
        sum += calculate_turbidity(turbility_data[i]["calibration_constant"], turbility_data[i]["detector_current"])
    
    # Calculates the avarage turbidity of sample
    average = sum / elements

    # Return the trubidity value
    return average 

def calculate_decay_time(initial_turbidity, threshold_turbidity = 1.0, decay_rate_percent = 2.0):
    """ Calculate the time (in hours) it takes for turbidity to decay to a threshold.

    Uses the initial turbidity to calculate the time required until the turbidity to decay to a safe level.
    Example Usage:
        calculate_decay_time(turbidity)
        calculate_decay_time(turbidity, 2.0)
        calculate_decay_time(turbidity, 2.0, 5)
    """
    if is_safe(initial_turbidity):
        return 0.0  # Already at or below the threshold

    decay_rate = decay_rate_percent / 100.0
    remaining_fraction = threshold_turbidity / initial_turbidity

    time_hours = math.log(remaining_fraction) / math.log(1 - decay_rate)
    return time_hours

def main():
    # STEP 1: Extract data from turbidity.json
    with open('turbidity_data.json', 'r') as f:
        t_data = json.load(f)
    
    # STEP 2: Calculate current turbidity
    turbidity = print_current_turbidity(t_data["turbidity_data"])
    
    # STEP 3: Determine water safety and print time until safe consumption
    decay_time = calculate_decay_time(turbidity) 

    # STEP 4: Print turbidity information and safety
    # Print the turbidity
    print(f"Average turbidity based on most recent five measurements = {turbidity} NTU")

    # Logging statements
    if(is_safe(turbidity)):
        logging.info("Turbidity is below threshold for safe use.")

    # Print the current decay time
    print(f"Minimum time required to return below a safe threshold = {decay_time} hours")

if __name__ == "__main__":
    main()