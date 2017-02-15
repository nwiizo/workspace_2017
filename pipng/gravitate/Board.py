#!/usr/bin/env python3
# Copyright © 2012-13 Qtrac Ltd. All rights reserved.
# This program or module is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version. It is provided for
# educational purposes and is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.

import collections
import heapq
import math
import random
import tkinter as tk
import tkinter.messagebox as messagebox
from Globals import *

# Need to allow for them to be darkened/lightened for 3D shadow.
COLORS = [
    "#7F0000", # Red
    "#007F00", # Green
    "#00007F", # Blue
    "#007F7F", # Cyan
    "#7F007F", # Magenta
    "#7F7F00", # Yellow
    "#A0A0A4", # Gray
    "#A52A2A", # Brown
    ]
DEF_COLUMNS = 9
MIN_COLUMNS = 5
MAX_COLUMNS = 30
DEF_ROWS = 9
MIN_ROWS = 5
MAX_ROWS = 30
DEF_MAX_COLORS = 4
MIN_MAX_COLORS = 2
MAX_MAX_COLORS = len(COLORS)


class Board(tk.Canvas):

    def __init__(self, master, set_status_text, scoreText,
            columns=DEF_COLUMNS, rows=DEF_ROWS, maxColors=DEF_MAX_COLORS,
            delay=500, size=40, outline="#DFDFDF"):
        self.columns = columns
        self.rows = rows
        self.maxColors = maxColors
        self.delay = delay
        self.outline = outline
        self.size = size
        self.set_status_text = set_status_text
        self.scoreText = scoreText
        self.score = 0
        self.highScore = 0
        super().__init__(master, width=self.columns * self.size,
                height=self.rows * self.size)
        self.pack(fill=tk.BOTH, expand=True)
        self.bind("<ButtonRelease>", self._click)
        self.new_game()


    def new_game(self, event=None):
        self.score = 0
        random.shuffle(COLORS)
        colors = COLORS[:self.maxColors]
        self.tiles = []
        for x in range(self.columns):
            self.tiles.append([])
            for y in range(self.rows):
                self.tiles[x].append(random.choice(colors))
        self._draw()
        self.update_score()


    def _draw(self, *args):
        self.delete("all")
        self.config(width=self.columns * self.size,
                height=self.rows * self.size)
        for x in range(self.columns):
            x0 = x * self.size
            x1 = x0 + self.size
            for y in range(self.rows):
                y0 = y * self.size
                y1 = y0 + self.size
                self._draw_square(self.size, x0, y0, x1, y1,
                        self.tiles[x][y], self.outline)
        self.update()


    # |\__t__/|
    # |l| m |r|
    # |/-----\|
    # ----b----
    #
    def _draw_square(self, size, x0, y0, x1, y1, color, outline):
        if color is None:
            light, color, dark = (outline,) * 3
        else:
            light, color, dark = self._three_colors(color)
        offset = 4
        self.create_polygon( # top
                x0,          y0,
                x0 + offset, y0 + offset,
                x1 - offset, y0 + offset,
                x1,          y0,
                fill=light, outline=light)
        self.create_polygon( # left
                x0,          y0,
                x0,          y1,
                x0 + offset, y1 - offset,
                x0 + offset, y0 + offset,
                fill=light, outline=light)
        self.create_polygon( # right
                x1 - offset, y0 + offset,
                x1,          y0,
                x1,          y1,
                x1 - offset, y1 - offset,
                fill=dark, outline=dark)
        self.create_polygon( # bottom
                x0,          y1,
                x0 + offset, y1 - offset,
                x1 - offset, y1 - offset,
                x1,          y1,
                fill=dark, outline=dark)
        self.create_rectangle( # middle
                x0 + offset, y0 + offset,
                x1 - offset, y1 - offset,
                fill=color, outline=color)


    def _three_colors(self, color):
        r, g, b = self.winfo_rgb(color)
        color = "#{:04X}{:04X}{:04X}".format(r, g, b)
        dark = "#{:04X}{:04X}{:04X}".format(max(0, int(r * 0.5)),
                max(0, int(g * 0.5)), max(0, int(b * 0.5)))
        light = "#{:04X}{:04X}{:04X}".format(min(0xFFFF, int(r * 1.5)),
                min(0xFFFF, int(g * 1.5)), min(0xFFFF, int(b * 1.5)))
        return light, color, dark


    def _click(self, event):
        x = event.x // self.size
        y = event.y // self.size
        color = self.tiles[x][y]
        if color is None or not self._is_legal(x, y, color):
            return
        self._dim_adjoining(x, y, color)


    def _is_legal(self, x, y, color):
        """A legal click is on a colored tile that is adjacent to
        another tile of the same color."""
        if x > 0 and self.tiles[x - 1][y] == color:
            return True
        if x + 1 < self.columns and self.tiles[x + 1][y] == color:
            return True
        if y > 0 and self.tiles[x][y - 1] == color:
            return True
        if y + 1 < self.rows and self.tiles[x][y + 1] == color:
            return True
        return False


    def _dim_adjoining(self, x, y, color):
        adjoining = set()
        self._populate_adjoining(x, y, color, adjoining)
        self.score += len(adjoining) ** (self.maxColors - 2)
        for x, y in adjoining:
            self.tiles[x][y] = "#F0F0F0"
        self._draw()
        self.after(self.delay, lambda: self._delete_adjoining(adjoining))


    def _populate_adjoining(self, x, y, color, adjoining):
        if not ((0 <= x < self.columns) and (0 <= y < self.rows)):
            return # Fallen off an edge
        if (x, y) in adjoining or self.tiles[x][y] != color:
            return # Color doesn't match or already done
        adjoining.add((x, y))
        self._populate_adjoining(x - 1, y, color, adjoining)
        self._populate_adjoining(x + 1, y, color, adjoining)
        self._populate_adjoining(x, y - 1, color, adjoining)
        self._populate_adjoining(x, y + 1, color, adjoining)


    def _delete_adjoining(self, adjoining):
        for x, y in adjoining:
            self.tiles[x][y] = None
        self._draw()
        self.after(self.delay, self._close_up)


    def _close_up(self):
        self._move()
        self._draw()
        self._check_game_over()


    def _move(self):
        moved = True
        while moved:
            moved = False
            for x in range(self.columns):
                for y in range(self.rows):
                    if self.tiles[x][y] is not None:
                        if self._move_if_possible(x, y):
                            moved = True
                            break


    def _move_if_possible(self, x, y):
        empty_neighbours = self._empty_neighbours(x, y)
        if empty_neighbours:
            move, nx, ny = self._nearest_to_middle(x, y, empty_neighbours)
            if move:
                self.tiles[nx][ny] = self.tiles[x][y]
                self.tiles[x][y] = None
                return True
        return False


    def _empty_neighbours(self, x, y):
        neighbours = set()
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if (0 <= nx < self.columns and 0 <= ny < self.rows and
                self.tiles[nx][ny] is None):
                neighbours.add((nx, ny))
        return neighbours


    def _nearest_to_middle(self, x, y, empty_neighbours):
        color = self.tiles[x][y]
        midX = self.columns // 2
        midY = self.rows // 2
        Δold = math.hypot(midX - x, midY - y)
        heap = []
        for nx, ny in empty_neighbours:
            if self._is_square(nx, ny):
                Δnew = math.hypot(midX - nx, midY - ny)
                if self._is_legal(nx, ny, color):
                    Δnew -= 0.1 # Make same colors slightly attractive
                heapq.heappush(heap, (Δnew, nx, ny))
        Δnew, nx, ny = heap[0]
        return (True, nx, ny) if Δold > Δnew else (False, x, y)


    def _is_square(self, x, y):
        if x > 0 and self.tiles[x - 1][y] is not None:
            return True
        if x + 1 < self.columns and self.tiles[x + 1][y] is not None:
            return True
        if y > 0 and self.tiles[x][y - 1] is not None:
            return True
        if y + 1 < self.rows and self.tiles[x][y + 1] is not None:
            return True
        return False


    def _check_game_over(self):
        userWon, canMove = self._check_tiles()
        title = message = None
        if userWon:
            title, message = self._user_won()
        elif not canMove:
            title = "Game Over"
            message = "Game over with a score of {:,}.".format(
                    self.score)
        if title is not None:
            messagebox.showinfo("{} — {}".format(title, APPNAME), message,
                    parent=self)
            self.new_game()
        else:
            self.update_score()


    def _check_tiles(self):
        countForColor = collections.defaultdict(int)
        userWon = True 
        canMove = False
        for x in range(self.columns):
            for y in range(self.rows):
                color = self.tiles[x][y]
                if color is not None:
                    countForColor[color] += 1
                    userWon = False
                    if self._is_legal(x, y, color): # We _can_ move
                        canMove = True
        if 1 in countForColor.values():
            canMove = False
        return userWon, canMove


    def _user_won(self):
        title = "Winner!"
        message = "You won with a score of {:,}.".format(self.score)
        if self.score > self.highScore:
            self.highScore = self.score
            message += "\nThat's a new high score!"
        return title, message


    def update_score(self):
        self.scoreText.set("{:,} ({:,})".format(self.score,
                self.highScore))


if __name__ == "__main__":
    import sys
    if sys.stdout.isatty():
        application = tk.Tk()
        application.title("Board")
        scoreText = tk.StringVar()
        board = Board(application, print, scoreText)
        application.mainloop()
    else:
        print("Loaded OK")
