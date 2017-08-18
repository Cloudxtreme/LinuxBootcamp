"""
This is the main entry point for bootcamp.
It will display a list of modules, and 
allow a user to choose what module to play.

Once a module is completed, the user will be
reprompted with the module selection list.
"""
#from modules import Sample_Module
import modules

try:
    input = raw_input
except NameError:
    pass


def prompt(mods):
    print("\nWelcome to the bootcamp. Select a module.\n")

    for idx, mod in enumerate(mods):
        mods[idx] = mods[idx].create()
        print("\t{}\t{}".format(idx, mods[idx].title))
    
    try:
        mod = int(input("\n\nModule: "))
        if mod < len(mods) and mod >= 0:
            m = mods[mod]
            m.initialize()
            m.start()
    except Exception as e:
        print(e)
        print("Error occured.")

def main():
    mods = []

    for name in dir(modules):
        try:
            m = getattr(modules, name)
            if name != 'module' and isinstance(m, __builtins__.__class__):
                mods.append(m)
        except Exception as e:
            print(e)
    
    while True:
        prompt(mods)
    


if __name__ == '__main__':
    main()
