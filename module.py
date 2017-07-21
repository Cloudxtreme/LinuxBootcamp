"""
This is the top level object that modules will inherit from.
"""
import hashlib
import os
import process_isolation
import random
import shutil
import subprocess
import sys
import time

from shlex import split as shlexSplit
from shutil import copyfile, copytree

class Module (object):
    def __init__(self, title, prompt='Bootcamp > ', banner='Welcome to the Linux Bootcamp.\nInitializing your environment...', flag=None, allowed_commands=[], binaries=[]):
        self.title = title
        self.prompt = prompt
        self.banner = banner
        self.flag = flag
        self.allowed_commands = allowed_commands
        self.binaries = binaries
        self.real_root = os.open("/", os.O_RDONLY)

        self.context = None

        # Generate unique directory path
        md5_hash = hashlib.md5()
        md5_hash.update(str(self.title)+str(time.time())+str(random.randint(0, 429496729)))
        self.root_dir = '/tmp/bootcamp/'+md5_hash.hexdigest()

        # Initialize a virtual environment for the module
        self.initialize()

    """
    Initialize the environment for this module.
    If your module requires additional support, either override this method,
    or the `start` method (If you want to also include this functionality).
    """
    def initialize(self):
        # Print the banner
        print(self.banner)

        # Create the virtual env directory
        venv_dir = self.root_dir+'/bin'
        if not os.path.exists(venv_dir):
            os.makedirs(venv_dir)

        # Copy sh
        if '/bin/sh' not in self.binaries:
            self.binaries.append('/bin/sh')

        # Copy bash
        if '/bin/bash' not in self.binaries:
            self.binaries.append('/bin/bash')

        # Create /usr/lib
        if not os.path.exists(self.root_dir+'/usr/lib'):
            os.makedirs(self.root_dir+'/usr/lib')

        # Copy files in /usr/lib
        for f in os.listdir('/usr/lib'):
            newpath = os.path.abspath(self.root_dir+'/usr/lib/'+f)
            os.system('cp -rf /usr/lib/'+f+' '+newpath)

        # Copy binaries (and hard link dependancies) into environment
        for binary in self.binaries:
            new_bin = self.root_dir+'/bin/'+os.path.basename(binary)
            copyfile(binary, new_bin)
            os.chmod(new_bin, 0555)
            #copy_dependencies(self.root_dir, binary)
            os.system("ldd "+binary+" | egrep '(.dylib|.so)' | awk '{ print $1 }' | xargs -I@ bash -c 'sudo cp @ "+self.root_dir+"@'")

        # Generate a context used for execution of commands in virtual env
        self.context = process_isolation.default_context()
        self.context.ensure_started()

        # Put the context in a chroot
        self.context.client.call(os.chroot, self.root_dir)

        # Ensure '/' and '/bin' exist
        #if not os.path.exists(self.root_dir):
        #    os.mkdir(self.root_dir)
        #if not os.path.exists(self.root_dir+'/bin'):
        #    os.mkdir(self.root_dir+'/bin')
        # 


        # Chroot into the virtual environment (This requires root access)
        os.chdir(self.root_dir)
        os.chroot(self.root_dir)

        # Set the new PATH
        #os.environ["PATH"] = "/bin"

    """
    Cleanup and then sys.exit. This should be overridden if special cleanup is necessary.
    """
    def exit(self):
        # Exit the chroot environment
        os.fchdir(self.real_root)
        os.chroot(".")
        os.close(self.real_root)

        try:
            shutil.rmtree(self.root_dir)
        except Exception as e:
            # Couldn't cleanup properly, still exit though.
            pass

        sys.exit('Exiting Bootcamp...')
        
    """
    This function is used to determine if we will allow the user input.
    """
    def validate_input(self, program_input):
        if program_input is not None and program_input != "":
            cmd = program_input.split(' ')[0]
            if cmd in self.allowed_commands or cmd == 'exit':
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

    """
    Execute a command within the virtual environment.
    """
    def safe_exec(self, program_input):
        cmd = shlexSplit(program_input)
        program_output = subprocess.check_output(cmd, shell=True)
        print(program_output)
        return program_output

        #sandbox = self.context.load_module('sandbox', path=['.'])
        #program_output = self.context.client.call(os.system, 'ls -al')
        #program_output = sandbox.sandbox_exec('')
        #program_output = self.context.client.call(subprocess.check_output, cmd, shell=True)
        #program_output = subprocess.check_output(cmd, shell=True)
        #print(program_output)

    """
    This is the default parser_func that is called by input_loop with program_input.
    By default, it look's for the exit command, if found it calls self.exit. Else,
    it will execute the given command in the virtual environment.
    """
    def parser_func(self, program_input):
        if program_input == 'exit':
            self.exit()

        program_output = self.safe_exec(program_input)

        print(program_output)

        return program_output

    """
    This function will loop, displaying the prompt and recieving input.
    Input received is sent to the given parser_func parameter.
    """
    def input_loop(self, parser_func):
        print("DEBUG> Starting input loop. Here's some info")
        print(os.environ)
        print([f for f in os.listdir('.') if os.path.isfile(f)])
        #print(os.getcwd())
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
                print(e)
                print("Error: Could not execute command")
