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

def prompt(mods):
    print("Welcome to the bootcamp. Select a module.\n")
    for i in range(0, len(mods)):
        print("\t{}\t{}".format(i, mods[i].title))
    
    mod = int(raw_input("\n\nModule: "))
    mods[mod].initialize()
    mods[mod].start()

def main():
    mods = []

    for name in dir(modules):
        if name.startswith('_'):
            continue
        try:
            m = importlib.import_module("modules.{}".format(name)).create()
            mods.append(m)
        except Exception as e:
            pass
    
    while True:
        prompt(mods)
    


if __name__ == '__main__':
    main()
