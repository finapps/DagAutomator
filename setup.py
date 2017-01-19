from cx_Freeze import setup, Executable

setup(name='dagAutomator',
      version='1.0',
      description='Create DAGs',
      executables = [Executable("program.py")])