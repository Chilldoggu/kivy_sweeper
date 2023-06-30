# TOOD:
#   - Zmień cords w game_start() z (x,y) na (y,x)
#       - Upewnij się że nigdzie nie sytępuje błąd z powodu zmiany kolejności koordynatów
#   - Upewnij się że pierwszy ruch jest zawsze bezpieczny
#   - Spraw by dało się przegrać
#   - Dodaj RGB dla wyjścia konsolowego
#   + Dodaj GUI
#       o Możesz dodać anonimowy tytuł okienka: {"M", "Mi", "Min", "Mine", "Mines", "Minesw", "Mineswe", "Mineswee", "Minesweep", "Minesweepe", "Minesweeper"}
#   + Dodaj bota

import random

class MyError(Exception):
    def __init__(self, message):
        super().__init__(message)

class Characters:
    SAFE = " "
    UNCHECKED = u"\u25AA"
    MINE = "X"

class Minesweeper():
    def __init__(self, board_size: tuple, difficulty=0.2) -> None:
        self.player_move = 0
        self.board_size = board_size 
        self.mine_amount = int(difficulty*self.board_size[0]*self.board_size[1]) 

        self.create_grid(self.mine_amount)


    def create_grid(self, mine_amount: int) -> None:
        self.logic_structure = []
        self.player_view = []

        # Make empty grid
        for row in range(self.board_size[1]):
            self.logic_structure.append([])
            self.player_view.append([])
            for column in range(self.board_size[0]):
                self.logic_structure[row].append(Characters.SAFE)
                self.player_view[row].append(Characters.UNCHECKED)

        # Populate empty grid with mines
        while mine_amount:
            row = random.choice(range(self.board_size[1]))
            column = random.choice(range(self.board_size[0]))
            if self.logic_structure[row][column] == Characters.SAFE:
                self.logic_structure[row][column] = Characters.MINE
                mine_amount -= 1
        
        # Populate grid with number indicators
        self._spawn_mine_counters()


    def check_mine(self, cords: list[int]) -> bool:
        y = cords[0] - 1
        x = cords[1] - 1
        if not x in range(self.board_size[0]) or not y in range(self.board_size[1]) or len(cords) != len(self.board_size):
            raise MyError(f"Invalid Cords:\ncords: {cords} are not in range of board_size {self.board_size}")
        elif self.player_view[y][x] == Characters.SAFE:
            return True

        self.player_move += 1
        if self.logic_structure[y][x] == Characters.MINE:
            if self.player_move == 1:
                self.player_move = 0
                self.create_grid(self.mine_amount)
                self.check_mine(cords)
            else:
                self.player_view[y][x] = self.logic_structure[y][x]
                return False
        elif not self.logic_structure[y][x] == "0":
            self.player_view[y][x] = self.logic_structure[y][x]
        else:
            # Start recursion to discover big empty spaces
            self.player_view[y][x] = Characters.SAFE
            self._uncheck_outer_square(y,x)
        return True


    # PRIVATE METHODS
    def _uncheck_outer_square(self, row, column) -> None:
        for loop_y in range(-1, 2):
            for loop_x in range(-1, 2):
                new_y = row+loop_y
                new_x = column+loop_x
                if new_y in range(self.board_size[1]) and new_x in range(self.board_size[0]):
                    # If in the outer square there is a 0 do recursion else just show the value
                    if (not self.player_view[new_y][new_x] == Characters.UNCHECKED):
                        continue
                    elif (not self.logic_structure[new_y][new_x] == "0"):
                        self.player_view[new_y][new_x] = self.logic_structure[new_y][new_x]
                    else:
                        self.player_view[new_y][new_x] = Characters.SAFE
                        self._uncheck_outer_square(new_y, new_x)


    def _calc_outer_square(self, row, column) -> int:
        counter = 0
        for y in range(-1, 2):
            for x in range(-1, 2):
                new_y = row-y
                new_x = column-x
                counter += 1 if (new_y in range(self.board_size[1]) and
                                new_x in range(self.board_size[0]) and
                                self.logic_structure[new_y][new_x] == Characters.MINE) \
                                else 0
        return counter


    def _spawn_mine_counters(self):
        for row in range(self.board_size[1]):
            for column in range(self.board_size[0]):
                if self.logic_structure[row][column] == Characters.MINE:
                    continue
                else:
                    self.logic_structure[row][column] = str(self._calc_outer_square(row, column))


def main():
    pass


if __name__ == "__main__":
    main()
