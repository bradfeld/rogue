from dataclasses import dataclass
from typing import List, Optional
from items import Item, Inventory
import random

@dataclass
class Stats:
    max_hp: int
    hp: int
    attack: int
    defense: int
    level: int = 1
    xp: int = 0

class Entity:
    def __init__(self, x: int, y: int, char: str, color: str, name: str,
                 stats: Stats, is_player: bool = False, is_boss: bool = False):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.stats = stats
        self.is_player = is_player
        self.is_boss = is_boss
        self.inventory = Inventory() if is_player else None
        self.weapon: Optional[Item] = None
        self.armor: Optional[Item] = None

    def attack(self, target: 'Entity') -> int:
        base_damage = self.stats.attack
        if self.weapon:
            base_damage += self.weapon.damage
        
        defense = target.stats.defense
        if target.armor:
            defense += target.armor.defense
            
        damage = max(1, base_damage - defense)
        target.stats.hp -= damage
        return damage

    def is_dead(self) -> bool:
        return self.stats.hp <= 0

    def heal(self, amount: int) -> int:
        missing_hp = self.stats.max_hp - self.stats.hp
        heal_amount = min(missing_hp, amount)
        self.stats.hp += heal_amount
        return heal_amount

# Monster templates
MONSTERS = {
    "rat": lambda x, y: Entity(
        x, y, "r", "brown", "Rat",
        Stats(max_hp=5, hp=5, attack=2, defense=0)
    ),
    "orc": lambda x, y: Entity(
        x, y, "o", "green", "Orc",
        Stats(max_hp=10, hp=10, attack=4, defense=1)
    ),
    "troll": lambda x, y: Entity(
        x, y, "T", "red", "Troll",
        Stats(max_hp=15, hp=15, attack=6, defense=2)
    ),
    "dragon": lambda x, y: Entity(
        x, y, "D", "red", "Dragon",
        Stats(max_hp=30, hp=30, attack=10, defense=4)
    )
}

def create_boss_dragon(x: int, y: int) -> Entity:
    return Entity(
        x, y, "Đ", "magenta", "Ancient Dragon",
        Stats(max_hp=50, hp=50, attack=15, defense=8),
        is_boss=True
    )

def create_player(x: int, y: int) -> Entity:
    return Entity(
        x, y, "@", "yellow", "Player",
        Stats(max_hp=30, hp=30, attack=5, defense=2),
        is_player=True
    )

def create_random_monster(x: int, y: int, difficulty: int = 1) -> Entity:
    # Higher difficulty increases chance of stronger monsters
    choices = list(MONSTERS.values())
    weights = [1] * len(choices)
    for i in range(len(weights)):
        if i >= difficulty:
            weights[i] *= 0.5 ** (i - difficulty + 1)
    
    monster_creator = random.choices(choices, weights=weights)[0]
    return monster_creator(x, y) 