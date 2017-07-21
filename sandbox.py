"""
Sandbox module, will be run in an isolated process.
"""
#import subprocess
import os 

def sandbox_exec(cmd):
    #program_output = subprocess.check_output(cmd, shell=True)

    #print(program_output)
    return os.system('echo hi')
