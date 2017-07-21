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
        ['ls', 'cat', 'echo', 'exit'],
        ['/bin/ls','/bin/cat', '/bin/echo'])
    m.input_loop(m.parser_func)

if __name__ == '__main__':
    main()
