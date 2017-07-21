"""
"""
from module import Module

import subprocess

def main():
    m = Module(
        'Sample_Module',
        'Bootcamp(Sample Module) > ',
        'Welcome to the Linux Bootcamp.\nInitializing your environment...',
        'flag1',
        ['/bin/ls',
        '/bin/cat',
        '/bin/echo',
        '/usr/bin/touch',
        '/usr/bin/whoami',
        '/usr/bin/stat',
        '/usr/bin/env',
        '/usr/bin/grep',
        '/bin/mkdir',
        '/bin/chmod'
        ])
    m.input_loop(m.parser_func)

if __name__ == '__main__':
    main()
