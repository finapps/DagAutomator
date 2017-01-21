import runpy
import os


def menu():
	print("Please choose a script to run")
	print("1: Update Transaction Dates to Current Dates")
	print("2: Randomize Transactions with in last 90 Days")
	print("3: Exit")
	choice = input()

	if choice == "1":
		file_globals = runpy.run_path("non_randomized_program.py")
		print("Updating Transaction Dates")
		menu()

	if choice == "2":
		file = runpy.run_path("program_randomize.py")
		print("Generating Random XML")
		menu()

	if choice == "3":
		print("Exiting...")
		exit()
menu()