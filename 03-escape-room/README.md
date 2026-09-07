# Escape Room

A 3D escape-room game built with Python and the Ursina Engine.

## Gameplay

The game contains multiple puzzle-based rooms.

In the first room, the player must interact with colored floor tiles in the correct order to reveal a key and unlock the first door.

In the second room, the player is given a scrambled word (an anagram). Solving it unlocks a cabinet containing a key card that can be used to open the final door.

## Features

- First-person 3D movement
- Interactive doors and objects
- Color-sequence puzzle
- Anagram puzzle
- Inventory system
- Keys and key cards
- On-screen hints and messages
- Multiple rooms
- Mouse-based interaction

## Requirements

- Python 3
- Ursina Engine

Install the required package with:

```bash
pip install -r requirements.txt
```

## How to Run

Open a terminal in this folder and run:

```bash
python escape_room.py
```

If your system uses `python3`, run:

```bash
python3 escape_room.py
```

## Controls

- `W`, `A`, `S`, `D` — move
- Mouse — look around
- Left mouse button — interact with the colored tiles
- `E` — interact with doors and the cabinet
- Type into the on-screen input field to solve the anagram puzzle

## Project Structure

```text
03-escape-room/
├── escape_room.py
├── requirements.txt
└── README.md
```

## Notes

This project uses built-in Ursina models and textures such as `cube`, `plane`, `brick`, `grass`, and `sky_cloudy`.

## About

This project was created as part of an Advanced Programming course.
It demonstrates 3D game development, event handling, object interaction, collision detection, inventory logic, and puzzle design using Python and Ursina.
