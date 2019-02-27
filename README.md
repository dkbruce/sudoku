# Sudoku

Implementation of a traditional game of sudoku.

## Running

Either run 

```python main.py```

from your terminal / command line, or open `main.py` with your Python installation

## Input files

The first row of input files contain four numbers. These numbers, in order, are the number of rows in each box, the number of columns in each box, the number of boxes vertically, and the number of boxes horizontally. Note that we must have that the first number times the third equals the second times the fourth (let these equal n), so that a valid board is created. The next n rows and columns contain the initial numbers for the game. Entries of 0 represent a blank space to be filled in by the player. The player cannot change the entry of any number 1 - 9 in the initial grid.

## Dependencies

Python 3.4.5 or newer.

## Issues

* Typing numbers larger than 9 will not work, so the largest boards that currently work are 3x3.

## Acknowledgement

Thanks to [newcoder](http://newcoder.io/gui/) for the guide. I was not familiar with tkinter beforehand, so most of the front-end code is based on his tutorial.