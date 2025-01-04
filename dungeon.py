import random
from dataclasses import dataclass
from typing import List, Tuple, Set

@dataclass
class Room:
    x: int
    y: int
    width: int
    height: int

    @property
    def center(self) -> Tuple[int, int]:
        return (self.x + self.width // 2, self.y + self.height // 2)

    def intersects(self, other: 'Room') -> bool:
        return (self.x <= other.x + other.width and self.x + self.width >= other.x and
                self.y <= other.y + other.height and self.y + self.height >= other.y)

def generate_dungeon(width: int, height: int, max_rooms: int = 15) -> Tuple[List[List[str]], List[Room]]:
    # Initialize with walls
    dungeon = [["#" for _ in range(width)] for _ in range(height)]
    rooms: List[Room] = []
    
    # Generate rooms
    for _ in range(max_rooms):
        # Random room size
        w = random.randint(5, 10)
        h = random.randint(5, 10)
        x = random.randint(1, width - w - 1)
        y = random.randint(1, height - h - 1)
        
        new_room = Room(x, y, w, h)
        
        # Check if room intersects with existing rooms
        if not any(new_room.intersects(room) for room in rooms):
            create_room(dungeon, new_room)
            
            if rooms:
                # Connect to previous room
                prev_room = rooms[-1]
                connect_rooms(dungeon, new_room, prev_room)
            
            rooms.append(new_room)
    
    return dungeon, rooms

def create_room(dungeon: List[List[str]], room: Room) -> None:
    for y in range(room.y, room.y + room.height):
        for x in range(room.x, room.x + room.width):
            dungeon[y][x] = "."

def connect_rooms(dungeon: List[List[str]], room1: Room, room2: Room) -> None:
    x1, y1 = room1.center
    x2, y2 = room2.center
    
    # Randomly choose whether to go horizontal then vertical, or vertical then horizontal
    if random.random() < 0.5:
        create_horizontal_tunnel(dungeon, x1, x2, y1)
        create_vertical_tunnel(dungeon, y1, y2, x2)
    else:
        create_vertical_tunnel(dungeon, y1, y2, x1)
        create_horizontal_tunnel(dungeon, x1, x2, y2)

def create_horizontal_tunnel(dungeon: List[List[str]], x1: int, x2: int, y: int) -> None:
    for x in range(min(x1, x2), max(x1, x2) + 1):
        dungeon[y][x] = "."

def create_vertical_tunnel(dungeon: List[List[str]], y1: int, y2: int, x: int) -> None:
    for y in range(min(y1, y2), max(y1, y2) + 1):
        dungeon[y][x] = "." 