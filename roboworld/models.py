from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class DialogChoice:
    """A single player response option in a dialog node.

    - text: The text the player sees
    - next_id: The id of the next dialog node. If None, the dialog ends.
    - effects: Optional side-effect keys the game interprets (e.g., "gain:station_code").
    """

    text: str
    next_id: Optional[str]
    effects: List[str] = field(default_factory=list)


@dataclass
class DialogNode:
    """A robot dialog node in a directed acyclic graph (DAG)."""

    id: str
    text: str
    choices: List[DialogChoice] = field(default_factory=list)


@dataclass
class Robot:
    """A friendly but malfunctioning robot with a dialog tree."""

    name: str
    dialog: Dict[str, DialogNode]
    start_node: str


@dataclass
class Region:
    """A traversable area within a neighborhood."""

    key: str
    name: str
    description: str
    connections: Dict[str, str]  # direction/name -> region_key
    robots: List[Robot] = field(default_factory=list)
    is_train_station: bool = False
    station_unlocked: bool = False


@dataclass
class Neighborhood:
    """A collection of connected regions and a station to unlock."""

    name: str
    regions: Dict[str, Region]
    station_region_key: str


@dataclass
class City:
    name: str
    neighborhoods: Dict[str, Neighborhood]


@dataclass
class World:
    cities: Dict[str, City]

    # TODO: Teaching hook — Add support for multiple cities and progression.
