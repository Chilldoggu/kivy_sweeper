from minesweeper import * 

class bcolors:
    # FANCY
    BACKGROUND = '\x1B[48;5;15m'
    BOLD = '\x1B[1m'
    UNDERLINE = '\x1B[4m'
    # NUMBERS
    JEDEN   = BOLD + BACKGROUND + '\x1B[38;5;21m'
    DWA     = BOLD + BACKGROUND + '\x1B[38;5;40m'
    TRZY    = BOLD + BACKGROUND + '\x1B[38;5;160m'
    CZTERY  = BOLD + BACKGROUND + '\x1B[38;5;18m'
    PIEC    = BOLD + BACKGROUND + '\x1B[38;5;125m'
    SZESC   = BOLD + BACKGROUND + '\x1B[38;5;30m'
    SIEDIEM = BOLD + BACKGROUND + '\x1B[38;5;92m'
    OSIEM   = BOLD + BACKGROUND + '\x1B[38;5;207m'
    # GENERAL
    UNCHECKED = BOLD + BACKGROUND + '\x1B[38;5;236m'
    MINE = BOLD + BACKGROUND + '\x1B[38;5;232m'
    FAIL = UNDERLINE + '\x1B[38;5;196m' 
    # ALWAYS END STRING WITH THIS
    ENDC = '\x1B[0m'


class ConsoleSweeper():
    def __init__(self, **kwargs) -> None:
        self.minesweeper_backend = Minesweeper(board_size=kwargs["board_size"])


    def start_game(self) -> None:
        while True:
            self.draw_player_view()
            cords = [int(i) for i in list(input("Choose square: ").split(","))]
            if mine_sweep := self.minesweeper_backend.check_mine(cords):
                continue
            else:
                self.draw_player_view()
                print(f"{bcolors.FAIL}YOU LOST!\nYOU WERE ON MOVE {self.minesweeper_backend.player_move}{bcolors.ENDC}")
                break


    def draw_player_view(self) -> None:
        # SHOW COLORING SCHEME
        print(f"{bcolors.JEDEN}1{bcolors.ENDC} {bcolors.DWA}2{bcolors.ENDC} {bcolors.TRZY}3{bcolors.ENDC} {bcolors.CZTERY}4{bcolors.ENDC} {bcolors.PIEC}5{bcolors.ENDC} {bcolors.SZESC}6{bcolors.ENDC} {bcolors.SIEDIEM}7{bcolors.ENDC} {bcolors.OSIEM}8{bcolors.ENDC} {bcolors.MINE}#{bcolors.ENDC} {bcolors.FAIL}YOU HAVE FAILED{bcolors.ENDC}")

        for row in range(self.minesweeper_backend.board_size[1]):
            print(f"{bcolors.BACKGROUND}+---"*self.minesweeper_backend.board_size[0]+"+", end=f"{bcolors.ENDC}\n")
            for column in range(self.minesweeper_backend.board_size[0]):

                print(f"{bcolors.BACKGROUND}| ", end=f"{bcolors.ENDC}")
                match self.minesweeper_backend.player_view[row][column]:
                    case " ":
                        print(bcolors.BACKGROUND, end="")
                    case u"\u25AA":
                        print(bcolors.UNCHECKED, end="")
                    case "X":
                        print(bcolors.MINE, end="")
                    case "1":
                        print(bcolors.JEDEN, end="")
                    case "2":
                        print(bcolors.DWA, end="")
                    case "3":
                        print(bcolors.TRZY, end="")
                    case "4":
                        print(bcolors.CZTERY, end="")
                    case "5":
                        print(bcolors.PIEC, end="")
                    case "6":
                        print(bcolors.SZESC, end="")
                    case "7":
                        print(bcolors.SIEDIEM, end="")
                    case "8":
                        print(bcolors.OSIEM, end="")
                    case _:
                        MyError(f"{bcolors.ENDC}Unknow player view character: {self.minesweeper_backend.player_view[row][column]}")

                print(f"{self.minesweeper_backend.player_view[row][column]}{bcolors.ENDC}{bcolors.BACKGROUND} ", end=f"{bcolors.ENDC}")
            print(f"{bcolors.BACKGROUND}|{bcolors.ENDC}")
        print(f"{bcolors.BACKGROUND}+---"*self.minesweeper_backend.board_size[0]+"+", end=f"{bcolors.ENDC}\n")


    def draw_logic_structure(self) -> None:
        for row in range(self.minesweeper_backend.board_size[1]):
            print("+---"*self.minesweeper_backend.board_size[0]+"+")
            for column in range(self.minesweeper_backend.board_size[0]):
                print(f"| {self.minesweeper_backend.logic_structure[row][column]} ", end="")
            print("|")
        print("+---"*self.minesweeper_backend.board_size[0]+"+")


if __name__ == "__main__":
    game = ConsoleSweeper(board_size=(5,5))
    game.start_game()