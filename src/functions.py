# check sudo
def check_sudo():
    from sys import platform as _platform
    if _platform == "linux" or _platform == "linux2":
        # Linux
        import os
        if os.getuid() != 0:
            raise RuntimeError("\n\nYou need to run this script with sudo!")
    #elif _platform == "darwin":
        # MAC OS X
    #elif _platform == "win32":
        # Windows
