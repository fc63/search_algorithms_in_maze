# Visualization of Search Algorithms with Random Costs in a Maze (With Pygame)

![Preview](/preview.png)
<br>
<br>

##  **Breadth First Search,** **Depth First Search,** **Uniform Cost Search** **and** **A_star Search (Euclidean and Manhattan)** in **Python** using **Pygame**! 👓

Forked from [maxontech](https://github.com/MaxRohowsky)

## Table of contents

- [Description](#description)
- [YouTube Tutorial](#youtube-tutorial)
- [Installation](#installation)
- [Controls](#controls)
- [Libraries](#libraries)
- [FAQ](#faq)

## Description

This is a visual implementation of the **Breadth First Search,** **Depth First Search,** and **Uniform Cost Search** algorithm.

You can manually draw walls, and the algorithm will find the path from the start to the end.

## YouTube Videos

Max Rohowsky's YouTube introductory video for the version I forked that only included breadth first search:

[Python Pathfinding Vizualisation](https://www.youtube.com/watch?v=QNpUN8gBeLY)

## Installation
Requirements: You must have [Python](https://www.python.org/downloads/) installed and preferably a code editor like [PyCharm](https://www.jetbrains.com/pycharm/download/).

1. Clone the repository 
2. In the terminal, navigate to the directory where the repository was cloned, e.g., `C:\Users\Max\PycharmProjects\breadth-first-search-algorithm`
3. Create a virtual environment, activate it, and install pygame by running the following commands in the terminal:
    ```bash
    python -m venv venv #This creates a virtual environment
    venv\Scripts\activate #This activates the virtual environment
    pip install -r requirements.txt #This installs the required libraries
    ```
4. Run the game by running the following command in the terminal:
    ```bash
    python pathfinding.py
    ```

## Controls
- Left mouse to draw walls
- Right mouse to set target point
- R to Determines Random Cost for each box
- 1 to start the Breadth First Search
- 2 to start the Depth First Search
- 3 to start the Uniform Cost Search
- 4 to start the A* Search with Manhattan Distance
- 5 to start the A* Search with Euclidean Distance

## Libraries

- [pygame](https://www.pygame.org/news): Pygame is a cross-platform set of Python modules designed for writing video games.

## FAQ
- How to Open GitHub Projects in PyCharm? [Explained Here](https://youtu.be/cAnWazo5pFU)
- How to use Virtual Environments? [Explained Here](https://youtu.be/2P30W3TN4nI)
- How to install PyCharm and Python? [Explained Here](https://youtu.be/XsL8JDkH-ec)
- How to set PyCharm Config. and Interpreter? [Explained Here](https://youtu.be/OajNS-WHiUI)
