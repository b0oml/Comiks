'''
Colors for Linux terminal.

Usage :
    from colors import *

    print(BLUE + "Blue string" + RST)
    print(RED + BOLD + "Bold red string" + RST)
'''

# Colors
DEFAULT = '\033[39m'  # Default foreground color
WHITE   = '\033[97m'
BLACK   = '\033[30m'
RED     = '\033[31m'
GREEN   = '\033[32m'
YELLOW  = '\033[33m'
BLUE    = '\033[34m'
MAGENTA = '\033[35m'
CYAN    = '\033[36m'

DEFAULT = '\033[49m'  # Default background color
BG_WHITE   = '\033[107m'
BG_BLACK   = '\033[40m'
BG_RED     = '\033[41m'
BG_GREEN   = '\033[42m'
BG_YELLOW  = '\033[43m'
BG_BLUE    = '\033[44m'
BG_MAGENTA = '\033[45m'
BG_CYAN    = '\033[46m'

# Light and dark colors
LIGHT_GRAY      = '\033[37m'
DARK_GRAY       = '\033[90m'
DARK_RED        = '\033[91m'
LIGHT_GREEN     = '\033[92m'
LIGHT_YELLOW    = '\033[93m'
LIGHT_BLUE      = '\033[94m'
LIGHT_MAGENTA   = '\033[95m'
LIGHT_CYAN      = '\033[96m'

# Other styles
BOLD        = '\033[1m'
DIM         = '\033[2m'
UNDERLINED  = '\033[4m'

# Reset all styles
RST = "\033[0m"
