# SnakePy

SnakePy is simple snake game written in Python using as few libraries as possible (for me).

## Goal

The goal was to use lists in order to represent different entities (ex. tail, fruits) in Python and to easily access and modify the elements game output CLI screen.

I know I could use curses to accomplish the same using less code, but I wanted to learn about list manipulation so I chose the hard way.

## How to run

1) Install the required 'keyboard' module using PIP (run in terminal or CMD if you have Windows):
   ```$ pip3 install keyboard```
   
2) Run the script: ```$ python snake.py``` on Windows or ```$ sudo python3 snake.py``` on GNU/Linux
   (the keyboard module needs root privilages in order to function)

## Fine tune the snake's speed

Depending on the platform, you may want to adjust the ```speed``` variable. In GNU/Linux, it results to a much higher refresh rate which makes the snake move extremely fast.
