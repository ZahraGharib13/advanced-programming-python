# Pacman Multiplayer

A collaborative two-player networked Pacman-style game built with **Python**, **Pygame**, and TCP sockets.

## Authors

- Zahra Gharib
- Seyed Sajjad Qavami

This project was developed collaboratively as part of the Advanced Programming course.

## Project Overview

The game uses a client-server architecture:

- `pacman_server.py` owns the main game state, map, players, pellets, ghosts, collision logic, scores, and networking.
- `pacman_client.py` connects to the server, sends keyboard input, receives the current game state, and renders the game with Pygame.
- The server waits for **two clients** before the multiplayer game starts.

## Requirements

- Python 3
- Pygame

Install the dependency with:

```bash
pip install -r requirements.txt
```

## How to Run

Open **three terminals** in this folder.

### 1. Start the server

```bash
python pacman_server.py
```

### 2. Start player 1

```bash
python pacman_client.py
```

### 3. Start player 2

```bash
python pacman_client.py
```

If your system uses `python3`, replace `python` with `python3`.

## Controls

| Key | Action |
| --- | --- |
| Left Arrow | Move left |
| Right Arrow | Move right |
| Up Arrow | Move up |
| Down Arrow | Move down |

## Networking

The default connection settings are:

```text
Host: 127.0.0.1
Port: 8002
```

With the default host, the server and both clients run on the same computer.

To play on different computers, the host setting must be changed to an address that the client machines can reach.

Game state and input are serialized using Python `pickle` and transferred over TCP sockets. This is appropriate for a trusted/local coursework environment, but `pickle` should not be used with untrusted network data in a production application.

## Project Structure

```text
07-pacman-multiplayer/
├── pacman_client.py
├── pacman_server.py
├── requirements.txt
└── README.md
```

## About

This project demonstrates:

- client-server programming
- TCP sockets
- threading
- multiplayer game-state synchronization
- Pygame graphics and input
- collision detection
- score and game-state management
- object-oriented programming
