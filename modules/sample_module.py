"""
This sample module demonstrates how to create
training modules using the framework provided to you.

You may add your own modules by implementing a similar pattern,
and then including your module in this package's __init__.py
"""

from .module import Module

""""
This class needs to inherit from Module, and will gain all of that functionality.
"""
class Sample_Module(Module):
    def __init__(self):
        Module.__init__(
            self,

            # Title
            'Sample_Module',

            # Prompt
            'Bootcamp(Sample Module) > ',

            # Banner
            """
            Welcome to the Linux Bootcamp.
            This is a sample module, with a flag of 'flag1'
            All commands are whitelisted, and anything containing "blacklist" will be blacklisted.
            You will have access to basic commands. Feel free to roam around.
            To complete the module, echo the flag (i.e. `echo flag1`).
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
            0,

            # GID to execute commands with
            0)
