"""
This is the main entry point for bootcamp.
It will display a list of modules, and 
allow a user to choose what module to play.

Once a module is completed, the user will be
reprompted with the module selection list.
"""
#from modules import Sample_Module
import modules
import importlib
import copy

def prompt(mods):
    print("\nWelcome to the bootcamp. Select a module.\n")

    for idx, mod in enumerate(mods):
        print("\t{}\t{}".format(idx, mod.title))
    
    try:
        try:
            input = raw_input
        except NameError:
            pass
        
        mod = int(input("\n\nModule: "))
        if mod < len(mods) and mod >= 0:
            m = copy.deepcopy(mods[mod])
            m.initialize()
            m.start()
    except Exception as e:
        print(e)
        print("Error occured.")

def main():
    mods = []

    for name in dir(modules):
        if name.startswith('_'):
            continue
        try:
            m = importlib.import_module("modules.{}".format(name)).create()
            mods.append(m)
        except Exception as e:
            print(e)
    
    while True:
        prompt(mods)
    


if __name__ == '__main__':
    main()
