import runpy
import getpass
import random


def menu():
	#gets Usersname from computer
	userName = getpass.getuser()

	#List called if Wrong input is Selected
	myList = [" Really? There is two choices...TWO!!", 
		" Wow! I'm amazed at your stupidity", "Numbers are hard.... :-)", 
		" Are you kidding me?! Here Lets Practice... 1 .... 2....", 
		" What you've just selected is one of the most insanely idiotic \n"
		" things I have ever seen. At no point in your rambling incoherent response \n"
		" were you even close to anything that could be considered a rational response.\n"
		" Everyone in this room is now dumber for having listened to it.\n"
		" I award you no points and may God have mercy on your soul.", 
		" I'm sorry, " + str(userName) + ". I can't do that."]
	
	print("\n************Welcome " + str(userName) + " to the DAG Automator************")
	print("Select an Option \n 1. All Files \n 2. Exit Program")
	
	choice = input()
	while choice not in ("1","2"):
		print(random.choice(myList))
		print("Try Again!")
		menu()
		choice = input()
	if choice == "1":
		file = runpy.run_path("checking_1_updater.py")
		file2 = runpy.run_path("checking_2_updater.py")
		file3 = runpy.run_path("securebank_1_updater.py")
		file4 = runpy.run_path("investment_1_updater.py")
		
		print("All XML Files Generated")
		menu()
	if choice == "2":
		print("Exiting...")
		exit()
menu()