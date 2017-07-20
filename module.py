"""
This is the top level object that modules will inherit from.
"""
import sys
import subprocess
import shlex

class Module (object):
    def __init__(self, title, prompt='Bootcamp > ', flag=None, allowed_commands=[]):
        self.title = title
        self.prompt = prompt
        self.flag = flag
        self.allowed_commands = allowed_commands

    """
    Cleanup and then sys.exit. This should be overridden if special cleanup is necessary.
    """
    def exit(self):
        sys.exit('Exiting Bootcamp...')
        
    """
    This function is used to determine if we will allow the user input.
    """
    def validate_input(self, program_input):
        if program_input is not None and program_input != "":
            cmd = program_input.split(' ')[0]
            if cmd in self.allowed_commands:
                return True
        return False

    """
    Inheriting modules should override this function with their own logic.
    This function is used to determine if the input/output should complete the module.
    """
    def is_success(self, program_input, program_output):
        if self.flag is not None:
            return self.flag in program_input or self.flag in program_output
        return False

    def parser_func(self, program_input):
        if program_input == 'exit':
            self.exit()

        program_output = subprocess.check_output(shlex.split(program_input), shell=True)
        print(program_output)

        return program_output

    """
    This function will loop, displaying the prompt and recieving input.
    Input received is sent to the given parser_func parameter.
    """
    def input_loop(self, parser_func):
        while True:
            try:
                # Retrieve Input
                program_input = raw_input(self.prompt)

                # Validate
                if not self.validate_input(program_input):
                    print("Error: Invalid input")
                    continue

                # Parse and execute
                if callable(parser_func):
                    program_output = parser_func(program_input)
            except Exception as e:
                print("Error: Could not execute command")
