#!/usr/bin/env python3
import blessed
import random
import time
from typing import List, Optional, Set
from dungeon import generate_dungeon, Room
from items import Item, generate_random_item
from entities import Entity, create_player, create_random_monster, create_boss_dragon

term = blessed.Terminal()

class Game:
    def __init__(self, width: int = 80, height: int = 24):
        self.width = width
        self.height = height
        self.map, self.rooms = generate_dungeon(width, height)
        self.running = True
        self.messages: List[str] = ["Welcome to Rogue! Find and defeat the Ancient Dragon to win!"]
        
        # Place player in first room
        start_room = self.rooms[0]
        px, py = start_room.center
        self.player = create_player(px, py)
        
        self.monsters: List[Entity] = []
        self.items: List[Item] = []
        self.spawn_entities()
        
    def spawn_entities(self):
        # Spawn boss in the last room
        last_room = self.rooms[-1]
        bx, by = last_room.center
        boss = create_boss_dragon(bx, by)
        self.monsters.append(boss)
        
        # Spawn monsters and items in rooms (except starting and boss rooms)
        for room in self.rooms[1:-1]:
            # Add 1-3 monsters per room
            num_monsters = random.randint(1, 3)
            for _ in range(num_monsters):
                x = random.randint(room.x + 1, room.x + room.width - 2)
                y = random.randint(room.y + 1, room.y + room.height - 2)
                monster = create_random_monster(x, y)
                self.monsters.append(monster)
            
            # Add 0-2 items per room
            num_items = random.randint(0, 2)
            for _ in range(num_items):
                x = random.randint(room.x + 1, room.x + room.width - 2)
                y = random.randint(room.y + 1, room.y + room.height - 2)
                item = generate_random_item(x, y)
                self.items.append(item)

    def show_death_screen(self):
        # Clear screen
        print(term.home + term.clear)
        
        # Calculate center of screen
        center_y = self.height // 2
        message = "YOU DIED"
        center_x = (self.width - len(message)) // 2
        
        # Blink the message 5 times
        for _ in range(5):
            # Show message in red
            print(term.move(center_y, center_x) + term.bold_red + message + term.normal)
            time.sleep(0.5)
            # Clear message
            print(term.move(center_y, center_x) + " " * len(message))
            time.sleep(0.5)
        
        # Show final message
        print(term.move(center_y, center_x) + term.bold_red + message + term.normal)
        time.sleep(2)

    def show_victory_screen(self):
        # Clear screen
        print(term.home + term.clear)
        
        # Calculate center of screen
        center_y = self.height // 2
        message = "YOU KILLED THE ANCIENT DRAGON"
        center_x = (self.width - len(message)) // 2
        
        # Blink the message 5 times
        for _ in range(5):
            # Show message in gold
            print(term.move(center_y, center_x) + term.bold + term.yellow + message + term.normal)
            time.sleep(0.5)
            # Clear message
            print(term.move(center_y, center_x) + " " * len(message))
            time.sleep(0.5)
        
        # Show final victory message
        print(term.move(center_y, center_x) + term.bold + term.yellow + message + term.normal)
        print(term.move(center_y + 2, center_x + (len(message) - 14) // 2) + term.green + "VICTORY ACHIEVED" + term.normal)
        time.sleep(3)

    def move_player(self, dx: int, dy: int):
        new_x = self.player.x + dx
        new_y = self.player.y + dy
        
        # Check for wall collision
        if self.map[new_y][new_x] != "#":
            # Check for monster collision
            monster = next((m for m in self.monsters if m.x == new_x and m.y == new_y), None)
            if monster:
                damage = self.player.attack(monster)
                self.messages.append(f"You hit the {monster.name} for {damage} damage!")
                
                if monster.is_dead():
                    self.messages.append(f"You killed the {monster.name}!")
                    if monster.is_boss:
                        self.draw()  # Draw final game state
                        self.show_victory_screen()
                        self.running = False
                    self.monsters.remove(monster)
                else:
                    # Monster counterattack
                    monster_damage = monster.attack(self.player)
                    self.messages.append(f"The {monster.name} hits you for {monster_damage} damage!")
                    
                    if self.player.is_dead():
                        self.draw()  # Draw final game state
                        self.show_death_screen()
                        self.running = False
            else:
                # Check for items
                item = next((i for i in self.items if i.x == new_x and i.y == new_y), None)
                if item:
                    if self.player.inventory.add_item(item):
                        self.messages.append(f"You picked up {item.name}!")
                        self.items.remove(item)
                    else:
                        self.messages.append("Your inventory is full!")
                else:
                    self.player.x = new_x
                    self.player.y = new_y

    def handle_inventory(self):
        if not self.player.inventory.items:
            self.messages.append("Inventory is empty!")
            return
        
        # Show inventory
        print(term.clear)
        print("Inventory:")
        for i, item in enumerate(self.player.inventory.items):
            print(f"{i+1}) {item.name}")
        print("\nPress 1-9 to use/equip item, or any other key to cancel")
        
        key = term.inkey()
        if key.isdigit():
            index = int(key) - 1
            if 0 <= index < len(self.player.inventory.items):
                item = self.player.inventory.items[index]
                if item.healing > 0:
                    # Use healing item
                    healed = self.player.heal(item.healing)
                    self.messages.append(f"You healed for {healed} HP!")
                    self.player.inventory.remove_item(item)
                elif item.damage > 0:
                    # Equip weapon
                    old_weapon = self.player.weapon
                    self.player.weapon = item
                    if old_weapon:
                        self.player.inventory.add_item(old_weapon)
                    self.player.inventory.remove_item(item)
                    self.messages.append(f"Equipped {item.name}!")
                elif item.defense > 0:
                    # Equip armor
                    old_armor = self.player.armor
                    self.player.armor = item
                    if old_armor:
                        self.player.inventory.add_item(old_armor)
                    self.player.inventory.remove_item(item)
                    self.messages.append(f"Equipped {item.name}!")

    def draw(self):
        print(term.home + term.clear)
        
        # Draw map and entities
        for y in range(self.height):
            for x in range(self.width):
                char = self.map[y][x]
                
                # Draw items
                item = next((i for i in self.items if i.x == x and i.y == y), None)
                if item:
                    print(term.move(y, x) + getattr(term, item.color)(item.char), end="")
                # Draw monsters
                elif monster := next((m for m in self.monsters if m.x == x and m.y == y), None):
                    print(term.move(y, x) + getattr(term, monster.color)(monster.char), end="")
                # Draw player
                elif x == self.player.x and y == self.player.y:
                    print(term.move(y, x) + term.yellow(self.player.char), end="")
                else:
                    print(term.move(y, x) + char, end="")
        
        # Draw health bar
        health_percent = self.player.stats.hp / self.player.stats.max_hp
        bar_width = 20  # Width of health bar in characters
        filled_width = int(health_percent * bar_width)
        empty_width = bar_width - filled_width
        
        # Choose color based on health percentage
        if health_percent > 0.7:
            health_color = term.green
        elif health_percent > 0.3:
            health_color = term.yellow
        else:
            health_color = term.red
        
        health_bar = (
            health_color + "█" * filled_width +  # Filled portion
            term.white + "░" * empty_width +     # Empty portion
            term.normal
        )
        
        # Draw status with health bar
        health_text = f"HP: {self.player.stats.hp}/{self.player.stats.max_hp}"
        print(term.move(self.height, 0) + term.bold + health_text + " " + health_bar + term.normal, end="")
        
        # Draw equipment status on the same line
        equipment_text = ""
        if self.player.weapon:
            equipment_text += f" Weapon: {self.player.weapon.name}"
        if self.player.armor:
            equipment_text += f" Armor: {self.player.armor.name}"
        print(equipment_text)
        
        # Draw messages
        for i, msg in enumerate(self.messages[-3:]):
            print(term.move(self.height + 1 + i, 0) + msg)

    def handle_input(self, key: str):
        if key.lower() == "q":
            self.running = False
        elif key.name == "KEY_UP" or key.lower() == "w":
            self.move_player(0, -1)
        elif key.name == "KEY_DOWN" or key.lower() == "s":
            self.move_player(0, 1)
        elif key.name == "KEY_LEFT" or key.lower() == "a":
            self.move_player(-1, 0)
        elif key.name == "KEY_RIGHT" or key.lower() == "d":
            self.move_player(1, 0)
        elif key.lower() == "i":
            self.handle_inventory()
        elif key == "+":  # Cheat code
            # Find the boss dragon
            boss = next((m for m in self.monsters if m.is_boss), None)
            if boss:
                self.messages.append("CHEAT ACTIVATED: Ancient Dragon vanquished!")
                self.monsters.remove(boss)
                self.draw()  # Draw final game state
                self.show_victory_screen()
                self.running = False

def main():
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        game = Game()
        
        while game.running:
            game.draw()
            key = term.inkey()
            game.handle_input(key)

if __name__ == "__main__":
    main() 