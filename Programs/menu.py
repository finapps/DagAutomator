import runpy



def menu():
	print("\n************DAG Automator************ \n Select a script to run \n 1. Checking Account \n 2. Investment Account \n 3. Randomize Checking Account \n 4. Exit")
	choice = input()

	if choice == "1":
		file_globals = runpy.run_path("non_randomized_program.py")
		print("Checking Account XML Generated")
		menu()

	if choice == "2":
		#file = runpy.run_path("program_randomize.py")
		print("Investment Account XML Generated")
		menu()

	if choice == "3":
		file = runpy.run_path("program_randomize.py")
		print("Generating Random XML")
		menu()

	if choice == "4":
		print("Exiting...")
		exit()
menu()