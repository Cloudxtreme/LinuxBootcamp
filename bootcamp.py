"""
"""
from modules import Sample_Module
import importlib

def main():
    m = Sample_Module()
    m.initialize()
    m.start()

if __name__ == '__main__':
    main()
