import runpy

def menu():
	print("\n************DAG Automator************ \n Select an Option \n 1. All Files \n 2. Exit Program")

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
