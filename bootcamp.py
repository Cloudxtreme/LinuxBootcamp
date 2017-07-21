"""
"""
from module import Module

import subprocess

def main():
    m = Module(
        'Sample Module',
        'Bootcamp(Sample Module) > ',
        'Welcome to the Linux Bootcamp.\nInitializing your environment...',
        'flag1',
        ['ls', 'cat', 'echo', 'exit', 'touch'],
        ['/bin/ls',
        '/bin/cat',
        '/bin/echo',
        '/usr/bin/touch',
        '/usr/bin/whoami',
        '/usr/bin/stat',
        '/usr/bin/env',
        '/usr/bin/grep'
        ])
    m.input_loop(m.parser_func)

if __name__ == '__main__':
    main()
