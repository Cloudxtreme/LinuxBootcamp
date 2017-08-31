"""
Module designed to teach basic command line usage.

Concepts:
    files
    ls
    cat
    grep
    cd
    pwd
"""
from .module import Module

"""
This function must be present in all module files, 
and must return an instance of the module class.
"""
def create():
    return Basic_Commands()

class Basic_Commands(Module):
    def __init__(self):
        self.stage = 0

        Module.__init__(self,

            # Title
            'Basic_Commands',

            # Prompt
            'Bootcamp(Basic Commands) > ',

            # Banner
            """
            In this module, you will learn how to utilize basic commands. 
            Find the flag to complete the module.

            Initializing your environment...
            """,

            # Flag (Set to None if using your own is_success)
            'flag1',

            # Copied binaries
            [
                '/bin/ls',
                '/bin/cat',
                '/bin/echo',
                '/usr/bin/touch',
                '/usr/bin/whoami',
                '/usr/bin/stat',
                '/usr/bin/env',
                '/usr/bin/grep',
                '/bin/mkdir',
                '/bin/chmod',
                '/usr/bin/id'
            ],

            # Blacklist Regular Expressions (Blacklist matching input)
            ['blacklist'],

            # Whitelist Regular Expressions (Whitelist matching input)
            ['.*'],

            # Set a timeout for commands
            10,

            # UID to execute commands with
            1001,

            # GID to execute commands with
            1001)
    
    """
    This function is called to start the module.
    You may override this for a more custom experience.
    """
    def start(self):
        print(""" 
        First, let me introduce you to the shell.
        This is the command line in linux that let's you run commands, it's a very powerful tool.

        The first command to learn is 'ls', which will list files in your current directory. 
        Enter the command 'ls' to continue.
        """)
        self.input_loop(self.parser_func)
        self.exit(False)
        print("Congratulations! You've completed {}\n".format(self.title))

    def parser_func(self, program_input):
        if program_input == 'exit':
            self.exit()
        
        if self.stage == 0:
            if self.check('ls', program_input):
               self.stage = 1
               print(
               """
               'ls' shows you the files in your current directory.
               Issue the command 'pwd' or Print Working Directory, to see the directory you're currently in.
               """)
            else:
                return ''
        elif self.stage == 1:
            if self.check('pwd', program_input):
                self.stage = 2
                print(
                """
                As you can see, we're currently in {}. Let's move to the 'root directory' of the file system.
                You can do this by using the Change Directory command, or 'cd'. Without giving it any arguments,
                cd will bring you to your home directory. To change to the root directory, issue the command
                'cd /'
                """
                )
            else:
                return ''       
        elif self.stage == 2:
            if self.check('cd /', program_input):
                self.stage = 3
                print(
                """
                Now we're in the root directory of the file system. Every file is located somewhere underneath here.
                To see the files and directories immediately below, we could use the 'ls' command. But, did you know that
                files in linux that start with a '.' are hidden by default? We can show hidden files by issuing the ls command
                with some arguments. Type 'ls -al' to show all files, and list their properties.
                """
                )
            else:
                return ''       
        elif self.stage == 3:
            if self.check('ls -al', program_input):
                self.stage = 4
	    else:
                return ''
	else:
	    pass
        program_output = self.safe_exec(program_input)

        print(program_output)

        return program_output
