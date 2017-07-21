"""
This is the top level object that modules will inherit from.
"""
import hashlib
import os
import random
import re
import shutil
import sys
import time

if os.name == 'posix' and sys.version_info[0] < 3:
    import subprocess32 as subprocess
else:
    import subprocess

from shlex import split as shlexSplit
from shutil import copyfile, copytree

class Module (object):
    def __init__(self, title, prompt='Bootcamp > ', banner='Welcome to the Linux Bootcamp.\nInitializing your environment...', flag=None, binaries=[], blacklist=[], whitelist=[], timeout=5):
        self.title = title
        self.prompt = prompt
        self.cur_prompt = '[~] '+prompt
        self.history = []
        self.banner = banner
        self.flag = flag
        self.binaries = binaries
        self.cmd_whitelist = whitelist
        self.cmd_blacklist = blacklist
        self.timeout = timeout

        self.real_root = os.open("/", os.O_RDONLY)

        # Environment
        #self.env = os.environ.copy()
        self.env = {}

        # Directory Tracking        
        self.env['HOME'] = '/home/root/'
        self.env['PWD'] = '/home/root/'
        self.env['OLDPWD'] = '/home/root/'
        self.env['TEMP'] = 'TEMP'
        
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

        # Create home directory
        home = self.root_dir+self.env['HOME']
        if not os.path.exists(home):
            os.makedirs(home)

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

        # Copy binaries (and copy dependencies) into environment
        for binary in self.binaries:
            new_bin = self.root_dir+'/bin/'+os.path.basename(binary)
            copyfile(binary, new_bin)
            os.chmod(new_bin, 0555)
            os.system("ldd "+binary+" | egrep '(.dylib|.so)' | awk '{ print $1 }' | xargs -I@ bash -c 'sudo cp @ "+self.root_dir+"@'")

        # Copy module files
        mod_fileroot = 'files/'+self.title
        print("DEBUG> file_root: "+mod_fileroot)
        if os.path.exists(mod_fileroot):
            print("DEBUG>Found module file_root")
            for f in os.listdir(mod_fileroot):
                print("DEBUG>Copying file {} to {}".format(f, self.root_dir+'/'+os.path.basename(f)))
                copytree(mod_fileroot+'/'+f, self.root_dir+'/'+os.path.basename(f))

        # Chroot into the virtual environment (This requires root access)
        os.chdir(self.root_dir)
        os.chroot(self.root_dir)
        os.chdir(self.env['HOME'])

        # Setup Environment Variables
        self.env['SHELL'] = '/bin/sh'
        self.env['PATH'] = '/bin'

    """
    Cleanup and then sys.exit. This should be overridden if special cleanup is necessary.
    """
    def exit(self):
        print("Cleaning up...")
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
            # Specifically allow cd, exit, clear, and pwd
            if program_input == 'cd' or program_input == 'exit' or program_input == 'clear' or program_input == 'pwd':
                return True
            
            # Check whitelist
            if self.cmd_whitelist is not None and self.cmd_whitelist != []:
                whitelist_matched = False
                for exp in self.cmd_whitelist:
                    r = re.compile(exp)
                    matches = r.findall(program_input)
                    if len(matches) > 0:
                        whitelist_matched = True
                        break
                if not whitelist_matched:
                    return False
            
            # Check blacklist
            if self.cmd_blacklist is not None and self.cmd_blacklist != []:
                blacklist_matched = False
                for exp in self.cmd_blacklist:
                    r = re.compile(exp) 
                    matches = r.findall(program_input)
                    if len(matches) > 0:
                        blacklist_matched = True
                        break
                if blacklist_matched:
                    return False
        return True

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
        # Simulate working directory
        if program_input.startswith('cd'):
            args = shlexSplit(program_input)
            if len(args) < 2 or args[1] == '~':
                self.env['OLDPWD'] = self.env['PWD']
                os.chdir(self.env['HOME'])
            elif args[1] == '-':
                tmp = self.env['OLDPWD']
                self.env['OLDPWD'] = self.env['PWD']
                os.chdir(tmp)
            else:
                self.env['OLDPWD'] = self.env['PWD']
                os.chdir(os.path.abspath(args[1]))

            self.env['PWD'] = os.getcwd()

            if self.env['PWD'].strip('/') == self.env['HOME'].strip('/'):
                self.cur_prompt = '[~] {}'.format(self.prompt)
            else:
                self.cur_prompt = '[{}] {}'.format(os.path.abspath(os.getcwd()), self.prompt)
            return ''
        elif program_input == 'pwd':
            return self.env['PWD']
        elif program_input == 'clear':
            sys.stderr.write("\x1b[2J\x1b[H")
            return ''
        
        # Execute Command
        cmd = " ".join(shlexSplit(program_input))
        print("DEBUG> Executing {}".format(cmd))
        program_output = subprocess.check_output(cmd, shell=True, env=self.env, timeout=self.timeout)
        self.history.append(program_input)
        return program_output
        
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

        while True:
            try:
                # Retrieve Input
                program_input = raw_input(self.cur_prompt)

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
