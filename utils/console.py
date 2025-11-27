from utils.colours import Colour

ANSI_MAP = {
    Colour.RED: "\033[31m",
    Colour.GREEN: "\033[32m",
    Colour.YELLOW: "\033[33m",
    Colour.BLUE: "\033[34m",
}

RESET = "\033[0m"

def log(text: str, colour: Colour = None):
    if colour and colour in ANSI_MAP:
        print(f"{ANSI_MAP[colour]}{text}{RESET}")
    else:
        print(text)
