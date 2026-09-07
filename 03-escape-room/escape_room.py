from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.input_field import InputField

import random

app = Ursina()

# Room setup
room_size = 20
wall_height = 20

grass = Entity(
    model='plane',
    scale=(1000, 1, 1000),
    position=(room_size/2, -0.01, room_size/2),
    texture='grass',
    texture_scale=(50, 50),
    color=color.white,
    collider='box'
)
sky = Sky(texture='sky_cloudy')
# -------------------------------------------------- first room ---------------------------------------------------------------------------------------------
floor = Entity(model='plane', color=color.brown, scale=(room_size, 1, room_size), texture='white_cube', collider='box')
walls1 = [
    Entity(model='cube', scale=(0.2, wall_height, room_size), x=-room_size/2, color=color.pink, texture='brick', texture_scale=(room_size, wall_height), collider='box'), # west
    Entity(model='cube', scale=(0.2, wall_height, room_size), x=room_size/2, color=color.pink, texture='brick', texture_scale=(room_size, wall_height),collider='box'),  # east
    Entity(model='cube', scale=(room_size, wall_height, 0.2), z=-room_size/2, color=color.pink, texture='brick', texture_scale=(room_size, wall_height),collider='box'), # south
]

north_wall_bricks1 = []
door_bricks1 = []

for x in range(-10, 11):
    for y in range(10):
        pos_x = x
        pos_y = y + 0.5
        pos_z = room_size / 2

        brick = Entity(model='cube', scale=(1, 1, 0.2), color= color.pink, position=(pos_x, pos_y, pos_z), texture='brick', collider='box')

        if abs(pos_x) <= 1 and y < 5:
            door_bricks1.append(brick)
        else:
            north_wall_bricks1.append(brick)

exit_door = Entity(model='cube', scale=(3, 5, 0.21), position=(0, 2.5, room_size/2), color=color.brown, collider='box', locked=True)


pivot = Entity(position=exit_door.position + Vec3(exit_door.scale_x/2, 0, 0))
exit_door.parent = pivot
exit_door.position = (-exit_door.scale_x/2, 0, -exit_door.scale_z/2)

hint = Text(
    text="Try stepping on the tiles and left clicking on them, starting with the cool colors before the warm ones",
    position=(-0.8, 0.4),
    background=True
)

inventory = Text(text='inventory:', position=(0, -0.4), background=True)

# --------------------------------------------------- second room -----------------------------------------------------------------------------------

floor2 = Entity(model='plane', color=color.brown, scale=(room_size, 1, room_size), z=room_size, texture='white_cube', collider='box', enabled=False)
walls2 = [
    Entity(model='cube', scale=(0.2, wall_height, room_size), x=-room_size/2, z=room_size, color=color.pink, collider='box', texture='brick', texture_scale=(room_size, wall_height), enabled=False), # west
    Entity(model='cube', scale=(0.2, wall_height, room_size), x=room_size/2, z=room_size, color=color.pink, collider='box', texture='brick', texture_scale=(room_size, wall_height), enabled=False),  # east
]


north_wall_bricks2 = []
door_bricks2 = []

for x in range(-10, 11):
    for y in range(10):
        pos_x = x
        pos_y = y + 0.5
        pos_z = 1.5*room_size

        brick2 = Entity(model='cube', scale=(1, 1, 0.2), color= color.pink, position=(pos_x, pos_y, pos_z), texture='brick', collider='box', enabled=False)

        if abs(pos_x) <= 1 and y < 5:
            door_bricks2.append(brick2)
        else:
            north_wall_bricks2.append(brick2)

exit_door2 = Entity(model='cube', scale=(3, 5, 0.21), position=(0, 2.5, room_size*1.5), color=color.brown, collider='box', locked=True, enabled=False)


pivot2 = Entity(position=exit_door2.position + Vec3(exit_door2.scale_x/2, 0, 0))
exit_door2.parent = pivot2
exit_door2.position = (-exit_door2.scale_x/2, 0, -exit_door2.scale_z/2)


cabinet_locked = Entity(
    model='cube',
    scale=(2, 2, 1),
    position=(-5, 2, 29),
    texture='white_cube',
    color=color.rgba(220, 240, 255, 80),
    collider='box',
    enabled=False,
    locked=True,
    seternal=True,
    metallic=0.8,
    roughness=0.2 
)

cabinet_door = Entity(
    parent=cabinet_locked,
    model='cube',
    scale=(1, 1, 0.05),
    position=(0, 0, -0.5),
    color=color.rgba(150, 200, 255, 150),
    collider=None,
    seternal=True,
    metallic=0.8,
    roughness=0.2
)
# ------------------------------------------------------- tile in first room -----------------------------------------------------------------
tile_colors = [color.blue, color.green, color.yellow, color.orange, color.red] # purple would raise an error
tiles = []
pos = [(-5, 0.05,5), (-2, 0.05,-1), (8, 0.05,3), (0, 0.05,-9), (5, 0.05,-1)]

for i in range(5):
    tile = Entity(
        model='cube',
        scale=(2, 0.1, 2),
        position=pos[i],
        color=tile_colors[i],
        collider='box',
        original_color=tile_colors[i]
    )
    tiles.append(tile)

# Puzzle logic
correct_sequence = [0, 1, 2, 3, 4]  # Indices for blue, green, yellow, orange, red 
current_sequence = []
player_inventory = []
inventory_display = None
key_found = False
message = None
wrong_message = None
key_entity = None 
password_ui_active = False

# ------------------------------------------------------- anagram in second ---------------------------------------------------------------------
anagram_dict = {
    "ELPAP": "APPLE",
    "RACD": "CARD",
    "RAEB": "BEAR",
    "DAARM": "DRAMA",
    "EMCIR": "CRIME",
    "ILNO": "LION",
    "URTH": "HURT",
    "LEAPN": "PANEL",
    "SOPUTCEMR": "COMPUTERS",
    "RGINPAORM": "PROGRAMING"
}

def evaluate_password(user_input):
    global key_found, password_ui_active
    key_found = False

    if user_input == correct_password:
        key_found= True
        cabinet_locked.locked = False
        mouse.locked = True
        show_message("Correct! Cabinet unlocked. Get near and press 'e' to open the cabinet", color.green)
        return
    else:
        inc = Text(text="Incorrect. Try again.", position=(0.3, 0.4), background=True, color=color.red)
        invoke(destroy, inc, delay=2)
        mouse.locked = False
        password_ui_active = False
        show_password_ui()


def show_password_ui():
    global password_ui_active, correct_password
    if password_ui_active:
        return
    password_ui_active = True
    mouse.locked = False

    hint2 = Text(
    text="Try unscrambling the anagram",
    position=(-0.8, 0.4),
    background=True)

    scrambled_word, correct_password = random.choice(list(anagram_dict.items()))

    # Display the anagram on-screen (2D UI, not world space)
    anagram_display = Text(
        text=f'Terminal: unscramble {scrambled_word}',
        position=(-0.8, 0.3),
        color=color.white,
        background=True
    )
    input_box = InputField(
        default_value='',
        max_lines=1,
        scale=(0.4, 0.08),
        position=(-0.6, 0.2),
        color=color.black)

    submit_button = Button(
        text='Submit',
        position=(-0.4, 0.2),
        scale=(0.1, 0.095),
        color=color.pink
    )

    def submit_handler():
        user_answer = input_box.text.strip().upper()
        destroy(anagram_display)
        destroy(input_box)
        destroy(submit_button)
        destroy(hint2)
        evaluate_password(user_answer)

    submit_button.on_click = submit_handler

def update():
    global key_entity
    # -------- EXIT DOOR 1 --------
    if key_found and distance(player, exit_door) < 5 and mouse.hovered_entity == exit_door:
        if held_keys['e'] and not exit_door.locked:
            pivot.animate_rotation_y(90, duration=1)

            for bricks in door_bricks1:
                destroy(bricks)

            for wall in walls2:
                wall.enabled = True
            for brick in north_wall_bricks2:
                brick.enabled = True

            exit_door2.enabled = True    
            floor2.enabled = True

            cabinet_locked.enabled = True
            cabinet_door.enabled = True

            show_password_ui()

    # -------- CABINET INTERACTION --------
    if distance(player, cabinet_locked) < 5 and mouse.hovered_entity == cabinet_locked:
        if held_keys['e'] and not cabinet_locked.locked:
            # cabinet_door.animate_rotation_y(-90, duration=1)
            cabinet_door.animate_rotation((0, 0, 90), duration=1)
            cabinet_door.animate_scale((0, 0, 0), duration=1)
            reveal_key('KeyCard')
            
    # -------- EXIT DOOR 2 --------
    if "KeyCard" in player_inventory and distance(player, exit_door2) < 5 and mouse.hovered_entity == exit_door2:
        if held_keys['e'] and not exit_door2.locked:
            pivot2.animate_rotation_y(90, duration=1)

            for bricks in door_bricks2:
                destroy(bricks)

        final_message = Text(text="You may now escape!", position=(0.3, 0.4), background=True, color=color.green)
        invoke(destroy, final_message, delay=3)

    # -------- KEY COLLECTION --------
    # Check for key collection every frame (automatic when near)
    if key_entity and distance(player, key_entity) < 2:
        key_entity.enabled = False
        collect_keys()

def input(key):
    global current_sequence, key_found, wrong_message, message
    # room 1
    if key == 'left mouse down' and not key_found:
        hit_info = raycast(camera.world_position, camera.forward, distance=5, ignore=[player])
        
        if hit_info.hit and hit_info.entity in tiles:

            if wrong_message:
                destroy(wrong_message)
                wrong_message = None

            tile = hit_info.entity
            i = tiles.index(tile)

            # Check distance (player must be on/near the tile)
            if distance(player, tile) < 2:
                current_sequence.append(i)
                tile.color = color.gray

                if current_sequence == correct_sequence:
                    destroy(hint)
                    reveal_key()
                elif len(current_sequence) == len(correct_sequence):
                        wrong_message = Text(text="Wrong sequence! Try again.", position=(0.45, 0.4), background=True, color=color.red)
                        reset_tiles()

def reveal_key(key_type=None):
    global key_entity, inventory_display, key_found
    
    if key_entity:
        destroy(key_entity)
        key_entity = None

    if key_type == "KeyCard":
        key_entity = Entity(
            model='cube',
            scale=(0.5, 0.1, 1),
            position=cabinet_locked.position + (0, 0.5, -0.5),
            texture='white_cube',
            color=color.gold,
            collider='box',
            name=key_type
        )
        msg = show_message("KeyCard revealed! Get near to collect it", color.yellow) # c
        if not exit_door.locked:
            destroy(msg)
    else:
        # For the first key
        key_entity = Entity(
            model='cube',
            scale=(0.5, 0.1, 1),
            position=(0, 1, 0),
            texture='white_cube',
            color=color.gold,
            collider='box',
            name="Rusty key"
        )
        key_found = True
        show_message("Rusty key revealed! Get near to collect it", color.yellow) # c
        if not exit_door2.locked:
            destroy(msg)

def collect_keys():
    global player_inventory, inventory_display, key_entity, key_found, inventory
    destroy(inventory)

    key_name = key_entity.name
    
    # Add to inventory
    player_inventory.append(key_name)
    
    # Update inventory display
    if inventory_display:
        destroy(inventory_display)
    
    inventory_text = "Inventory:\n" + "\n".join(player_inventory)
    inventory_display = Text(text=inventory_text,position=(0, -0.4),background=True)
    
    if key_name == "Rusty key":
        key_found = True
        exit_door.locked = False
        msg = show_message("Rusty key collected. First door unlocked! Approach and press 'e'", color.green)
        if floor2.enabled:
            destroy(msg)

    elif key_name == "KeyCard":
        exit_door2.locked = False
        show_message("KeyCard collected. Final door unlocked! Approach and press 'e'", color.green)

    # Remove key from world
    destroy(key_entity)
    key_entity = None  # Clear the reference

def reset_tiles():
    global current_sequence
    current_sequence = []
    for tile in tiles:
        tile.color = tile.original_color

def show_message(text, color=color.white):
    global message
    if message:
        destroy(message)
    message = Text(
        text=text,
        position=(-0.8, 0.4),
        background=True,
        color=color
    )
    invoke(destroy, message, delay=3)

# Player setup
player = FirstPersonController(
    position=(0, 0, -5),
    mouse_sensitivity=Vec2(100, 100)
)
# camera.position = (room_size/2, 20, room_size/2)
# camera.rotation_x = 90  # Look straight down
player.collider = BoxCollider(player, size=(1, 2, 1))

app.run()