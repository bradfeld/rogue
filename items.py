from dataclasses import dataclass
from typing import List, Optional
import random

@dataclass
class Item:
    name: str
    char: str
    color: str
    x: int = 0
    y: int = 0
    damage: int = 0
    defense: int = 0
    healing: int = 0

class Inventory:
    def __init__(self, capacity: int = 10):
        self.items: List[Item] = []
        self.capacity = capacity
        
    def add_item(self, item: Item) -> bool:
        if len(self.items) < self.capacity:
            self.items.append(item)
            return True
        return False
    
    def remove_item(self, item: Item) -> None:
        if item in self.items:
            self.items.remove(item)

# Item templates
ITEMS = {
    "health_potion": lambda: Item("Health Potion", "!", "red", healing=20),
    "sword": lambda: Item("Sword", "/", "cyan", damage=5),
    "shield": lambda: Item("Shield", "]", "blue", defense=3),
    "better_sword": lambda: Item("Steel Sword", "/", "white", damage=8),
    "better_shield": lambda: Item("Steel Shield", "]", "white", defense=5),
}

def generate_random_item(x: int, y: int) -> Item:
    item_creator = random.choice(list(ITEMS.values()))
    item = item_creator()
    item.x = x
    item.y = y
    return item 