# Roboworld

A choose-your-own-adventure game

## Plot

The player wakes up to find themselves on a strange alien world populated by
robots. They seem content to execute their programming, except they have
forgotten how to do many things, like how to run the trains.

The player's goal is to speak with the robots and learn from them, and then fix
various problems. When the player solves the robot problems, they remember how
to run the train and the player can progress.

## Style

The game is posed as a choose-your-own-adventure book. The player will be able
to move freely to places they have been before and engage with the robots in any
unlocked area. But to unlock new areas, the player will need to engage with
robots, read what they have to say, and decide what course of action to take.
Some decisions will lead to the story ending early; a few decision paths lead to
a good outcome for everyone; some decision paths lead to bad outcomes.

Decisions are multiple-choice, and have long-term consequences. Players can
always opt to back out of a conversation and return later once they feel ready.

## Neighborhoods, Cities, and Trains

The game world is built from neighborhoods, which form cities. The player must
solve each neighborhood's specific problem to unlock its train station. Once
unlocked the player can go to connected neighborhoods. Once the player has
unlocked each neighborhood, the main train station is unlocked and the player
can travel to a new city.

Each city has four neighborhoods, and there are four cities. This brings us to
16 neighborhoods, each of which has a puzzle to solve. Each neighborhood can
have a number of regions that contains different robots you can talk to. Each
robot will have a short dialog tree that the player navigates by making
decisions about how to respond to each exchange. Robots all have human names.

## Technology

The core game logic is written in Python.

**Important** the game should be playable with minimal external dependencies.

We will need to maintain state about:

- Robots:
  - Name
  - Dialog tree consisting of nodes:
    - The robot's text
    - The available options for the player to choose among
    - Which node each option will open up
  - The player's current state in the dialog tree
- Regions within a neighborhood:
  - Name
  - Which regions are connected (e.g. go west to get to the plaza)
  - Which robots are there
- Neighborhoods:
  - A list of regions - one of which must be a train station
  - The player's progression state within the neighborhood
- City:
  - A list of neighborhoods
- Game world:
  - A list of Cities
- Player:
  - Which region / neighborhood / city they are currently in

## Player-Robot Interaction

When the player engages with a robot, it speaks the text associated with the
player's position in their dialog tree. (The tree is actually a directed acyclic
graph.)

The UI then shows the player the available options with numbers, such as:

(1) Try to repair the robot's antenna
(2) Ask why the antenna is broken
(3) Tell the robot you can't fix them
(4) Pretend to take a phone call (exit conversation)

There should always be an "exit conversation" option, and it always tells you
that is the outcome. There is never a negative consequence to doing this.

All other options have consequences because it updates the player's state with
that robot's dialog tree.
