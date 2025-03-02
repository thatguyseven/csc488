# File Name: print_primes.py
# Assignment: Homework 1
# PROBLEM: 
# Using nested for loops and if statements, write a program that iterates over every integer
# from 3 to 100 (inclusive) and prints out the number only if it is a prime number.

def is_prime(num):
	# Check if a number is prime
	if num < 2: 
		return False
	for divisor in range(2, int(num ** 0.5) + 1):
		# print(num, " | ", divisor, " | ",  num%divisor)
		if num % divisor == 0:
			# print("\n")
			return False
	return True


# Prints prime numbers between 3 and 100
for num in range(3,101):
	if is_prime(num):
		print(num)
		# print("PRIME!")
