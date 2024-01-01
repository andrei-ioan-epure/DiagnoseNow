import os
import sys

from DempsterShafer import DempsterShafer
from ui.UserInterface import UserInterface

if __name__ == "__main__":
    ui = UserInterface(sys.argv, os.path.join(os.getcwd(), 'ui/user-interface.ui'))
    sys.exit(ui.start())
