# Python Rogue Clone

A text-based implementation of the classic roguelike dungeon crawler game Rogue.

100% Written by Claude 3.5 Sonnet using Cursor Composer.

## Features
- Procedurally generated dungeons
- Turn-based gameplay
- ASCII graphics
- Player movement and combat
- Items and inventory system
- Monsters and combat

## Controls
- Arrow keys or WASD: Move player
- i: Open inventory
- q: Quit game
- Enter/Space: Interact/Attack 
- A cheat code exists to automatically win the game

## Game Symbols
| Symbol | Description |
|--------|-------------|
| `@` | Player character |
| `#` | Wall |
| `.` | Floor |
| `+` | Door |
| `>` | Stairs down |
| `<` | Stairs up |
| `M` | Monster (generic) |
| `g` | Goblin |
| `o` | Orc |
| `T` | Troll |
| `D` | Dragon |
| `Đ` | Ancient Dragon |
| `$` | Gold |
| `!` | Potion |
| `/` | Weapon |
| `]` | Armor |
| `?` | Scroll |
| `=` | Ring |
| `%` | Food |
| `~` | Water |
| ` ` | (space) Unexplored area |

## Setup
1. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Unix/macOS
# or
.\venv\Scripts\activate  # On Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the game:
```bash
python main.py
```

## Credits
- Inspired by a Friday afternoon conversation with Dan Shapiro.
- Modeled after the Rogue game by Michael Toy and Glenn Wichman with later contributions by Ken Arnold. 
- Cursor Composer was used to write the code.
- More info on the Rogue game can be found [here](https://en.wikipedia.org/wiki/Rogue_(video_game)).
- Bonus video of [Dan Shapiro explaining Rogue](https://www.youtube.com/watch?v=7CZJXM8PuJY)
