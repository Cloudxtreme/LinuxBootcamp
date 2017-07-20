"""
"""
from module import Module

def main():
    m = Module('Sample Module', 'Bootcamp(Sample Module) > ', 'flag1', ['ls', 'cat', 'echo', 'exit'])
    m.input_loop(m.parser_func)

if __name__ == '__main__':
    main()
