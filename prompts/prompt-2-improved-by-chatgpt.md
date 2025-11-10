# 🤖 Roboworld --- LLM-Ready Game Specification

## Overview

Generate a playable **terminal-based choose-your-own-adventure game in
Python** called **Roboworld**. The game should run with **zero or
minimal external dependencies** (standard library only unless absolutely
necessary).

The code should be **clean, modular, and readable**, and avoid
unnecessary framework complexity. Prioritize **clarity over
performance** because the code will be read and modified by beginner
programmers.

---

## Core Premise

- The player wakes up on an alien world populated by friendly but
  malfunctioning robots.
- Robots have **forgotten parts of their programming**, causing
  infrastructure failures (such as trains that no longer run).
- The player **converses with robots**, learns about their problems,
  and **helps solve them**.
- Fixing robots **restores their memory**, which eventually restores
  the train network.
- Restoring all neighborhoods unlocks cities. Restoring all cities
  enables the game's final success ending.

---

## Game Experience & Rules

### Player Movement

- The world is structured as **Cities → Neighborhoods → Regions**.
- Each neighborhood contains:
  - Multiple **Regions** connected like a graph
    (north/south/east/west or named connections).
  - One **Train Station** region (initially locked).
  - Multiple **Robots** the player can talk to.
  - One **puzzle or core problem** that must be solved to unlock the
    train.
- Players may **backtrack freely to any previously visited region**.
- Unlocking all neighborhoods in a city unlocks the city's central
  station and the next city.

### Player--Robot Conversations

- Robots have **dialog trees stored as Directed Acyclic Graphs
  (DAGs)**.
- Dialog nodes contain:
  - Robot text
  - Player response choices
  - Transitions to next nodes
  - Optional side effects (e.g. unlocking repair progress, modifying
    world state)
- Every dialog must include the option: \> **(X) Exit conversation**
  - This option _never_ causes negative consequences.

### Game Outcomes

- Some decision paths end the story early (neutral or failure
  endings).
- Some lead to bad outcomes that the player can later recover from.
- A small number of paths lead to successful neighborhood repairs.
- The game tracks long-term consequences of dialog choices.

---

## Scale Requirements

Concept Count

---

Cities 4
Neighborhoods per city 4
Total neighborhoods 16
Train Stations 1 per neighborhood (16 total)
Dialog puzzles 1 per neighborhood
Robots 2--4 per region recommended

---

## State the Game Must Track

### World Structure

- Cities → Neighborhoods → Regions → Robots
- Connectivity graph for regions
- Which train stations are unlocked

### Player State

- Current city → neighborhood → region
- Conversation progress per robot
- Completed neighborhood puzzles
- Unlocked train stations

### Robot State

- Name (human-style name)
- Dialog tree DAG
- Current dialog node per player
- Optional flags (e.g. `antenna_fixed = True`)

---

## User Interface Requirements

The game must run entirely in the terminal and support:

1.  **Exploration mode**
    - "Where you are"
    - Connected regions
    - Robots present
    - Whether the train station is operational
2.  **Conversation mode**
    - Shows robot dialog
    - Lists multiple-choice responses as numbered options
    - Includes an exit option
3.  **Input validation**
    - Must not crash if the user enters invalid input
4.  **A clear game loop**
    - Player can move, talk, or quit at any time

---

## Developer Constraints (for Generated Code)

- Use **Python 3.10+**
- **No external dependencies** unless absolutely required
- Avoid large monolithic functions
- Use dataclasses or simple classes for entities (`Robot`, `Region`,
  etc.)
- Keep save/load optional but design state so it _could support it
  later_
- Include comments that explain non-obvious logic
- Use simple in-memory structures (no databases)
- Avoid AI-generated placeholder prose --- dialogs should be minimal
  but meaningful

---

## Deliverables to Generate

1.  **A fully working Python game**
2.  **A clean data model for the world**
3.  **Example content:**
    - 1 city with 1 neighborhood scaffolded
    - At least 2 robots fully implemented with dialog trees
    - 1 puzzle that unlocks a train station
4.  **TODO comments** marking extensible areas for students to expand

---

## Teaching Hooks (Include these in TODOs)

Add code comments that explicitly flag opportunities for students to:

- Add new neighborhoods
- Write new robot personalities
- Expand dialog trees
- Add inventory or player tools
- Improve map navigation
- Add a save system
- Add ASCII art or flavor text

---

### Optional Prompt Questions for the AI (do NOT answer now, leave as comments in code)

Include these as commented prompts in the generated source code:

```python
# Prompt ideas for students:
# 1. "Generate 5 unique robot personalities and dialog trees"
# 2. "Add a puzzle that teaches a basic programming concept"
# 3. "Implement inventory without changing the world model"
```
