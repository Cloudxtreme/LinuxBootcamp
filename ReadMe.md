This program runs a sandbox environment for users, giving them a guided approach to learning Linux and security.


    sudo dnf install python-devel
    pip install -r requirements.txt

    # If not in virtual env
    sudo python bootcamp.py

    # Otherwise
    sudo `which python` bootcamp.py

Execution requires root because the sandbox is in a chroot.
