import pygame
import random
import time
import os

pygame.init()

TILE_SIZE = 32
LAB_OFFSET = TILE_SIZE * 10
WIDTH, HEIGHT = 640, 480
def update_map_size():
    global MAP_WIDTH, MAP_HEIGHT
    MAP_WIDTH = WORLD_W // TILE_SIZE
    MAP_HEIGHT = WORLD_H // TILE_SIZE
WORLD_W, WORLD_H = 3200, 3200
update_map_size()
MAP_WIDTH = WORLD_W // TILE_SIZE
MAP_HEIGHT = WORLD_H // TILE_SIZE
areas = {
    1: {
        "name": "Pallet Town",
        "size": (1100, 1300),
    },
    2: {
        "name": "Route One",
        "size": (640, 1000),
    },
    3: {
        "name": "First Town",
        "size": (1100, 1300),
    }
}

world_id = 1
area_banner_text = ""
area_banner_timer = 0
show_area_banner = False
banner_y = -80
base_speed = 2
sprint_speed = 4
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Pokemon Battle")
grass_tiles = []
path_tiles = []
bush_tiles = []
obstacles = []
zigzag_path = []
zigzag_bushes = []
zigzag_trees = []
route_fence = []
route_signs = []
route_flowers = []

encountered_bushes = set()
bush_img = pygame.image.load(
    "sprites/ground_tiles_assorted/tile_r02_c00.png"
).convert()

bush_img = pygame.transform.scale(
    bush_img,
    (TILE_SIZE, TILE_SIZE)
)
pokemart_img = pygame.transform.scale(
    pygame.image.load("pokemart.png").convert_alpha(),
    (192, 192)
)

pokecenter_img = pygame.transform.scale(
    pygame.image.load("pokecenter.png").convert_alpha(),
    (192, 192)
)

bush_tiles.append(bush_img)
for i in range(6):
    img = pygame.image.load("sprites/ground_tiles_assorted/tile_r00_c00.png").convert()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    grass_tiles.append(img)
# path tiles
for i in range(8):
    img = pygame.image.load(
        f"sprites/ground_tiles_assorted/tile_r14_c00.png"
    ).convert()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    path_tiles.append(img)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Pokemon Battle")
font = pygame.font.SysFont(None, 30)
HOUSE_BG = pygame.transform.scale(
    pygame.image.load("inhouse.png").convert(),
    (WIDTH, HEIGHT)
)
lab_bg_fullscreen = pygame.transform.scale(
    pygame.image.load("insidelab.png").convert(),
    (WIDTH, HEIGHT)
)
lab_img = pygame.transform.scale(
    pygame.image.load("lab.png").convert_alpha(),
    (240, 240)
)
LAB_DOOR_WIDTH = 64
LAB_DOOR_HEIGHT = 48


INSIDE_LAB_BG = pygame.transform.scale(
    pygame.image.load("insidelab.png").convert(),
    (WIDTH, HEIGHT)
)
tree_img = pygame.image.load("tree.png").convert_alpha()
TREE_SRC = pygame.Rect(0, 0, 48, 64)
scale = 1
tree_img = pygame.transform.scale(
    tree_img,
    (TREE_SRC.width * scale, TREE_SRC.height * scale)
)

def clean_grass_edges(surface, bg_color):
    surface.set_colorkey(bg_color)
    return surface

decor_bg_color = (0, 0, 0)
HOUSE_SRC_FOOT = (10, 0, 192, 148)
HOUSE_SRC_DOOR = (96, 95, 52, 52)
HOUSE_DISP = 192

house_img = pygame.transform.scale(
    pygame.image.load("house.png").convert_alpha(),
    (HOUSE_DISP, HOUSE_DISP)
)
_fx, _fy, _fw, _fh = HOUSE_SRC_FOOT
_sx = HOUSE_DISP / _fw
_sy = HOUSE_DISP / _fh

house_rect = house_img.get_rect(topleft=(360, 420))
bush_encounters = []
rare_bushes = []
forest_trees = []
forest_bushes = []
tree_rect = pygame.Rect(180, 300, TILE_SIZE, TILE_SIZE * 2)
tree_hitbox = pygame.Rect(
    tree_rect.x + 14,
    tree_rect.y + 44,
    20,
    20
)
door_rect = pygame.Rect(
    int(house_rect.x + (HOUSE_SRC_DOOR[0] - _fx) * _sx),
    int(house_rect.y + (HOUSE_SRC_DOOR[1] - _fy) * _sy),
    int(HOUSE_SRC_DOOR[2] * _sx),
    int(HOUSE_SRC_DOOR[3] * _sy),
)
house_hitbox = pygame.Rect(
    house_rect.x,
    house_rect.y,
    house_rect.width,
    house_rect.height,
)
_door_gap = door_rect.inflate(8, 0)
house_back_hitbox = pygame.Rect(
    house_hitbox.x,
    house_hitbox.y,
    house_hitbox.width,
    max(0, _door_gap.y - house_hitbox.y),
)
house_left_hitbox = pygame.Rect(
    house_hitbox.x,
    _door_gap.y,
    max(0, _door_gap.x - house_hitbox.x),
    house_hitbox.bottom - _door_gap.y,
)
house_right_hitbox = pygame.Rect(
    _door_gap.right,
    _door_gap.y,
    max(0, house_hitbox.right - _door_gap.right),
    house_hitbox.bottom - _door_gap.y,
)
PATH_LEFT = house_rect.centerx - TILE_SIZE
PATH_WIDTH = 3 * TILE_SIZE
north_exit = pygame.Rect(
    PATH_LEFT,
    0,
    PATH_WIDTH,
    TILE_SIZE * 2,
)
door_touch_rect = pygame.Rect(
    door_rect.x - 12,
    door_rect.y + 6,
    door_rect.width + 24,
    door_rect.height + 8,
)

    
pokemart_rect = pokemart_img.get_rect(
    topleft=(house_rect.right + (10 * TILE_SIZE), house_rect.y + 200)
)

pokecenter_rect = pokecenter_img.get_rect(
    topleft=(house_rect.right + (10 * TILE_SIZE), house_rect.y + 450)
)
POKEMART_FP = pygame.Rect(36, 42, 116, 112)
POKECENTER_FP = pygame.Rect(13, 18, 121, 136)

def pokemart_hitbox():
    return pygame.Rect(
        pokemart_rect.x + POKEMART_FP.x,
        pokemart_rect.y + POKEMART_FP.y,
        POKEMART_FP.width,
        POKEMART_FP.height,
    )

def pokecenter_hitbox():
    return pygame.Rect(
        pokecenter_rect.x + POKECENTER_FP.x,
        pokecenter_rect.y + POKECENTER_FP.y,
        POKECENTER_FP.width,
        POKECENTER_FP.height,
    )

def add_building_obstacles():
    obstacles.append(pokemart_hitbox())
    obstacles.append(pokecenter_hitbox())
    obstacles.append(lab_top_hitbox)
    obstacles.append(lab_left_hitbox)
    obstacles.append(lab_right_hitbox)

def add_town_obstacles():
    obstacles.extend([
        tree_hitbox,
        house_left_hitbox,
        house_right_hitbox,
        house_back_hitbox,
        lab_top_hitbox,
        lab_left_hitbox,
        lab_right_hitbox,
    ])
    obstacles.append(pokemart_hitbox())
    obstacles.append(pokecenter_hitbox())
    add_bush_obstacles()

pokemart_door = pygame.Rect(
    pokemart_rect.centerx - 25,
    pokemart_rect.bottom - 60,
    50,
    60
)

pokecenter_door = pygame.Rect(
    pokecenter_rect.centerx - 25,
    pokecenter_rect.bottom - 60,
    50,
    60
)
PATH_LENGTH = 20
path_end_x = house_rect.x - 160 + (PATH_LENGTH - 1) * TILE_SIZE
path_y = house_rect.bottom

lab_rect = lab_img.get_rect(
    topleft=(house_rect.right + (2 * TILE_SIZE), house_rect.y)
)
lab_door_rect = pygame.Rect(
    lab_rect.centerx - 24,
    lab_rect.y + 156,
    48,
    45,
)
lab_door_gap = lab_door_rect.inflate(0, 6)
lab_hitbox = pygame.Rect(
    lab_rect.x,
    lab_rect.y,
    lab_rect.width,
    lab_rect.height,
)
lab_top_hitbox = pygame.Rect(
    lab_hitbox.x,
    lab_hitbox.y,
    lab_hitbox.width,
    max(0, lab_door_gap.y - lab_hitbox.y),
)
lab_left_hitbox = pygame.Rect(
    lab_hitbox.x,
    lab_door_gap.y,
    max(0, lab_door_gap.x - lab_hitbox.x),
    lab_hitbox.bottom - lab_door_gap.y,
)
lab_right_hitbox = pygame.Rect(
    lab_door_gap.right,
    lab_door_gap.y,
    max(0, lab_hitbox.right - lab_door_gap.right),
    lab_hitbox.bottom - lab_door_gap.y,
)
lab_exit_rect = pygame.Rect(WIDTH // 2 - 30, HEIGHT - 60, 60, 20)
route_exit = pygame.Rect(
    WORLD_W//2 - 40,
    50,
    80,
    40
)
if world_id == 2:

    forest_start_y = 1400

starter_npc = pygame.Rect(300, 180, TILE_SIZE, TILE_SIZE)
starter_selected = False
clump_start_x = house_rect.left + (3 * TILE_SIZE)
clump_start_y = house_rect.bottom + (5 * TILE_SIZE)
clump_rows = 2
clump_cols = 5

for row in range(clump_rows):
    for col in range(clump_cols):
        x = clump_start_x + col * TILE_SIZE
        y = clump_start_y + row * TILE_SIZE
        bush_rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        bush_encounters.append(bush_rect)
        obstacles.append(bush_rect)  

rare_start_x = tree_rect.x - 3 * TILE_SIZE
rare_start_y = house_rect.y - 96

for row in range(2):
    for col in range(3):
        x = rare_start_x + col * TILE_SIZE
        y = rare_start_y + row * TILE_SIZE
        bush_rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        rare_bushes.append(bush_rect)
        obstacles.append(bush_rect)
forest_start_y = 1400
for row in range(8):

    for col in range(8):

        offset = 0

        if row % 2 == 1:
            offset = 64

        x = 300 + (col * TILE_SIZE)
        y = forest_start_y + (row * TILE_SIZE * 2)

        tree_rect_new = pygame.Rect(
            x,
            y,
            TILE_SIZE,
            TILE_SIZE * 2
        )

        forest_trees.append(tree_rect_new)

direction = 10
for row in range(10):

    for col in range(12):

        x = 220 + (col * 96)

        y = forest_start_y + 80 + (row * 96)

        
obstacles.extend([
    tree_hitbox,
    house_left_hitbox,
    house_right_hitbox
    ,
    house_back_hitbox
    ,
    lab_top_hitbox,
    lab_left_hitbox,
    lab_right_hitbox
])
add_building_obstacles()

def add_bush_obstacles():
    if starter_selected:
        for bush in bush_encounters + forest_bushes + rare_bushes:
            if bush in obstacles:
                obstacles.remove(bush)
        return
    for bush in bush_encounters + forest_bushes + rare_bushes:
        if bush not in obstacles:
            obstacles.append(bush)

add_bush_obstacles()  # lock bushes at world load (pre-starter)
for bush in zigzag_bushes:
    obstacles.append(bush)

for tree in zigzag_trees:
    obstacles.append(
        pygame.Rect(
            tree.x + 18,
            tree.y + 40,
            tree.width - 36,
            tree.height - 55
        )
    )

for tree in forest_trees:
    if tree.y > WORLD_H - 600:
        continue
    forest_hitbox = pygame.Rect(
        tree.x + 10,
        tree.bottom - 30,
        tree.width - 20,
        30
    )

    obstacles.append(forest_hitbox)
if starter_selected:
    for bush in bush_encounters:
        obstacles.append(bush)
for bush in forest_bushes:
    if bush.y > WORLD_H - 600:
        continue
        obstacles.append(bush)


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
#type chart
TYPE_CHART = {
    "normal": {},
    "fire": {
        "grass": 2.0,
        "fire": 0.5,
        "water": 0.5
    },
    "poison": {
        "grass": 2.0,
        "poison": 0.5,
        "ground": 0.5
    },
    "electric": {
        "water": 2.0,
        "electric": 0.5,
        "grass": 0.5
    },
    "grass": {
        "water": 2.0,
        "fire": 0.5,
        "grass": 0.5,
        "poison": 0.5
    },
    "water": {
        "fire": 2.0,
        "water": 0.5,
        "grass": 0.5
    },

    "rock": {
        "fire": 2.0,
        "flying": 2.0,
        "ground": 0.5
    },

    "ground": {
        "electric": 2.0,
        "fire": 2.0,
        "grass": 0.5
    },

"flying": {
    "grass": 2.0,
    "electric": 0.5
    },

    "ghost": {
        "ghost": 2.0,
        "normal": 0.0
    },

    "dragon": {
        "dragon": 2.0
    },

    "steel": {
        "rock": 2.0,
        "ice": 2.0,
        "fire": 0.5
    }
    ,
    "shadow": {
        "psychic": 2.0,
        "ghost": 2.0,
        "light": 0.5
    },

    "light": {
        "shadow": 2.0,
        "ghost": 1.5
    },

    "crystal": {
        "dragon": 2.0,
        "fire": 0.5,
        "rock": 2.0
    },

    "sound": {
        "water": 1.5,
        "flying": 2.0
    },

    "cosmic": {
        "dragon": 2.0,
        "psychic": 2.0
    }
}

def build_route_one():
    global near_north, route_exit
    route_fence.clear()
    route_signs.clear()
    route_flowers.clear()
    forest_trees.clear()
    forest_bushes.clear()
    zigzag_path.clear()
    zigzag_bushes.clear()
    zigzag_trees.clear()
    obstacles.clear()

    CX = WORLD_W // 2
    TREE_W = TILE_SIZE
    TREE_H = TILE_SIZE * 2
    BORDER = 6 * TILE_SIZE
    PATH_W = 1 * TILE_SIZE
    for tx in range(0, WORLD_W, TILE_SIZE):
        if CX - PATH_W // 2 <= tx < CX + PATH_W // 2:
            continue
        r = pygame.Rect(tx, 0, TREE_W, TREE_H)
        zigzag_trees.append(r); obstacles.append(r)
    for ty in range(0, WORLD_H, TREE_H):
        for side in (0, WORLD_W - BORDER):
            for k in range(BORDER // TILE_SIZE):
                x = side + k * TILE_SIZE
                r = pygame.Rect(x, ty, TREE_W, TREE_H)
                zigzag_trees.append(r); obstacles.append(r)
    for py in range(TILE_SIZE * 2, WORLD_H - TILE_SIZE, TILE_SIZE):
        zigzag_path.append(pygame.Rect(CX, py, TILE_SIZE, TILE_SIZE))
    for side_x in (CX - 4 * TILE_SIZE, CX + TILE_SIZE):
        for (gy, gh) in [(TILE_SIZE * 6, 3), (TILE_SIZE * 12, 3),
                        (WORLD_H - TILE_SIZE * 10, 2)]:
            for r in range(gh):
                for c in range(3):
                    b = pygame.Rect(side_x + c * TILE_SIZE,
                                    gy + r * TILE_SIZE,
                                    TILE_SIZE, TILE_SIZE)
                    forest_bushes.append(b)
    for fx in range(0, WORLD_W, TILE_SIZE):
        if CX - TILE_SIZE // 2 <= fx < CX + TILE_SIZE // 2:
            continue
        r = pygame.Rect(fx, WORLD_H - TILE_SIZE, TILE_SIZE, TILE_SIZE)
        route_fence.append(r); obstacles.append(r)
    route_exit = pygame.Rect(CX - TILE_SIZE // 2, WORLD_H - TILE_SIZE, TILE_SIZE, TILE_SIZE)
    sign_rect = pygame.Rect(CX - TILE_SIZE // 2,
                            WORLD_H - TILE_SIZE * 3,
                            TILE_SIZE, TILE_SIZE)
    route_signs.append(sign_rect); obstacles.append(sign_rect)
    for fx, fy in [(BORDER + 2 * TILE_SIZE, TILE_SIZE * 5),
                   (BORDER + 4 * TILE_SIZE, TILE_SIZE * 9),
                   (BORDER + 1 * TILE_SIZE, TILE_SIZE * 14),
                   (WORLD_W - BORDER - 2 * TILE_SIZE, TILE_SIZE * 20),
                   (BORDER + 3 * TILE_SIZE, TILE_SIZE * 22)]:
        route_flowers.append(pygame.Rect(fx, fy, TILE_SIZE, TILE_SIZE))

    player.x = CX - player_width // 2
    player.y = WORLD_H - TILE_SIZE * 4
    near_north = False


def load_area(area_id):
    global WORLD_W, WORLD_H, current_area, world_id

    WORLD_W, WORLD_H = areas[area_id]["size"]
    current_area = areas[area_id]["name"]
    world_id = area_id

    update_map_size()
    show_area_name(current_area)
    if area_id == 1:
        obstacles.clear()
        for lst in (zigzag_path, zigzag_bushes, zigzag_trees,
                    forest_trees, forest_bushes, route_fence, route_signs, route_flowers):
            lst.clear()
        add_town_obstacles()
    elif area_id == 2:
        build_route_one()
def draw_text(text, x, y):
    
    img = font.render(text, True, BLACK)
    screen.blit(img, (x, y))
# status
def show_area_name(name):
    global area_banner_text
    global area_banner_timer
    global show_area_banner
    global banner_y

    area_banner_text = name
    area_banner_timer = pygame.time.get_ticks()
    show_area_banner = True
    banner_y = -80

player_status = None
enemy_status = None
has_running_shoes = False
is_sprinting = False
last_interact = 0
# UI

selected_move = 0
def reset_battle():
    global player_status, enemy_status, state
    global player_choice, enemy_choice, turn_order, selected_move
    global playerPokemon, enemy
    player_status = None
    enemy_status = None
    state = "player_input"
    selected_move = 0
    player_choice = None
    enemy_choice = None
    turn_order = []
    playerPokemon.stats["HP"] = playerPokemon.max_hp
    enemy.stats["HP"] = enemy.max_hp
def gain_xp(amount):
    global player_xp
    global player_level
    global xp_to_next
    global battle_message

    player_xp += amount

    if player_xp >= xp_to_next:

        player_xp -= xp_to_next
        player_level += 1
        xp_to_next += 25

        playerPokemon.max_hp += 10
        playerPokemon.stats["Attack"] += 5
        playerPokemon.stats["Speed"] += 3

        playerPokemon.stats["HP"] = playerPokemon.max_hp

        battle_message = f"{playerPokemon.name} leveled up to Lv {player_level}!"
        evolve_pokemon()
def evolve_pokemon():
    global playerPokemon, battle_message

    while (
        playerPokemon.evolution_level is not None
        and player_level >= playerPokemon.evolution_level
    ):

        next_name = playerPokemon.evolves_to

        if next_name not in POKEMON_DATABASE:
            break

        next_form = POKEMON_DATABASE[next_name]

        hp_ratio = playerPokemon.stats["HP"] / playerPokemon.max_hp

        playerPokemon = Pokemon(
            next_form.name,
            next_form.pokemon_types,
            next_form.stats["Speed"],
            next_form.stats["Attack"],
            next_form.max_hp,
            next_form.moves,
            next_form.evolution_level,
            next_form.evolves_to
        )

        playerPokemon.stats["HP"] = int(playerPokemon.max_hp * hp_ratio)

        battle_message = f"Your Pokémon evolved into {playerPokemon.name}!"
def draw_moves():
    current_moves = getattr(playerPokemon, "moves", [])
    for i, move in enumerate(current_moves):
        x = 100 if i % 2 == 0 else 300
        y = 250 if i < 2 else 300
        if i == selected_move:
            pygame.draw.rect(screen, (0, 200, 0), (x-10, y-5, 160, 30), 2)
        draw_text(move["name"], x, y)
def draw_hp_bar(x, y, hp, max_hp):
    ratio = max(0, min(1, hp / max_hp))
    pygame.draw.rect(screen, (200, 0, 0), (x, y, 200, 20))
    pygame.draw.rect(screen, (0, 200, 0), (x, y, 200 * ratio, 20))
    pygame.draw.rect(screen, BLACK, (x, y, 200, 20), 2)
def is_crit():
    return random.randint(1, 100) <= 10
def get_type_multiplier(move_type, defender_type):
    if move_type == "heal":
        return 1.0
    return TYPE_CHART.get(move_type, {}).get(defender_type, 1.0)
def decide_first():
    return "player" if playerPokemon.stats["Speed"] >= enemy.stats["Speed"] else "enemy"
def STAB(move_type, pokemon_types):
    if move_type in pokemon_types:
        return 1.5
    return 1.0
#pokemon and moves  
class Pokemon:
    MOVE_LIBRARY = {
        "Tackle": {"name": "Tackle", "damage": 10, "type": "normal"},
        "Fireball": {"name": "Fireball", "damage": 18, "type": "fire"},
        "Water Gun": {"name": "Water Gun", "damage": 14, "type": "water"},
        "Bubble": {"name": "Bubble","damage": 12,"type": "water"},
        "Heal": {"name": "Heal", "heal": 12, "type": "heal"},
        "Poison Sting": {"name": "Poison Sting", "damage": 6, "type": "poison"},
        "Quick Attack": {"name": "Quick Attack", "damage": 12, "type": "normal"},
        "Thunderbolt": {"name": "Thunderbolt", "damage": 20, "type": "electric"},
        "Ember": {"name": "Ember", "damage": 14, "type": "fire"},
        "Flamethrower": {"name": "Flamethrower", "damage": 18, "type": "fire"},
        "Vine Whip": {"name": "Vine Whip", "damage": 14, "type": "grass"},
        "Razor Leaf": {"name": "Razor Leaf", "damage": 16, "type": "grass"},
        "Body Slam": {"name": "Body Slam", "damage": 18, "type": "normal"},
        "Hyper Beam": {"name": "Hyper Beam", "damage": 22, "type": "normal"},
        "Shadow Pulse": {"name": "Shadow Pulse", "damage": 20, "type": "shadow"},
        "Light Beam": {"name": "Light Beam", "damage": 18, "type": "light"},

        "Crystal Spike": {"name": "Crystal Spike", "damage": 22, "type": "crystal"},

        "Sonic Boom": {"name": "Sonic Boom", "damage": 19, "type": "sound"},

        "Galaxy Burst": {"name": "Galaxy Burst", "damage": 25, "type": "cosmic"},
    }
    @classmethod
    def get_moves_for_type(cls, pokemon_type):

        valid_moves = []

        for move in cls.MOVE_LIBRARY.values():

            if (
                move["type"] == pokemon_type
                or move["type"] == "normal"
                or move["type"] == "heal"
            ):
                valid_moves.append(dict(move))

        # custom type bonus moves

        if pokemon_type == "shadow":
            valid_moves.append(cls.MOVE_LIBRARY["Shadow Pulse"])

        elif pokemon_type == "light":
            valid_moves.append(cls.MOVE_LIBRARY["Light Beam"])

        elif pokemon_type == "crystal":
            valid_moves.append(cls.MOVE_LIBRARY["Crystal Spike"])

        elif pokemon_type == "sound":
            valid_moves.append(cls.MOVE_LIBRARY["Sonic Boom"])

        elif pokemon_type == "cosmic":
            valid_moves.append(cls.MOVE_LIBRARY["Galaxy Burst"])

        return valid_moves
    @classmethod
    def random_moves_for_type(cls, pokemon_type, count=4):
        valid_moves = cls.get_moves_for_type(pokemon_type)

        if len(valid_moves) <= count:
            selected_moves = valid_moves[:]
        else:
            selected_moves = random.sample(valid_moves, k=count)

        random_moves = []
        for move in selected_moves:
            random_move = dict(move)
            if "damage" in random_move:
                random_move["damage"] = max(1, int(round(random_move["damage"] * random.uniform(0.85, 1.15))))
            random_moves.append(random_move)

        return random_moves
    def __init__(self,name, pokemon_types,Speed,attack,hp,moves=None,evolution_level=None,evolves_to=None):
        self.name = name
        self.pokemon_types = pokemon_types
        self.max_hp = hp
        self.stats = {
            "Speed": Speed,
            "Attack": attack,
            "HP": hp
        }
        self.moves = list((moves or [])[:4])
        self.evolution_level = evolution_level
        self.evolves_to = evolves_to

    @classmethod
    def make_moves(cls, *move_names):
        return [cls.MOVE_LIBRARY[name] for name in move_names]

    def apply_status(self, status): 
        if status == "poison":
            self.stats["HP"] -= 3
        elif status == "burn":
            self.stats["HP"] -= 6

#all pokemon            
pikachu = Pokemon(
    "Pikachu",
    ["electric"],
    100,
    55,
    90,
    Pokemon.get_moves_for_type("electric"),
    evolution_level=16,
    evolves_to="Raichu"
)

squirtle = Pokemon(
    "Squirtle",
    ["water"],
    43,
    48,
    130,
    Pokemon.make_moves("Water Gun", "Bubble", "Tackle", "Heal"),
    evolution_level=16,
    evolves_to="Wartortle"
)

wartortle = Pokemon(
    "Wartortle",
    ["water"],
    58,
    63,
    165,
    Pokemon.get_moves_for_type("water"),
    evolution_level=36,
    evolves_to="Blastoise"
)

blastoise = Pokemon(
    "Blastoise",
    ["water"],
    78,
    83,
    220,
    Pokemon.get_moves_for_type("water")
)
charmander = Pokemon(
    "Charmander",
    ["fire"],
    80,
    84,
    150,
    Pokemon.get_moves_for_type("fire"),
    evolution_level=16,
    evolves_to="Charmeleon"
)

charmeleon = Pokemon(
    "Charmeleon",
    ["fire"],
    105,
    109,
    190,
    Pokemon.get_moves_for_type("fire"),
    evolution_level=36,
    evolves_to="Charizard"
)

charizard = Pokemon(
    "Charizard",
    ["fire", "flying"],
    120,
    130,
    240,
    Pokemon.get_moves_for_type("fire"),
    evolution_level=None,
    evolves_to=None
)

bulbasaur = Pokemon(
    "Bulbasaur",
    ["grass", "poison"],
    45,
    49,
    120,
    Pokemon.get_moves_for_type("grass"),
    evolution_level=16,
    evolves_to="Ivysaur"
)

ivysaur = Pokemon(
    "Ivysaur",
    ["grass", "poison"],
    60,
    62,
    155,
    Pokemon.get_moves_for_type("grass"),
    evolution_level=32,
    evolves_to="Venusaur"
)

venusaur = Pokemon(
    "Venusaur",
    ["grass", "poison"],
    80,
    82,
    200,
    Pokemon.get_moves_for_type("grass")
)
raichu = Pokemon(
    "Raichu",
    ["electric"],
    130,
    90,
    180,
    Pokemon.get_moves_for_type("electric")
)
snorlax = Pokemon(
    "Snorlax",
    ["normal"],
    30,
    110,
    300,
    Pokemon.get_moves_for_type("normal")
)
wild_pokemon = [
("Pichu", ["electric"], 90, 40, 60, 50, "Pikachu"),
("Pikachu", ["electric"], 100, 55, 90, 40, "Raichu"),

("Magikarp", ["water"], 10, 20, 80, 60, "Gyarados"),
("Gyarados", ["water", "flying"], 81, 125, 190, 15, None),

("Geodude", ["rock", "ground"], 20, 80, 160, 20, "Graveler"),
("Graveler", ["rock", "ground"], 35, 95, 200, 12, "Golem"),

("Gastly", ["ghost", "poison"], 80, 60, 100, 15, "Haunter"),
("Haunter", ["ghost", "poison"], 95, 85, 140, 8, "Gengar"),

("Dratini", ["dragon"], 60, 60, 80, 25, "Dragonair"),
("Dragonair", ["dragon"], 80, 85, 140, 10, "Dragonite"),

("Eevee", ["normal"], 75, 65, 110, 30, "UmbreonX"),

("Flareon", ["fire"], 95, 110, 170, 15, "Luxflare"),

("Sparrow", ["sound"], 80, 60, 90, 25, "Echohawk"),

("Cosmite", ["psychic"], 80, 90, 120, 20, "Nebulon"),
]
rare_pokemon = [

    ("Crystagon", ["crystal", "dragon"], 70, 150, 250, 20),

    ("Nebulon", ["cosmic", "psychic"], 100, 130, 160, 20),

    ("UmbreonX", ["shadow"], 90, 120, 180, 20),

    ("Dragonite", ["dragon", "flying"], 100, 134, 220, 10),
]
POKEMON_DATABASE = {
    "Charmander": charmander,
    "Charmeleon": charmeleon,
    "Charizard": charizard,

    "Bulbasaur": bulbasaur,
    "Ivysaur": ivysaur,
    "Venusaur": venusaur,

    "Squirtle": squirtle,
    "Wartortle": wartortle,
    "Blastoise": blastoise,

    "Pikachu": pikachu,
    "Raichu": raichu,
}
playerPokemon = pikachu
enemy=charmander
print(f"{playerPokemon.stats['Speed']}")
print(f"{enemy.stats}")
playerPokemon.max_hp = 150
enemy.max_hp = 100 
for stat in enemy.stats:
    enemy.stats[stat] = int(round(enemy.stats[stat] * 0.9))
playerPokemon.stats["HP"] = playerPokemon.max_hp
enemy.stats["HP"] = enemy.max_hp

def use_move(user, move):
    global player_status, enemy_status, battle_message
    
    if user == "player":
        atk = playerPokemon.stats["Attack"]
        target = "enemy"
        attacker_pokemon = playerPokemon
        target_pokemon = enemy
    else:
        atk = enemy.stats["Attack"]
        target = "player"
        attacker_pokemon = enemy
        target_pokemon = playerPokemon

    message = f"{user.capitalize()} used {move['name']}"

    if move["type"] == "heal":
        if user == "player":
            playerPokemon.stats["HP"] = int(min(playerPokemon.stats["HP"] + move["heal"], playerPokemon.max_hp))
        else:
            enemy.stats["HP"] = int(min(enemy.stats["HP"] + move["heal"], enemy.max_hp))
        return message

    # damge
    
    damage = atk * (move["damage"] / 60) * 0.5
    stab_multiplier = STAB(
        move["type"],
        attacker_pokemon.pokemon_types
    )
    damage *= stab_multiplier
    if stab_multiplier > 1:
        message += " (STAB!)"
    if is_crit():
        damage *= 1.5
        message += " (CRIT!)"

    type_multiplier = 1

    for defender_type in target_pokemon.pokemon_types:
        type_multiplier *= get_type_multiplier(
            move["type"],
            defender_type
        )
    damage *= type_multiplier
    if type_multiplier > 1:
        message += " It's super effective!"
    elif type_multiplier < 1:
        message += " It's not very effective."
    damage = max(1, int(round(damage)))

    if target == "enemy":
        enemy.stats["HP"] -= damage
    else:
        playerPokemon.stats["HP"] -= damage
    if move["type"] == "fire" and random.randint(1,100) <= 20:
        if target == "enemy" and enemy_status is None:
            enemy_status = "burn"
            battle_message = "Enemy took burn damage."
        elif target == "player" and player_status is None:
            player_status = "burn"
            battle_message = "Player took burn damage."
    if move["type"] == "poison" and random.randint(1,100) <= 30:
        if target == "enemy" and enemy_status is None:
            enemy_status = "poison"
            battle_message = "Enemy took poison damage."
        elif target == "player" and player_status is None:
            player_status = "poison"
            battle_message = "Player took poison damage."
    return message
#  STATE MACHINE
starter_npc = pygame.Rect(
    300,
    180,
    TILE_SIZE,
    TILE_SIZE
)
state = "player_input"
battle_message = ""
timer = 0
delay = 1200 
starter_selected = False
choosing_starter = False
starter_index = 0
starter_choices = [
    bulbasaur,
    charmander,
    squirtle
]


player_choice = None
enemy_choice = None
turn_order = []
game_state = "world"
clock = pygame.time.Clock()
running=True

def get_tile_id(rect):
    return (rect.x // TILE_SIZE, rect.y // TILE_SIZE)
def draw(player, npc, camera_x, camera_y):
    global enemy, game_state, battle_message
    global show_area_banner
    global banner_y
    global area_banner_timer
    global area_banner_text

    if world_id == 1:
        screen.blit(pokemart_img, (pokemart_rect.x - camera_x, pokemart_rect.y - camera_y))
        screen.blit(pokecenter_img, (pokecenter_rect.x - camera_x, pokecenter_rect.y - camera_y))


        pygame.draw.rect(
            screen,
            (255, 0, 0),
            (
                lab_door_rect.x - camera_x,
                lab_door_rect.y - camera_y,
                lab_door_rect.width,
                lab_door_rect.height
            ),
            2
        )

    # draw grass
    for row in range(MAP_HEIGHT):
        for col in range(MAP_WIDTH):
            x = col * TILE_SIZE - camera_x
            y = row * TILE_SIZE - camera_y
            grass = grass_tiles[(row + col) % len(grass_tiles)]
            screen.blit(grass, (x, y))
    if world_id == 2:
        for tile in zigzag_path:
            screen.blit(
                path_tiles[0],
                (tile.x - camera_x, tile.y - camera_y)
            )
        for bush in zigzag_bushes:
            screen.blit(
                bush_tiles[0],
                (bush.x - camera_x, bush.y - camera_y)
            )

        for tree in zigzag_trees:
            screen.blit(
                tree_img,
                (tree.x - camera_x, tree.y - camera_y)
            )
    if world_id == 1:
        path_width = 3
        path_length = 20
        for i in range(22):

            x = PATH_LEFT - camera_x
            y = house_rect.y - (i * TILE_SIZE) - camera_y

            screen.blit(
                path_tiles[i % len(path_tiles)],
                (x, y)
            )
    if world_id == 1:
        for row in range(path_width):

            path_y = (
                house_rect.bottom
                + (row * TILE_SIZE)
                - camera_y
            )

            for i in range(path_length):

                x = (
                    house_rect.x
                    - 160
                    + (i * TILE_SIZE)
                    - camera_x
                )

                screen.blit(
                    path_tiles[i % len(path_tiles)],
                    (x, path_y)
                )


    if world_id == 2:
        for bush in forest_bushes:
            screen.blit(
                bush_tiles[0],
                (bush.x - camera_x, bush.y - camera_y)
            )

        for tree in forest_trees:
            screen.blit(
                tree_img,
                (tree.x - camera_x, tree.y - camera_y)
            )
        for f in route_fence:
            pygame.draw.rect(
                screen, (150, 150, 160),
                (f.x - camera_x, f.y - camera_y, f.width, f.height)
            )
            pygame.draw.rect(
                screen, (90, 90, 100),
                (f.x - camera_x + 4, f.y - camera_y + 4, f.width - 8, f.height - 8)
            )
        for s in route_signs:
            pygame.draw.rect(
                screen, (110, 110, 140),
                (s.x - camera_x, s.y - camera_y, s.width, s.height)
            )
            pygame.draw.rect(
                screen, (200, 200, 220),
                (s.x - camera_x + 5, s.y - camera_y + 5, s.width - 10, s.height - 10)
            )
        for fl in route_flowers:
            cx = fl.centerx - camera_x
            cy = fl.centery - camera_y
            pygame.draw.circle(screen, (220, 40, 40), (cx, cy), 6)
            pygame.draw.circle(screen, (255, 220, 120), (cx, cy), 2)
    if world_id == 1:
        screen.blit(tree_img, (tree_rect.x - camera_x, tree_rect.y - camera_y))
        screen.blit(house_img,(house_rect.x - camera_x, house_rect.y - camera_y))
        screen.blit(lab_img,(lab_rect.x - camera_x, lab_rect.y - camera_y))
        for bush in bush_encounters:
            screen.blit(
                bush_tiles[0],
                (bush.x - camera_x, bush.y - camera_y)
            )
        for bush in rare_bushes:
            screen.blit(
                bush_tiles[0],
                (bush.x - camera_x, bush.y - camera_y)
            )
        pygame.draw.rect(
            screen,
            "blue",
            npc.move(-camera_x, -camera_y)
        )
    player_screen = player.move(-camera_x, -camera_y)
    screen.blit(player_sprite, player_screen.topleft)
    if show_area_banner:

        if banner_y < 20:
            banner_y += 8

        pygame.draw.rect(
            screen,
            (240, 240, 240),
            (140, banner_y, 360, 60),
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            BLACK,
            (140, banner_y, 360, 60),
            4,
            border_radius=10
        )

        title_font = pygame.font.SysFont(None, 42)

        text_img = title_font.render(
            area_banner_text,
            True,
            BLACK
        )

        screen.blit(
            text_img,
            (
                320 - text_img.get_width() // 2,
                banner_y + 18
            )
        )

        if pygame.time.get_ticks() - area_banner_timer > 1000:
            banner_y -= 8

            if banner_y <= -80:
                show_area_banner = False
    return camera_x, camera_y
def get_camera(player):
    camera_x = max(0, min(WORLD_W - WIDTH, player.centerx - WIDTH // 2))
    camera_y = max(0, min(WORLD_H - HEIGHT, player.centery - HEIGHT // 2))
    return camera_x, camera_y


player_width = TILE_SIZE
player_height = TILE_SIZE 
player_vel=5
player_sprite = pygame.transform.scale(
    pygame.image.load("sprites/pokemonsprite_named/overworld_walk_down_01.png").convert_alpha(),
    (player_width, player_height),
)
npc=pygame.Rect(300,10 ,player_width,player_height)
player=pygame.Rect(200,HEIGHT - player_height,player_width,player_height)
camera_x, camera_y = get_camera(player)
draw(player, npc, camera_x, camera_y)


house_player = pygame.Rect(
    WIDTH // 2 - player_width // 2,
    HEIGHT - player_height - 24,
    player_width,
    player_height,
)

house_exit = pygame.Rect(
    WIDTH // 2 - 20 + 72,
    HEIGHT - 40,  
    70,
    40
)
walk_left= [
    pygame.transform.scale(
        pygame.image.load("sprites/pokemonsprite_named/overworld_walk_left_01.png").convert_alpha(),
        (player_width, player_height)
    ),
    pygame.transform.scale(
        pygame.image.load("sprites/pokemonsprite_named/overworld_walk_left_02.png").convert_alpha(),
        (player_width, player_height)
    ),
    pygame.transform.scale(
        pygame.image.load("sprites/pokemonsprite_named/overworld_walk_left_03.png").convert_alpha(),
        (player_width, player_height)
    ),
    pygame.transform.scale(
        pygame.image.load("sprites/pokemonsprite_named/overworld_walk_left_04.png").convert_alpha(),
        (player_width, player_height)
    )
]
walk_down = [
    pygame.transform.scale(
        pygame.image.load("sprites/pokemonsprite_named/overworld_walk_down_01.png").convert_alpha(),
        (player_width, player_height)
    ),
    pygame.transform.scale(
        pygame.image.load("sprites/pokemonsprite_named/overworld_walk_down_02.png").convert_alpha(),
        (player_width, player_height)
    ),
    pygame.transform.scale(
        pygame.image.load("sprites/pokemonsprite_named/overworld_walk_down_03.png").convert_alpha(),
        (player_width, player_height)
    ),
    pygame.transform.scale(
        pygame.image.load("sprites/pokemonsprite_named/overworld_walk_down_04.png").convert_alpha(),
        (player_width, player_height)
    )
]
walk_right = [
    pygame.transform.scale(
        pygame.image.load("sprites/pokemonsprite_named/overworld_walk_right_01.png").convert_alpha(),
        (player_width, player_height)
    ),
    pygame.transform.scale(
        pygame.image.load("sprites/pokemonsprite_named/overworld_walk_right_02.png").convert_alpha(),
        (player_width, player_height)
    ),
    pygame.transform.scale(
        pygame.image.load("sprites/pokemonsprite_named/overworld_walk_right_03.png").convert_alpha(),
        (player_width, player_height)
    ),
    pygame.transform.scale(
        pygame.image.load("sprites/pokemonsprite_named/overworld_walk_right_04.png").convert_alpha(),
        (player_width, player_height)
    )
]
walk_up= [
    pygame.transform.scale(
        pygame.image.load("sprites/pokemonsprite_named/overworld_walk_up_01.png").convert_alpha(),
        (player_width, player_height)
    ),
    pygame.transform.scale(
        pygame.image.load("sprites/pokemonsprite_named/overworld_walk_up_02.png").convert_alpha(),
        (player_width, player_height)
    ),
    pygame.transform.scale(
        pygame.image.load("sprites/pokemonsprite_named/overworld_walk_up_03.png").convert_alpha(),
        (player_width, player_height)
    ),
    pygame.transform.scale(
        pygame.image.load("sprites/pokemonsprite_named/overworld_walk_up_04.png").convert_alpha(),
        (player_width, player_height)
    )
]

#variables
# starter NPC inside house for testing
starter_npc = pygame.Rect(
    300,
    180,
    TILE_SIZE,
    TILE_SIZE
)
player_level = 5
player_xp = 0
xp_to_next = 50
frame = 0
direction = "down"
tile_size = 32
move_speed = 2
animation_speed = 0.35
moving = False
encountered_bushes = set()
steps_in_grass = 0
move_x = 0
move_y = 0
target_x = player.x
target_y = player.y
camera_x = 0
camera_y = 0
last_player_tile = None
leavehouse_img = pygame.image.load("leavehouse.png").convert_alpha()

leavehouse_img = pygame.transform.scale(
    leavehouse_img,
    (70, 40)
)
show_area_name("Pallet Town")
_headless = bool(os.environ.get("HEADLESS_TEST"))
while running and not _headless:  
    dt = clock.tick(60)
    screen.fill((0, 0, 0))
    if game_state == "world":
        desired_move = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            desired_move = (0, -1)
        elif keys[pygame.K_DOWN]:
            desired_move = (0, 1)
        elif keys[pygame.K_LEFT]:
            desired_move = (-1, 0)
        elif keys[pygame.K_RIGHT]:
            desired_move = (1, 0)
        if keys[pygame.K_x] and has_running_shoes:
            is_sprinting = True
        else:
            is_sprinting = False
    # start movement 
        if desired_move is None:
            if moving:
                moving = False
                move_x = 0
                move_y = 0
                target_x = round(player.x / tile_size) * tile_size
                target_y = round(player.y / tile_size) * tile_size
                player.x = target_x
                player.y = target_y
        else:
            move_x, move_y = desired_move
            moving = True
            if move_y < 0:
                direction = "up"
            elif move_y > 0:
                direction = "down"
            elif move_x < 0:
                direction = "left"
            else:
                direction = "right"
        if moving:
        # animation
            frame += animation_speed
            if direction == "down":
                if frame >= len(walk_down):
                    frame = 0
                player_sprite = walk_down[int(frame)]
            elif direction == "up":
                if frame >= len(walk_up):
                    frame = 0
                player_sprite = walk_up[int(frame)]
            elif direction == "left":
                if frame >= len(walk_left):
                    frame = 0
                player_sprite = walk_left[int(frame)]
            elif direction == "right":
                if frame >= len(walk_right):
                    frame = 0
                player_sprite = walk_right[int(frame)]
        # movement
            speed = sprint_speed if is_sprinting else base_speed
            prev_x = player.x
            player.x += move_x * speed
            player.x = max(0, min(WORLD_W - player_width, player.x))
            for obstacle in obstacles:
                if player.colliderect(obstacle):
                    if move_x > 0:
                        player.right = obstacle.left
                    elif move_x < 0:
                        player.left = obstacle.right
                    break
            prev_y = player.y
            player.y += move_y * speed
            player.y = max(0, min(WORLD_H - player_height, player.y))
            for obstacle in obstacles:
                if player.colliderect(obstacle):
                    if move_y > 0:
                        player.bottom = obstacle.top
                    elif move_y < 0:
                        player.top = obstacle.bottom
                    break
            blocked = (move_x != 0 and player.x == prev_x) or (move_y != 0 and player.y == prev_y)
            if blocked:
                moving = False
                move_x = 0
                move_y = 0
                target_x = player.x
                target_y = player.y
    # idle
        if not moving:
            if direction == "down":
                player_sprite = walk_down[0]
            elif direction == "up":
                player_sprite = walk_up[0]
            elif direction == "left":
                player_sprite = walk_left[0]
            elif direction == "right":
                player_sprite = walk_right[0]
    # Bounds
        player.x = max(0, min(WORLD_W - player_width, player.x))
        player.y = max(0, min(WORLD_H - player_height, player.y))
        if player.colliderect(door_rect):
            game_state = "house1"
            moving = False
            move_x = 0
            move_y = 0
            target_x = house_player.x
            target_y = house_player.y
            house_player.centerx = house_exit.centerx
            house_player.bottom = house_exit.top - 5
            pygame.display.flip()
            continue
        
        if player.colliderect(lab_door_rect):
            
            game_state = "insidelab"
            moving = False
            move_x = 0
            move_y = 0
            camera_x = 0
            camera_y = 0
            player.x = starter_npc.x
            player.y = starter_npc.bottom + 16
            target_x = player.x
            target_y = player.y
        if player.colliderect(pokemart_door):
            game_state = "pokemart"
        if player.colliderect(pokecenter_door):
            pass
        if world_id == 2 and player.colliderect(route_exit):
            load_area(1)
            show_area_name("Pallet Town")
            player.x = PATH_LEFT + TILE_SIZE // 2
            player.y = house_rect.bottom + 2 * TILE_SIZE
            player.x = max(0, min(WORLD_W - player_width, player.x))
            player.y = max(0, min(WORLD_H - player_height, player.y))
            target_x = player.x
            target_y = player.y
            moving = False
            move_x = 0
            move_y = 0


        if world_id == 1:
            near_north = player.colliderect(north_exit)
            if near_north and starter_selected:
                load_area(2)
                show_area_name("Route One")
        current_tile = get_tile_id(player)
        if current_tile != last_player_tile:
            last_player_tile = current_tile
            if starter_selected:
                for bush in bush_encounters + forest_bushes + rare_bushes:
                    if player.colliderect(bush):
                        if random.random() < 0.1:
                            if bush in rare_bushes:
                                pokemon_pool = rare_pokemon
                            else:
                                pokemon_pool = wild_pokemon

                            chosen = random.choices(
                                pokemon_pool,
                                weights=[p[5] for p in pokemon_pool],
                                k=1
                            )[0]
                            enemy = Pokemon(
                                chosen[0],
                                chosen[1],
                                chosen[2],
                                chosen[3],
                                chosen[4],
                                Pokemon.random_moves_for_type(chosen[1][0])
                            )

                            reset_battle()
                            battle_message = f"A wild {enemy.name} appeared!"
                            game_state = "battle"
                        break
        camera_x, camera_y = get_camera(player)
        draw(player, npc, camera_x, camera_y)
        current_camera_x = camera_x
        current_camera_y = camera_y
        pygame.display.flip()
    
    elif game_state == "insidelab":
        desired_move = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if choosing_starter and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    starter_index = (starter_index + 1) % len(starter_choices)
                elif event.key == pygame.K_LEFT:
                    starter_index = (starter_index - 1) % len(starter_choices)
                elif event.key == pygame.K_RETURN:
                    playerPokemon = starter_choices[starter_index]
                    starter_selected = True
                    choosing_starter = False
                    add_bush_obstacles()
        keys = pygame.key.get_pressed()  

        if not choosing_starter:
            if keys[pygame.K_UP]:
                desired_move = (0, -1)
            elif keys[pygame.K_DOWN]:
                desired_move = (0, 1)
            elif keys[pygame.K_LEFT]:
                desired_move = (-1, 0)
            elif keys[pygame.K_RIGHT]:
                desired_move = (1, 0)

            if desired_move is not None:
                move_x, move_y = desired_move
                player.x += move_x * base_speed
                player.y += move_y * base_speed
                player.x = max(0, min(WIDTH - player_width, player.x))
                player.y = max(0, min(HEIGHT - player_height, player.y))

                if move_y < 0:
                    direction = "up"
                elif move_y > 0:
                    direction = "down"
                elif move_x < 0:
                    direction = "left"
                else:
                    direction = "right"

                frame += animation_speed
                if direction == "up":
                    if frame >= len(walk_up):
                        frame = 0
                    player_sprite = walk_up[int(frame)]
                elif direction == "down":
                    if frame >= len(walk_down):
                        frame = 0
                    player_sprite = walk_down[int(frame)]
                elif direction == "left":
                    if frame >= len(walk_left):
                        frame = 0
                    player_sprite = walk_left[int(frame)]
                elif direction == "right":
                    if frame >= len(walk_right):
                        frame = 0
                    player_sprite = walk_right[int(frame)]
            else:
                if direction == "up":
                    player_sprite = walk_up[0]
                elif direction == "down":
                    player_sprite = walk_down[0]
                elif direction == "left":
                    player_sprite = walk_left[0]
                else:
                    player_sprite = walk_right[0]
        screen.blit(INSIDE_LAB_BG, (0, 0))
        draw_text("Inside Lab - Choose Starter", 120, 40)
        pygame.draw.rect(screen, "blue", starter_npc)
        draw_text("Professor", starter_npc.x, starter_npc.y - 20)
        screen.blit(player_sprite, (player.x - camera_x, player.y - camera_y))

        if player.colliderect(starter_npc) and not starter_selected:
            choosing_starter = True

        
        if not choosing_starter and player.colliderect(lab_exit_rect):
            game_state = "world"
            player.centerx = lab_door_rect.centerx
            player.y = lab_rect.bottom + 10
            camera_x, camera_y = get_camera(player)

        if choosing_starter:
            screen.fill((255, 255, 255))
            draw_text("Choose Your Starter", 180, 60)

            for i, pokemon in enumerate(starter_choices):
                box_x = 70 + (i * 180)
                box_y = 160
                box_w = 140
                box_h = 140

                if pokemon.name == "Charmander":
                    bg_color = (255, 80, 80)
                elif pokemon.name == "Squirtle":
                    bg_color = (80, 160, 255)
                elif pokemon.name == "Bulbasaur":
                    bg_color = (100, 220, 100)

                pygame.draw.rect(screen, bg_color, (box_x, box_y, box_w, box_h))

                if "poison" in pokemon.pokemon_types:
                    pygame.draw.rect(
                        screen,
                        (180, 80, 255),
                        (box_x, box_y + 100, box_w, 40)
                    )

                if i == starter_index:
                    pygame.draw.rect(screen, (255, 255, 0), (box_x, box_y, box_w, box_h), 5)
                else:
                    pygame.draw.rect(screen, BLACK, (box_x, box_y, box_w, box_h), 3)

                draw_text(pokemon.name, box_x + 20, box_y + 30)
                draw_text("ENTER to choose", box_x + 5, box_y + 80)

        pygame.display.flip()
    elif game_state == "house1":
        desired_move = None
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            desired_move = (0, -1)
        elif keys[pygame.K_DOWN]:
            desired_move = (0, 1)
        elif keys[pygame.K_LEFT]:
            desired_move = (-1, 0)
        elif keys[pygame.K_RIGHT]:
            desired_move = (1, 0)
        if house_player.colliderect(house_exit):
            game_state = "world"
            player.centerx = door_touch_rect.centerx
            player.y = min(WORLD_H - player_height, door_touch_rect.bottom + 16)
            moving = False
            move_x = 0
            move_y = 0
            target_x = player.x
            target_y = player.y
            pygame.display.flip()
            continue
        if keys[pygame.K_e]:
            print(starter_choices)
        
          
        if keys[pygame.K_x] and has_running_shoes:
            is_sprinting = True
        else:
            is_sprinting = False
    # start movement
        if desired_move is None:
            if moving:
                moving = False
                move_x = 0
                move_y = 0
        elif not moving:
            move_x, move_y = desired_move
            moving = True
            if move_y < 0:
                direction = "up"
            elif move_y > 0:
                direction = "down"
            elif move_x < 0:
                direction = "left"
            else:
                direction = "right"
            target_x = house_player.x + move_x * tile_size
            target_y = house_player.y + move_y * tile_size
            target_x = max(0, min(WIDTH - player_width, target_x))
            target_y = max(0, min(HEIGHT - player_height, target_y))
            if target_x == house_player.x and target_y == house_player.y:
                moving = False
                move_x = 0
                move_y = 0
                target_x = house_player.x
                target_y = house_player.y
        elif moving and house_player.x == target_x and house_player.y == target_y:
            move_x, move_y = desired_move
            if move_y < 0:
                direction = "up"
            elif move_y > 0:
                direction = "down"
            elif move_x < 0:
                direction = "left"
            else:
                direction = "right"
            target_x = house_player.x + move_x * tile_size
            target_y = house_player.y + move_y * tile_size
            target_x = max(0, min(WIDTH - player_width, target_x))
            target_y = max(0, min(HEIGHT - player_height, target_y))
        if moving:
        # animation
            frame += animation_speed
            if direction == "down":
                if frame >= len(walk_down):
                    frame = 0
                player_sprite = walk_down[int(frame)]
            elif direction == "up":
                if frame >= len(walk_up):
                    frame = 0
                player_sprite = walk_up[int(frame)]
            elif direction == "left":
                if frame >= len(walk_left):
                    frame = 0
                player_sprite = walk_left[int(frame)]
            elif direction == "right":
                if frame >= len(walk_right):
                    frame = 0
                player_sprite = walk_right[int(frame)]
        # movement
            speed = sprint_speed if is_sprinting else base_speed
            if house_player.x < target_x:
                house_player.x += speed
            elif house_player.x > target_x:
                house_player.x -= speed
            if house_player.y < target_y:
                house_player.y += speed
            elif house_player.y > target_y:
                house_player.y -= speed
        # snapping
            if abs(house_player.x - target_x) <= speed:
                house_player.x = target_x
            if abs(house_player.y - target_y) <= speed:
                house_player.y = target_y
        #stop movement
            if house_player.x == target_x and house_player.y == target_y:
                moving = False
    # idle
        if not moving:
            if direction == "down":
                player_sprite = walk_down[0]
            elif direction == "up":
                player_sprite = walk_up[0]
            elif direction == "left":
                player_sprite = walk_left[0]
            elif direction == "right":
                player_sprite = walk_right[0]
        house_player.x = max(0, min(WIDTH - player_width, house_player.x))
        house_player.y = max(0, min(HEIGHT - player_height, house_player.y))
        npc_runningshoes = pygame.Rect(100, 200, TILE_SIZE, TILE_SIZE)
        screen.blit(HOUSE_BG, (0, 0))
        if keys[pygame.K_x] and house_player.colliderect(npc_runningshoes):
            if pygame.time.get_ticks() - last_interact > 1000:
                has_running_shoes = True
                last_interact = pygame.time.get_ticks()
        screen.blit(player_sprite, house_player.topleft) 
        draw_text("Press X on the red box to get Sprint Shoes", 20, 20)
        pygame.draw.rect(screen, "red", npc_runningshoes)
        draw_text("Sprint Shoes", 100, 170)
        screen.blit(leavehouse_img, house_exit.topleft)
       
        pygame.display.flip()
    elif game_state == "battle":
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif state == "player_input" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and selected_move % 2 == 0:
                    selected_move += 1
                elif event.key == pygame.K_LEFT and selected_move % 2 == 1:
                    selected_move -= 1
                elif event.key == pygame.K_DOWN and selected_move < 2:
                    selected_move += 2
                elif event.key == pygame.K_UP and selected_move >= 2:
                    selected_move -= 2
                elif event.key == pygame.K_RETURN:

                    if selected_move >= len(playerPokemon.moves):
                        continue
                    player_choice = playerPokemon.moves[selected_move]
                    enemy_choice = random.choice(enemy.moves)
                    if decide_first() == "player":
                        turn_order = [("player", player_choice), ("enemy", enemy_choice)]
                    else:
                        turn_order = [("enemy", enemy_choice), ("player", player_choice)]
                    state = "action"
                    timer = pygame.time.get_ticks()
        draw_text(
            f"{playerPokemon.name} Lv {player_level}",
            60,
            20
        )
        draw_text(
            f"XP: {player_xp}/{xp_to_next}",
            60,
            130
        )
        draw_text(enemy.name, 380, 20)
        draw_hp_bar(60, 72, playerPokemon.stats["HP"], playerPokemon.max_hp)
        draw_hp_bar(380, 72, enemy.stats["HP"], enemy.max_hp)
        if player_status:
            draw_text("Status: " + player_status, 60, 104)
        if enemy_status:
            draw_text("Status: " + enemy_status, 380, 104)
        draw_moves()
        draw_text(battle_message, 60, 330)
    #  STATE LOGIC 
        if state == "action":
            if pygame.time.get_ticks() - timer > delay:
                if turn_order:
                    user, move = turn_order.pop(0)
                    battle_message = use_move(user, move)
                    timer = pygame.time.get_ticks()
                else:
                    playerPokemon.apply_status(player_status)
                    enemy.apply_status(enemy_status)
                    playerPokemon.stats["HP"] = int(max(0, playerPokemon.stats["HP"]))
                    enemy.stats["HP"] = int(max(0, enemy.stats["HP"]))
                    state = "player_input"
    # win check
        if playerPokemon.stats["HP"] <= 0:
            draw_text("You Lost!", 250, 200)
            game_state ="world"
        elif enemy.stats["HP"] <= 0:

            playerPokemon.stats["Attack"] += random.randint(2, 4)
            playerPokemon.stats["Speed"] += random.randint(1, 3)

            gain_xp(25)
            

            draw_text("You Won!", 250, 200)

            pygame.display.flip()

            pygame.time.delay(1000)

            game_state = "world"
        pygame.display.flip()
pygame.quit()