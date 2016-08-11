#!/bin/bash

## Import our functions
source module_func
source health_tracker

## Configuration
INIT_DIR=""
NAME="BootCamp_Level01"
MAL_PID=""

## Flags
FLAG_ONE="Insert Flag"
FLAG_TWO="Insert Flag"
FLAG_THREE="Insert Flag"
FLAG_FOUR="Insert Flag"
FLAG_FIVE="Insert Flag"

cleanup () 
{
    echo "Cleaning up..."
    kill -9 $MAL_PID
    rm -f "$INIT_DIR/$NAME/notmalware.pid"
    rm -f "$INIT_DIR/$NAME/etc/.flag"
    rm -rf "$INIT_DIR/$NAME/etc/*"
    rmdir "$INIT_DIR/$NAME/etc"
    rmdir "$INIT_DIR/$NAME"
}

function init ()
{
    ## Clear the screen
    clear
    echo "Loading level..."

    ## Store this directory for cleanup later
    INIT_DIR="$(pwd)"

    ## Create the level's files
    mkdir "$NAME"
    mkdir "$NAME/etc"
    touch "$NAME/etc/.flag"
    for i in {1..250}; do 
        echo ".flag will never be revealed to a plebian like you!" >> "$NAME/etc/.flag"
    done
    echo "The flag is $FLAG_ONE" >> "$NAME/etc/.flag"
    for i in {1..250}; do 
        echo ".flag will never be revealed to a plebian like you!" >> "$NAME/etc/.flag"
    done
    touch "$NAME/etc/.flag2"
    chmod 700 "$NAME/etc/.flag2"
    populate_dir "$NAME/etc"
    populate_dir "$NAME/etc/src"
    populate_dir "$NAME/etc/files"
    populate_dir "$NAME/etc/configs"
    populate_dir "$NAME/etc/confidential"

    ## Change into the levels top directory
    cd BootCamp_Level01

    ## Start the level.
    basic_commands
}

function basic_commands () 
{
    echo -e "Welcome to the basic commands tutorial maggot! Type 'exit' to quit, or type 'man <INSERT COMMAND>' for more information on a command.\n"
    validate "pwd" "*Slowly drifts awake* Where are we?! Use the command 'pwd' to print the current working directory."
    validate "ls" "I wonder how we got here, but there's no time for that soldier! Quick, use the command 'ls' to look around."
    validate "cd etc" "Alright, we have to get out of here. See that directory down there? Let's make a jump for it. Use 'cd etc' to change your working directory to etc."
    cd etc > /dev/null 2>&1  
    validate "pwd" "Okay, let's make sure it worked. Where are we soldier?"
    validate "ls" "Let's look around and see what we can find in here."
    validate "ls -l" "Damn, more files than I expected. Here's a trick, use the command 'ls -l' to list files in a directory and display it in a list format."
    validate "ls -a" "Something doesn't seem right about this place, I think there may be something hidden here. Use the command 'ls -a' to list ALL files."
    echo "I knew it! Files beginning with a '.' are hidden by default."
    validate "cat .flag" "Let's see what's in this baby, use the command 'cat .flag' to print the contents of .flag to the screen"
    
    echo -e "\nWow that's a big file. Soldier I think it's time you step it up and learn some command line fu."
    echo -e "The command line operator '|' sends the output of the command/operand on the left as the input for the command on the right."
    echo -e "The command 'grep' allows you to filter input based on a regex expression. Study up soldier! After this tutorial, type 'man grep' into the command line to learn more."
    echo -e "\nAlright soldier, enough playing around! This war ain't gunna fight itself."
    validate "cat .flag | grep -v plebian" "Use the command cat .flag | grep -v plebian to filter out any line containing the word 'plebian'."
    echo -e "Good work, be sure to write down the flag!"
    validate "cat .flag2" "Now there was that other flag somewhere, ah yes .flag2. Let's see what's in that one."
    validate "ls -al" "Strange, normally I'd have access to this sort of thing. Let's check the permissions on it, it should show up in the listed format. (Remember that it's hidden)"
    echo -e "Well that would explain it, and I don't have root on this system. We'll have to figure this out later maggot.\n"
    validate "whoami" "Sometimes I don't like to admit it, but I don't even know who I am anymore. Type the command 'whoami' to figure it out."
    
    sleep 2
    bash "$INIT_DIR/notmalware.sh" &
    MAL_PID=$(cat "$INIT_DIR/$NAME/notmalware.pid")
    echo "#$FLAG_THREE" >> "$INIT_DIR/notmalware.sh"
    lose_health
    read -p '' TEMP

    validate "ps" "WHOA. Get down maggot! Did you hear that?! We aren't alone here anymore! Let's figure out what's going on, use the command 'ps' to see what's running."
    validate "netstat" "Interesting. Let's view our network connections. Use the command 'netstat' to view ongoing connection information. (You may want to filter for the PID)"
    #validate "kill $MAL_PID" "Alright, that's definitely some sleeper malware we got. Let's wipe it out. Use the command 'kill $MAL_PID' to kill that process!"
    echo -e "\nWell done maggot, you made it through the first level. But there's much more to learn, and I won't go so easy on you next time!"
    echo -e "Keep looking around and see if you can find anything interesting...\n"
    
    exec_loop
    
    ## If broken out of loop
    echo "Congratulations, you've broken out. Here is your flag: $FLAG_FIVE"
    echo "But get back in there, you're not done yet soldier!"
    
    fixed_exec_loop
    
    cleanup
}

init
