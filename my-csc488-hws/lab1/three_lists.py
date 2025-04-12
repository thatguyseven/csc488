# File Name: three_lists.py
# Assignment: Homework 1
# PROBLEM: 
# Create three lists containing 10 integers each. The first list should contain all the
# integers sequentially from 1 to 10 (inclusive). The second list should contain the squares
# of each element in the first list. The third list should contain the cubes of each element
# in the first list. Print all three lists side-by-side in three columns. E.g. the first row
# should contain 1, 1, 1 and the second row should contain 2, 4, 8.

# Creates a list of numbers from 1 to 10 (inclusive)
def create_list_1_to_10():
	list = []
	for x in range(1,11):
		list.append(x)
	return list

list = create_list_1_to_10()
squares = []
cubes = []

# Appends squares of elements in list to squares list
for num in list:
        squares.append(num ** 2)

# Appends cubes of elements in list to cubes list
for num in list:
        cubes.append(num ** 3)

# Print out elements in all three lists
print("Base elements : ", list)
print("Elements squared : ", squares)
print("Elements cubed : ", cubes)
