import sys
from cx_Freeze import setup, Executable

setup(
    name = "DagAutomator",
    version = "1",
    description = "Generate Dag Accounts",
    executables = [Executable("AutoRunMenu.py", base = "Win32GUI")])