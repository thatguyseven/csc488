# Homework 3
This directory contains the contents required to complete Homework 3. 

## Task
Your robot has finished collecting its five meteorite samples and has taken them back
to the Mars lab for analysis. In order to analyze the samples, however, you need clean water. You
must check the latest water quality data to assess whether it is safe to analyze samples, or if the
Mars lab should go on a boil water notice.

## Contents
The contents of this folder are as follows:

| File | Description | 
| - | - |
| `turbidity.py` | A python script that analyzes data from `turbidity_data.json` and analyzes if the water sample is clean enough. |
| `test_turbidity.py` | A pytest script that tests `turbidity.py` to ensure `turbidity.py` is functioning properly. | 

## Downloading `turbidity_data.json`
To download `turbidity_data.json`:
1. Navigate Module 4 in Blackboard.
2. Open `Assignments and Assessment` folder.
3. Download `turbidity_data.json` from the `M4-HW3` assignment.

## Running the Code
To run `turbidity.py`:
1. Download the project files from this directory.
2. Download `turbidity_data.json` by following the instruction above.
3. Place `turbidity_data.json` in the same directory as the project files.
4. Open the terminal and navigate to the directory with the project files.
5. Run `python3 turbidity.py` in the terminal. The output should look something like this:
  ![turbidity_output](https://github.com/user-attachments/assets/b6c4e7a9-ead3-43d7-b99d-8e429892a948)

To run `test_turbidity.py`:
1. Follow steps 1-4 of the above instructions.
2. Run `pytest test_turbidity.py` in the terminal.
## Results
The results are printed in Nephelometric Turbidity Unit (NTU), which represents the amount of particles in the solution. To analyze meteorite samples, the water used should have a NTU below 1.0. A NTU above 1.0 indicates that a boil water notice should be put into place.
