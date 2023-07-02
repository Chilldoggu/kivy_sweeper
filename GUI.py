# from kivy.uix.widget import Widget
# from kivy.uix.image import Image
# from kivy.uix.gridlayout import GridLayout
# from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.button import Button

from kivy.properties import ObjectProperty, ListProperty
from kivy.config import Config
from kivy.clock import Clock
from kivymd.app import MDApp

import random
# import time

# TOOD:
# - Lose screen
# - Win screen
# - Timer

Config.set("graphics", "resizable", False)
Config.set("graphics", "width", 1280)
Config.set("graphics", "height", 720)
Config.set("input", "mouse", "mouse,multitouch_on_demand")
Config.write()


class MyError(Exception):
    def __init__(self, message):
        super().__init__(message)


class Characters:
    SAFE = " "
    UNCHECKED = "#"
    MINE = "X"


class Minesweeper:
    # board_size = (col, row)
    def __init__(self, board_size: tuple, difficulty=0.1) -> None:
        self.player_move = 0
        self.board_size = board_size
        self.mine_amount = int(difficulty * self.board_size[0] * self.board_size[1])

        self.create_grid(self.mine_amount)

    def create_grid(self, mine_amount: int) -> None:
        self.logic_structure = []
        # Not used for GUI gameplay, only for console output

        # Make empty grid
        for row in range(self.board_size[1]):
            self.logic_structure.append([])
            for column in range(self.board_size[0]):
                self.logic_structure[row].append(Characters.SAFE)

        # Populate empty grid with mines
        while mine_amount:
            row = random.choice(range(self.board_size[1]))
            column = random.choice(range(self.board_size[0]))
            if self.logic_structure[row][column] == Characters.SAFE:
                self.logic_structure[row][column] = Characters.MINE
                mine_amount -= 1
        # Populate grid with number indicators
        self._spawn_mine_counters()

    def _calc_outer_square(self, row, column) -> int:
        counter = 0
        for y in range(-1, 2):
            for x in range(-1, 2):
                new_y = row - y
                new_x = column - x
                counter += (
                    1
                    if (
                        new_y in range(self.board_size[1])
                        and new_x in range(self.board_size[0])
                        and self.logic_structure[new_y][new_x] == Characters.MINE
                    )
                    else 0
                )
        return counter

    def _spawn_mine_counters(self):
        for row in range(self.board_size[1]):
            for column in range(self.board_size[0]):
                if self.logic_structure[row][column] == Characters.MINE:
                    continue
                else:
                    self.logic_structure[row][column] = str(
                        self._calc_outer_square(row, column)
                    )


class GameplaySquare(ScreenManager):
    btnWidgetObj = ObjectProperty(None)
    imgWidgetObj = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(GameplaySquare, self).__init__(**kwargs)
        self.transition = FadeTransition()

    def set_img_source(self, src: str):
        self.imgWidgetObj.children[0].source = src


class GameplaySquareButton(Screen):
    squareBtnObj = ObjectProperty(None)

    def on_left_click(self):
        # Give out the coordinates of a button in a grid to a Game.check_square()
        for widget in self.manager.parent.walk_reverse():
            if widget.__class__.__name__ == "Game":
                [
                    widget.check_square([y, row.index(self.manager)])
                    for y, row in enumerate(widget.ButtonList)
                    if self.manager in row
                ]


class InnerGameplaySquareButton(Button):
    flag = False

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos) and touch.grab_current is self:
            if touch.button == "right":
                if self.flag:
                    self.background_normal = 'button_normal.png'
                    self.background_down = 'button_down.png'
                else:
                    self.background_normal = 'button_flag.png'
                    self.background_down = 'button_flag.png'
                self.flag = not self.flag
            elif touch.button == "left" and not self.flag:
                self.parent.on_left_click()
        return super(Button, self).on_touch_up(touch)


class GameplaySquareImage(Screen):
    def on_left_click(self):
        for widget in self.manager.parent.walk_reverse():
            if widget.__class__.__name__ == "Game":
                [
                    widget.combo_reveal([y, row.index(self.manager)]) for y, row in enumerate(widget.ButtonList) if self.manager in row
                ]

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            if touch.button == "right":
                ...
            elif touch.button == "left":
                self.on_left_click()
        return super(Screen, self).on_touch_up(touch)


class Game(Screen):
    gameplayGridObj = ObjectProperty(None)
    gameplaySquareObj = ObjectProperty(None)
    ButtonList = ListProperty(None)
    mineSweeperObj = ObjectProperty(Minesweeper(board_size=(12, 10)))

    def __init__(self, **kw):
        super(Game, self).__init__(**kw)
        Clock.schedule_once(lambda dt: self.make_grid())

    def make_grid(self):
        self.gameplayGridObj.clear_widgets()
        self.ButtonList = []

        # Show the logic structure of the gamefield
        for row in self.mineSweeperObj.logic_structure:
            print(row)

        # Set up the GUI grid with buttons and proper images (1, 2, mine, etc...)
        for i in range(self.gameplayGridObj.rows):
            self.ButtonList.append([])
            for j in range(self.gameplayGridObj.cols):
                gameplaySquareObj = GameplaySquare()
                squareMark = self.mineSweeperObj.logic_structure[i][j]
                gameplaySquareObj.set_img_source(squareMark + ".png")
                self.ButtonList[i].append(gameplaySquareObj)
                self.gameplayGridObj.add_widget(gameplaySquareObj)

    def check_square(self, cords, recursion=True):
        y = cords[0]
        x = cords[1]
        current_mark = self.ButtonList[y][x].imgWidgetObj.children[0].source[:-4]
        self.ButtonList[y][x].current = "image"

        if current_mark == "X":
            # Restart grid if first move is a mine
            if self.mineSweeperObj.player_move == 1:
                self.mineSweeperObj.player_move = 0
                self.mineSweeperObj.create_grid(self.mineSweeperObj.mine_amount)
                return self.check_square(cords)
            else:
                print("YOU LOST")
        # Start recursion to open big empty spaces
        if current_mark == "0" and recursion:
            self.uncheck_outer_square(y, x)

    def uncheck_outer_square(self, row, column, flag_search=False) -> bool:
        for loop_y in range(-1, 2):
            for loop_x in range(-1, 2):
                out_y = row + loop_y
                out_x = column + loop_x
                if out_y in range(self.mineSweeperObj.board_size[1]) and out_x in range(self.mineSweeperObj.board_size[0]):
                    squareObj = self.ButtonList[out_y][out_x]
                    # Not flag_search mode: If in the outer square there is a 0 do recursion else reveal value
                    # Flag_search mode: If a button is a flag then return true
                    if squareObj.current == "button" and \
                            not squareObj.get_screen('button').children[0].flag and \
                            not flag_search:
                        squareObj.current = "image"
                        self.check_square(cords=[out_y, out_x])
                        if squareObj.imgWidgetObj.children[0].source == "0.png":
                            self.uncheck_outer_square(out_y, out_x)
                    if squareObj.current == "button" and flag_search and squareObj.get_screen('button').children[0].flag:
                        return True
        return False

    def combo_reveal(self, cords):
        y = cords[0]
        x = cords[1]
        if not self.uncheck_outer_square(y, x, flag_search=True):
            return None
        self.uncheck_outer_square(y, x)


class Menu(Screen):
    ...


class MineSweeperScreenManager(ScreenManager):
    ...


class MineSweeperApp(MDApp):
    def build(self):
        mineSweeperApp = MineSweeperScreenManager()
        Clock.schedule_interval(self.movingWindowTitle, 0.2)
        return mineSweeperApp

    def movingWindowTitle(self, dt):
        full_title = self.__class__.__name__[:-3]
        if self.get_application_name() == full_title:
            self.title = "M"
        else:
            self.title += full_title[len(self.title)]


if __name__ == "__main__":
    mineSweeper = MineSweeperApp()
    mineSweeper.run()
