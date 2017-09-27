# Pydoku

A simple sudoku puzzle solver that reads puzzles from the file provided in the Project Euler problem \#96. In order to solve the puzzles, it first performs an intelligent elimination of potential combinations using the rules of sudoku. This first pass is usually enough to solve beginner level sudoku puzzles, but for many more difficult puzzles it will not be sufficient


## Installation and Use

Pydoku has no pre-requisites besides python 2.7 itself

In order to get started, simply enter the following commands into your terminal

```
$ git clone https://github.com/austinphilp/Pydoku
$ md Pydoku
$ python pydoku.py 1
```

The argument passed into the program represents which puzzle in the file you would like to solve, you may enter any number between 1 and 50


