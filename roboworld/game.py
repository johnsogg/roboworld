from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

from .models import DialogNode, Neighborhood, Region, Robot, World
from .world_data import create_world

"""Main game loop for Roboworld.

Implements exploration and conversation modes with simple input
validation. This is intentionally minimal and beginner-friendly.

TODO (teaching hook):
    - Add save/load of world + player state.
    - Add inventory and item-based puzzles.
    - Add additional neighborhoods and train travel.
    - Add ASCII art for regions / robots.
"""


@dataclass
class PlayerState:
    city_key: str
    neighborhood_key: str
    region_key: str
    known_codes: set[str]


class Game:
    def __init__(self) -> None:
        self.world: World = create_world()
        # Start in the only city/neighborhood/region available.
        self.player = PlayerState(
            city_key="alpha_city",
            neighborhood_key="central_yard",
            region_key="square",
            known_codes=set(),
        )

    # ------------- Utility lookups -------------
    def current_city(self):
        return self.world.cities[self.player.city_key]

    def current_neighborhood(self) -> Neighborhood:
        return self.current_city().neighborhoods[self.player.neighborhood_key]

    def current_region(self) -> Region:
        return self.current_neighborhood().regions[self.player.region_key]

    # ------------- Exploration Mode -------------
    def show_exploration(self) -> None:
        region = self.current_region()
        # Show location context
        print(
            f"\nLocation: {self.current_city().name} → {self.current_neighborhood().name}"
        )
        print(f"You are at: {region.name}")
        print(region.description)
        # Connections
        if region.connections:
            print("Connections:")
            for label, dest_key in region.connections.items():
                dest = self.current_neighborhood().regions[dest_key]
                print(f"  - {label}: {dest.name}")
        else:
            print("No exits here.")

        # Robots
        if region.robots:
            print("Robots present:")
            for i, r in enumerate(region.robots, start=1):
                print(f"  {i}. {r.name}")
        else:
            print("No robots in this area.")

        if region.is_train_station:
            status = "OPERATIONAL" if region.station_unlocked else "locked"
            print(f"Train Station status: {status}")

    def exploration_input(self) -> bool:
        region = self.current_region()
        base = "\nOptions: (M)ove  (T)alk  (Q)uit"
        if region.is_train_station and region.station_unlocked:
            base = base.replace("  (Q)", "  (R)ide  (Q)")
        print(base)
        choice = input("> ").strip().lower()
        if choice == "q":
            print("Goodbye.")
            return False
        elif choice == "m":
            self.handle_move()
        elif choice == "t":
            self.handle_talk()
        elif choice == "r" and region.is_train_station and region.station_unlocked:
            self.handle_ride_train()
        else:
            print("Invalid choice. Try again.")
        return True

    def handle_move(self) -> None:
        region = self.current_region()
        if not region.connections:
            print("No available moves from here.")
            return
        print("Enter a direction/name to move:")
        dest = input("> ").strip().lower()
        if dest in region.connections:
            self.player.region_key = region.connections[dest]
        else:
            print("Can't go there.")

    def handle_talk(self) -> None:
        region = self.current_region()
        if not region.robots:
            print("No one to talk to here.")
            return
        print("Choose a robot number to converse (or blank to cancel):")
        for i, r in enumerate(region.robots, start=1):
            print(f"  {i}. {r.name}")
        raw = input("> ").strip()
        if not raw:
            return
        try:
            idx = int(raw) - 1
            robot = region.robots[idx]
        except (ValueError, IndexError):
            print("Invalid robot selection.")
            return
        self.conversation_loop(robot)

    # ------------- Conversation Mode -------------
    def conversation_loop(self, robot: Robot) -> None:
        current_id = robot.start_node
        while True:
            node = robot.dialog[current_id]
            self.render_dialog(robot, node)
            choice_index = self.get_dialog_choice(node)
            if choice_index is None:
                print(f"Exiting conversation with {robot.name}.")
                return
            choice = node.choices[choice_index]
            # Apply effects
            for eff in choice.effects:
                if eff.startswith("gain:"):
                    code = eff.split(":", 1)[1]
                    self.player.known_codes.add(code)
                    print(f"You memorized code: {code}")
            if choice.next_id is None:
                print(f"Conversation branch with {robot.name} ended.")
                return
            current_id = choice.next_id

    def render_dialog(self, robot: Robot, node: DialogNode) -> None:
        print(f"\n[{robot.name}] {node.text}")
        for i, c in enumerate(node.choices, start=1):
            print(f"  {i}. {c.text}")
        print("  X. Exit conversation")

    def get_dialog_choice(self, node: DialogNode) -> Optional[int]:
        while True:
            raw = input("> ").strip().lower()
            if raw == "x":
                return None
            try:
                idx = int(raw) - 1
                if 0 <= idx < len(node.choices):
                    return idx
            except ValueError:
                pass
            print("Invalid selection. Choose a listed number or X to exit.")

    # ------------- Station Unlock -------------
    def try_unlock_station(self) -> None:
        region = self.current_region()
        if not region.is_train_station:
            print("You are not at a station panel.")
            return
        if region.station_unlocked:
            print("Station already operational.")
            return
        code = input("Enter override code (or blank to cancel): ").strip()
        if not code:
            return
        if code in self.player.known_codes:
            region.station_unlocked = True
            print("The panel chimes happily. Local line restored!")
        else:
            print("Incorrect code. Panel resets.")

    # ------------- Train Travel -------------
    def handle_ride_train(self) -> None:
        region = self.current_region()
        if not (region.is_train_station and region.station_unlocked):
            print("The station isn't operational.")
            return
        city = self.current_city()
        neighborhoods = list(city.neighborhoods.items())
        # Exclude current neighborhood
        destinations = [
            (key, nb)
            for key, nb in neighborhoods
            if key != self.player.neighborhood_key
        ]
        if not destinations:
            print("No other stations on this line yet.")
            return
        print("Choose a destination neighborhood (blank to cancel):")
        for i, (_, nb) in enumerate(destinations, start=1):
            print(f"  {i}. {nb.name}")
        raw = input("> ").strip()
        if not raw:
            return
        try:
            idx = int(raw) - 1
            key, nb = destinations[idx]
        except (ValueError, IndexError):
            print("Invalid selection.")
            return
        # Travel: arrive at the destination's station region
        self.player.neighborhood_key = key
        self.player.region_key = nb.station_region_key
        print(f"You ride the line to {nb.name} and arrive at its station.")

    # ------------- Main Loop -------------
    def run(self) -> None:
        print("Welcome to Roboworld.")
        while True:
            self.show_exploration()
            # Offer station unlock attempt if at station
            if (
                self.current_region().is_train_station
                and not self.current_region().station_unlocked
            ):
                print("(U)nlock station panel available")
                extra = (
                    input("Try unlock now? (u to attempt, Enter to skip): ")
                    .strip()
                    .lower()
                )
                if extra == "u":
                    self.try_unlock_station()
            if not self.exploration_input():
                break


def main() -> None:
    Game().run()


if __name__ == "__main__":
    main()
