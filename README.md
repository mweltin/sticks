# Sticks 
### A Q-learning example

The goal of this repository is to create an environment where a computer 
program learns how to play and hopefully win (or at least not lose) at the game of sticks. The rules of the game are
summed up nicely [here](https://frugalfun4boys.com/play-sticks-finger-game-kids/).

The learning method this program uses is called Q-Learning.  For an explanation on 
Q-learning checkout this [playlist](https://www.youtube.com/playlist?list=PLZbbT5o_s2xoWNVdDudn51XM8lOuZ_Njv) 
by the awesome folks at DeepLizard.  I have no connection to Deeplizard at all. I'm not getting a kickback or anything.
I just think they are great and produce very high quality content. 

###Requirements:
 - python 3
 - coverage 5.5
 - numpy 1.21.2

###Installation:
I'll assume you have a python 3 environment and have already cloned this repo. 
Enter into the repository and install the requirements.

```pip install -r requirements.txt```

### Q-learning
To run the Q-Learning algorithm enter into sticks/qlearning directory and run the following command
```python qlearning.py```
The output from this program is a file called q_table.csv.  This file holds the information the algorithm "learned"

### Playing the game
Assuming the installation and Q-learning instructions above were followed you are now ready to play the game. To 
start the game run the following command from the repository's root directory.

```python main.py```

Then follow the instructions in the console.  Yes the UI is horrible, but I'm working on that. 

### Unit tests
To run tests use unittest from the tests directory
$ python -m unittest

For code coverage run coverage and then reports
$ coverage run -m unittest
$ coverage report

### Docker
Build it yourself

```docker build -t {add your tag name}```

run it

```docker run -d -p 8000:8000 --name sticks {your tag}```

Grab it from dockerhub (not up yet) mweltin/sticks:latest