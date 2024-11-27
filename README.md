# Wordle Solver

This project is an automated Wordle solver that intelligently guesses words until it finds the correct answer. It uses feedback from each guess to refine future guesses, similar to the Wordle game. Refer to the file random_guess.py (wordleAPI.py is just to show the previous work)

## Features

- Automatically guesses words from a provided list.
- Uses feedback to prioritize potential word candidates.
- Prints detailed feedback after each guess.

## Usage

1. **Prerequisites**: Python 3.x and the `requests` library (`pip install requests`).
2. **Word List**: Ensure `nyt-answers.txt` is in the same directory.
3. **Run the Script**: Execute with `python wordle_solver.py`.

## How It Works

- Loads words from `nyt-answers.txt`.
- Makes and refines guesses based on feedback from the Wordle API.

## Resources

Inspired by:
- ChatGPT and Cursor for code development.
- [Pete Haha's Wordle Solver](https://github.com/petehaha/WordleSolver)
- [Josh Stephenson's Wordle Solver](https://github.com/joshstephenson/Wordle-Solver)
- [Bright Mediums Blog](https://www.brightmediums.com/blog/2022/9/1/solving-wordle-with-algorithms)

