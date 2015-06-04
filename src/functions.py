# check sudo
def check_sudo():
    import os
    if os.getuid() != 0:
        raise RuntimeError("You need to run this script with sudo!")      
