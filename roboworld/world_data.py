from __future__ import annotations

from typing import Dict

from .models import City, DialogChoice, DialogNode, Neighborhood, Region, Robot, World

"""Example world content for Roboworld.

Scaffolds 1 city with 1 neighborhood, 3 regions, and 2 robots with dialog
DAGs. Includes a simple station-unlock puzzle that requires learning an
override code from a robot first.

Prompt ideas for students:
    # 1. "Generate 5 unique robot personalities and dialog trees"
    # 2. "Add a puzzle that teaches a basic programming concept"
    # 3. "Implement inventory without changing the world model"
"""


def create_world() -> World:
    """Create the starting world with one city and one neighborhood.

    Structure:
    - Alpha City
      - Central Yard (neighborhood)
        - Square (start)
        - Workshop
        - Station (train station region, initially locked)
        - Robots: Ada (Workshop), Bolt (Square)

    Puzzle: Learn the override code from Ada to unlock the Station.
    """

    # --- Ada's dialog (teaches the station override code) ---
    ada_dialog: Dict[str, DialogNode] = {
        "start": DialogNode(
            id="start",
            text=(
                "Oh! Hello, traveler. I'm Ada. My memory banks are glitching, "
                "but I still remember how the station used to work."
            ),
            choices=[
                DialogChoice(
                    text="Ask about the broken train station.",
                    next_id="station_info",
                ),
                DialogChoice(
                    text="Compliment Ada's diagnostic stickers.",
                    next_id="stickers",
                ),
            ],
        ),
        "stickers": DialogNode(
            id="stickers",
            text=(
                "Thank you! I organize them by checksum. Speaking of... the station "
                "needs an override code after a reboot."
            ),
            choices=[
                DialogChoice(
                    text="Ask about the override code.",
                    next_id="station_info",
                ),
            ],
        ),
        "station_info": DialogNode(
            id="station_info",
            text=(
                "The panel expects an override code. Let me recall... yes! It's 'ORANGE-7'. "
                "That should restore the local line."
            ),
            choices=[
                DialogChoice(
                    text="Memorize 'ORANGE-7'.",
                    next_id=None,  # End of helpful branch
                    effects=["gain:ORANGE-7"],
                ),
            ],
        ),
    }

    ada = Robot(name="Ada", dialog=ada_dialog, start_node="start")

    # --- Bolt's dialog (flavor + hint) ---
    bolt_dialog: Dict[str, DialogNode] = {
        "start": DialogNode(
            id="start",
            text=(
                "Name's Bolt. I've been looping this same patrol. If the station were up, "
                "I'd ride the line for a change of scenery. Maybe Ada remembers how to fix it?"
            ),
            choices=[
                DialogChoice(text="Ask about Ada.", next_id="about_ada"),
                DialogChoice(text="Wish Bolt a good loop.", next_id=None),
            ],
        ),
        "about_ada": DialogNode(
            id="about_ada",
            text=(
                "Ada's precise. If there's a code, she'll know it. I'd talk to her at the Workshop."
            ),
            choices=[
                DialogChoice(text="Thank Bolt.", next_id=None),
            ],
        ),
    }

    bolt = Robot(name="Bolt", dialog=bolt_dialog, start_node="start")

    # --- Regions ---
    square = Region(
        key="square",
        name="Square",
        description="A bright plaza with solar tiles underfoot.",
        connections={"east": "workshop", "south": "station"},
        robots=[bolt],
    )

    workshop = Region(
        key="workshop",
        name="Workshop",
        description="Benches, tools, and a gentle hum of calibration routines.",
        connections={"west": "square"},
        robots=[ada],
    )

    station = Region(
        key="station",
        name="Station",
        description="A compact platform with a flickering status panel.",
        connections={"north": "square"},
        robots=[],
        is_train_station=True,
        station_unlocked=False,
    )

    regions = {r.key: r for r in (square, workshop, station)}

    neighborhood = Neighborhood(
        name="Central Yard",
        regions=regions,
        station_region_key="station",
    )

    city = City(name="Alpha City", neighborhoods={"central_yard": neighborhood})
    world = World(cities={"alpha_city": city})
    return world


# TODO: Teaching hook — Add more neighborhoods and connect them by unlocking city-level transport.
