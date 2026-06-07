import pygame
import random
import time
# FIRST 6 GRASS TILES
pygame.init()
WIDTH, HEIGHT = 640, 480
TILE_SIZE = 32
base_speed = 2
sprint_speed = 4
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Pokemon Battle")
grass_tiles = []
path_tiles = []
bush_tiles = []

bush_img = pygame.image.load(
    "sprites/ground_tiles_assorted/tile_r02_c00.png"
).convert()

bush_img = pygame.transform.scale(
    bush_img,
    (TILE_SIZE, TILE_SIZE)
)

bush_tiles.append(bush_img)
for i in range(6):
    img = pygame.image.load("sprites/ground_tiles_assorted/tile_r00_c00.png").convert()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    grass_tiles.append(img)
# PATH TILES (ROW 14)
for i in range(8):
    img = pygame.image.load(
        f"sprites/ground_tiles_assorted/tile_r14_c00.png"
    ).convert()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    path_tiles.append(img)
WORLD_W, WORLD_H = 2000, 1200
MAP_WIDTH = WORLD_W // TILE_SIZE
MAP_HEIGHT = WORLD_H // TILE_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Pokemon Battle")
font = pygame.font.SysFont(None, 30)
HOUSE_BG = pygame.transform.scale(
    pygame.image.load("inhouse.png").convert(),
    (WIDTH, HEIGHT)
)
decor_sheet = pygame.image.load("download (2).png").convert()
decor_bg_color = decor_sheet.get_at((decor_sheet.get_width() - 1, 0))
leavehouse_img = pygame.image.load("leavehouse.png").convert_alpha()

leavehouse_img = pygame.transform.scale(
    leavehouse_img,
    (96, 96)
)
def clean_grass_edges(sprite, bg_color, threshold=12):
    """Normalize near-bg pixels so the colorkey removes grass artifacts cleanly."""
    bg_r, bg_g, bg_b = bg_color.r, bg_color.g, bg_color.b
    w, h = sprite.get_size()
    for y in range(h):
        for x in range(w):
            pixel = sprite.get_at((x, y))
            if abs(pixel.r - bg_r) <= threshold and abs(pixel.g - bg_g) <= threshold and abs(pixel.b - bg_b) <= threshold:
                sprite.set_at((x, y), (bg_r, bg_g, bg_b))
    sprite.set_colorkey((bg_r, bg_g, bg_b))
    return sprite

TREE_SRC = pygame.Rect(0, 0, 74, 98)
HOUSE_SRC = pygame.Rect(76, 42, 132, 95)
DOOR_SRC = pygame.Rect(131, 89, 16, 29)

tree_img = clean_grass_edges(decor_sheet.subsurface(TREE_SRC).copy().convert(), decor_bg_color)
house_img = clean_grass_edges(decor_sheet.subsurface(HOUSE_SRC).copy().convert(), decor_bg_color)
door_local_rect = pygame.Rect(
    DOOR_SRC.x - HOUSE_SRC.x,
    DOOR_SRC.y - HOUSE_SRC.y,
    DOOR_SRC.width,
    DOOR_SRC.height,
)

# SCALE FACTOR
scale = 2

# Upscale images
tree_img = pygame.transform.scale(
    tree_img,
    (TREE_SRC.width * scale, TREE_SRC.height * scale)
)

house_img = pygame.transform.scale(
    house_img,
    (HOUSE_SRC.width * scale, HOUSE_SRC.height * scale)
)

bush_encounters = []

tree_rect = tree_img.get_rect(topleft=(560, 260))
house_rect = house_img.get_rect(topleft=(700, 360))
door_rect = pygame.Rect(
    house_rect.x + (door_local_rect.x * scale),
    house_rect.y + (door_local_rect.y * scale),
    door_local_rect.width * scale,
    door_local_rect.height * scale,
)

# Adjust hitboxes for new size
tree_hitbox = pygame.Rect(
    tree_rect.x + 30,
    tree_rect.bottom - 50,
    tree_rect.width - 60,
    50
)

house_hitbox = pygame.Rect(
    house_rect.x + 24,
    house_rect.y + 104,
    house_rect.width - 48,
    house_rect.height - 116,
)
door_gap = door_rect.inflate(60, 20)
house_left_hitbox = pygame.Rect(
    house_hitbox.x,
    house_hitbox.y,
    max(0, door_gap.x - house_hitbox.x),
    house_hitbox.height,
)
house_right_hitbox = pygame.Rect(
    door_gap.right,
    house_hitbox.y,
    max(0, house_hitbox.right - door_gap.right),
    house_hitbox.height,
)
door_touch_rect = pygame.Rect(
    door_rect.x - 12,
    door_rect.y + 6,
    door_rect.width + 24,
    door_rect.height + 8,
)
starter_npc = pygame.Rect(300, 180, TILE_SIZE, TILE_SIZE)
starter_selected = False

# Create a fixed clump of bushes in front of the house instead of random scattered ones.
clump_start_x = max(0, house_rect.left - 3 * TILE_SIZE)
clump_start_y = house_rect.bottom + TILE_SIZE
clump_rows = 3
clump_cols = 4

for row in range(clump_rows):
    for col in range(clump_cols):
        x = clump_start_x + col * TILE_SIZE
        y = clump_start_y + row * TILE_SIZE
        bush_encounters.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))

obstacles = [tree_hitbox, house_left_hitbox, house_right_hitbox]


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

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
    }
}
def draw_text(text, x, y):
    img = font.render(text, True, BLACK)
    screen.blit(img, (x, y))


# STATUS
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

def STAB(move_type,pokemon_type):
    if move_type == pokemon_type:
        return 1.5
    return 1.0

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
    def __init__(self, name, pokemon_type, Speed, attack, hp, moves=None):
        self.name = name
        self.pokemon_type = pokemon_type
        self.max_hp = hp
        self.stats = {
            "Speed": Speed,
            "Attack": attack,
            "HP": hp
        }
        self.moves = list((moves or [])[:4])

    @classmethod
    def make_moves(cls, *move_names):
        return [cls.MOVE_LIBRARY[name] for name in move_names]

    def apply_status(self, status): 
        if status == "poison":
            self.stats["HP"] -= 3
        elif status == "burn":
            self.stats["HP"] -= 6

            
pikachu = Pokemon("Pikachu","electric",100,55,90,Pokemon.get_moves_for_type("electric"))
squirtle = Pokemon("Squirtle","water",43,48,130,Pokemon.make_moves("Water Gun","Bubble","Tackle","Heal"))
charmander = Pokemon("Charmander", "fire", 80, 84, 150, Pokemon.get_moves_for_type("fire"))
bulbasaur = Pokemon("Bulbasaur", "grass", 45, 49, 120, Pokemon.get_moves_for_type("grass"))
snorlax = Pokemon("Snorlax", "normal", 30, 110, 300, Pokemon.get_moves_for_type("normal"))
wild_pokemon = [
    ("Pikachu", "electric", 100, 55, 90, 40),
    ("Charmander", "fire", 80, 84, 150, 30),
    ("Bulbasaur", "grass", 45, 49, 120, 20),
    ("Snorlax", "normal", 30, 110, 300, 10),
]
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
    stab_multiplier = STAB(move["type"], attacker_pokemon.pokemon_type)
    damage *= stab_multiplier
    if stab_multiplier > 1:
        message += " (STAB!)"
    if is_crit():
        damage *= 1.5
        message += " (CRIT!)"

    type_multiplier = get_type_multiplier(move["type"], target_pokemon.pokemon_type)
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

    # STATUS EFFECTS
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

# ===== STATE MACHINE =====
starter_npc = pygame.Rect(300, 180, TILE_SIZE, TILE_SIZE)
state = "player_input"
battle_message = ""
timer = 0
delay = 1200  # ms
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
def draw(player, npc):

    camera_x = max(
        0,
        min(WORLD_W - WIDTH, player.centerx - WIDTH // 2)
    )

    camera_y = max(
        0,
        min(WORLD_H - HEIGHT, player.centery - HEIGHT // 2)
    )

    # =========================
    # DRAW GRASS MAP
    # =========================
    for row in range(MAP_HEIGHT):

        for col in range(MAP_WIDTH):

            x = col * TILE_SIZE - camera_x
            y = row * TILE_SIZE - camera_y

            grass = grass_tiles[(row + col) % len(grass_tiles)]
        
            screen.blit(grass, (x, y))

    # =========================
    # PATH TO HOUSE
    # =========================

    path_y = house_rect.bottom - camera_y

    for i in range(8):

        x = (house_rect.x - 64 + i * TILE_SIZE) - camera_x

        screen.blit(path_tiles[i % len(path_tiles)], (x, path_y))
    # 🌿 RANDOM WILD ENCOUNTERS
    for bush in bush_encounters:

        bush_id = (bush.x, bush.y)

        if player.colliderect(bush):

            if bush_id not in encountered_bushes:

                encountered_bushes.add(bush_id)

                if random.randint(1, 100) <= 20:

                    chosen = random.choices(
                        wild_pokemon,
                        weights=[pokemon[5] for pokemon in wild_pokemon],
                        k=1
                    )[0]

                    enemy = Pokemon(
                        chosen[0],
                        chosen[1],
                        chosen[2],
                        chosen[3],
                        chosen[4],
                        Pokemon.random_moves_for_type(chosen[1])
                    )

                    reset_battle()

                    battle_message = f"A wild {enemy.name} appeared!"

                    game_state = "battle"

            break

        else:
            bush_id = (bush.x, bush.y)

            if bush_id in encountered_bushes:
                encountered_bushes.remove(bush_id)
    # =========================
    # DRAW BUSHES
    # =========================

    for bush in bush_encounters:

        screen.blit(
            bush_tiles[0],
            (bush.x - camera_x, bush.y - camera_y)
        )
   # =========================
    # OBJECTS
    # =========================
    screen.blit(tree_img, (tree_rect.x - camera_x, tree_rect.y - camera_y))

    screen.blit(
        house_img,
        (house_rect.x - camera_x, house_rect.y - camera_y)
    )

    player_screen = player.move(-camera_x, -camera_y)

    screen.blit(player_sprite, player_screen.topleft)

    pygame.draw.rect(
        screen,
        "blue",
        npc.move(-camera_x, -camera_y)
    )
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
house_player = pygame.Rect(
    WIDTH // 2 - player_width // 2,
    HEIGHT - player_height - 24,
    player_width,
    player_height,
)
# Plant/exit trigger inside the house.
house_exit = pygame.Rect(WIDTH // 2 + 120, HEIGHT - 110, 96, 96)


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
while running:
    
    dt = clock.tick(60)
    screen.fill((0, 0, 0))
    if game_state == "world":
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_x] and has_running_shoes:
            is_sprinting = True
        else:
            is_sprinting = False

    # =========================
    # START MOVEMENT
    # =========================
        if not moving:

            if keys[pygame.K_UP]:
                move_y = -1
                move_x = 0
                moving = True
                direction = "up"

            elif keys[pygame.K_DOWN]:
                move_y = 1
                move_x = 0
                moving = True
                direction = "down"

            elif keys[pygame.K_LEFT]:
                move_x = -1
                move_y = 0
                moving = True
                direction = "left"

            elif keys[pygame.K_RIGHT]:
                move_x = 1
                move_y = 0
                moving = True
                direction = "right"

        # Set tile target
            if moving:
                target_x = player.x + move_x * tile_size
                target_y = player.y + move_y * tile_size
                target_x = max(0, min(WORLD_W - player_width, target_x))
                target_y = max(0, min(WORLD_H - player_height, target_y))

                if target_x == player.x and target_y == player.y:
                    moving = False

    # =========================
    # MOVEMENT + ANIMATION
    # =========================
        if moving:

        # ANIMATION
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


        # MOVEMENT
            speed = sprint_speed if is_sprinting else base_speed

            if player.x < target_x:
                player.x += speed
            elif player.x > target_x:
                player.x -= speed

            if player.y < target_y:
                player.y += speed
            elif player.y > target_y:
                player.y -= speed
        # SNAP TO TILE
    

        
            if abs(player.x - target_x) <= speed:
                player.x = target_x

            if abs(player.y - target_y) <= speed:
                player.y = target_y

        # STOP MOVEMENT
            if player.x == target_x and player.y == target_y:
                moving = False

    # =========================
    # IDLE SPRITE
    # =========================
        if not moving:

            if direction == "down":
                player_sprite = walk_down[0]

            elif direction == "up":
                player_sprite = walk_up[0]

            elif direction == "left":
                player_sprite = walk_left[0]

            elif direction == "right":
                player_sprite = walk_right[0]

    # =========================
    # WORLD BOUNDS
    # =========================
        player.x = max(0, min(WORLD_W - player_width, player.x))
        player.y = max(0, min(WORLD_H - player_height, player.y))

        if player.colliderect(door_rect):
            game_state = "house1"
            moving = False
            move_x = 0
            move_y = 0
            target_x = house_player.x
            target_y = house_player.y
            house_player.centerx = WIDTH // 2
            house_player.bottom = HEIGHT - 80
            pygame.display.flip()
            continue

        for obstacle in obstacles:

            if player.colliderect(obstacle):

                player.x = target_x - (move_x * tile_size)
                player.y = target_y - (move_y * tile_size)

                moving = False

                break

        # 🌿 RANDOM WILD ENCOUNTERS
        for bush in bush_encounters:

            if player.colliderect(bush) and not moving:

                if random.randint(1, 100) <= 20:

                    chosen = random.choices(
                        wild_pokemon,
                        weights=[pokemon[5] for pokemon in wild_pokemon],
                        k=1
                    )[0]

                    enemy = Pokemon(
                        chosen[0],
                        chosen[1],
                        chosen[2],
                        chosen[3],
                        chosen[4],
                        Pokemon.random_moves_for_type(chosen[1])
                    )

                    reset_battle()

                    battle_message = f"A wild {enemy.name} appeared!"

                    game_state = "battle"

                break
               
    


        

        camera_x, camera_y = draw(player, npc)

        pygame.display.flip()

    elif game_state == "house1":
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        pygame.draw.rect(screen, "blue", starter_npc)

        draw_text("Professor", starter_npc.x - 10, starter_npc.y - 20)

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
        if keys[pygame.K_x] and house_player.colliderect(starter_npc):

            if not starter_selected and not choosing_starter:
                choosing_starter = True
        if choosing_starter:

            pygame.draw.rect(screen, (220, 220, 220), (80, 120, 480, 200))

            draw_text("Choose Your Starter", 180, 140)

            for i, pokemon in enumerate(starter_choices):

                x = 120 + i * 140
                y = 220

                draw_text(pokemon.name, x, y)

                if i == starter_index:
                    pygame.draw.rect(screen, (255, 0, 0), (x - 10, y - 10, 120, 40), 3)
        if choosing_starter and event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RIGHT:
                starter_index = min(starter_index + 1, 2)

            elif event.key == pygame.K_LEFT:
                starter_index = max(starter_index - 1, 0)

            elif event.key == pygame.K_RETURN:

                playerPokemon = starter_choices[starter_index]

                starter_selected = True
                choosing_starter = False

                battle_message = f"You chose {playerPokemon.name}!"
        
        if starter_selected:
            draw_text(
                f"Starter: {playerPokemon.name}",
                20,
                60
            )
        else:
            draw_text(
                "Press X to choose starter",
            20,
                60
            )


        if keys[pygame.K_x] and has_running_shoes:
            is_sprinting = True
        else:
            is_sprinting = False
            
            

    # =========================
    # START MOVEMENT
    # =========================
        if not moving:

            if keys[pygame.K_UP]:
                move_y = -1
                move_x = 0
                moving = True
                direction = "up"

            elif keys[pygame.K_DOWN]:
                move_y = 1
                move_x = 0
                moving = True
                direction = "down"

            elif keys[pygame.K_LEFT]:
                move_x = -1
                move_y = 0
                moving = True
                direction = "left"
                

            elif keys[pygame.K_RIGHT]:
                move_x = 1
                move_y = 0
                moving = True
                direction = "right"

        # Set tile target
            if moving:
                target_x = house_player.x + move_x * tile_size
                target_y = house_player.y + move_y * tile_size
                target_x = max(0, min(WIDTH - player_width, target_x))
                target_y = max(0, min(HEIGHT - player_height, target_y))

                if target_x == house_player.x and target_y == house_player.y:
                    moving = False

    # =========================
    # MOVEMENT + ANIMATION
    # =========================
        if moving:

        # ANIMATION
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

        # MOVEMENT
            speed = sprint_speed if is_sprinting else base_speed

            if house_player.x < target_x:
                house_player.x += speed
            elif house_player.x > target_x:
                house_player.x -= speed

            if house_player.y < target_y:
                house_player.y += speed
            elif house_player.y > target_y:
                house_player.y -= speed

        # SNAP TO TILE
            if abs(house_player.x - target_x) <= speed:
                house_player.x = target_x

            if abs(house_player.y - target_y) <= speed:
                house_player.y = target_y

        # STOP MOVEMENT
            if house_player.x == target_x and house_player.y == target_y:
                moving = False

    # =========================
    # IDLE SPRITE
    # =========================
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
        
        pygame.draw.rect(screen, "blue", starter_npc)

        draw_text("Starter NPC", starter_npc.x - 20, starter_npc.y - 20)
        draw_text("Press X on the red box to get Sprint Shoes", 20, 20)
        pygame.draw.rect(screen, "red", npc_runningshoes)
        draw_text("Sprint Shoes", 100, 170)
        screen.blit(leavehouse_img, house_exit.topleft)

        draw_text(
            "Press X to leave",
            house_exit.x - 10,
            house_exit.y - 25
        )
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
                    player_choice = playerPokemon.moves[selected_move]
                    enemy_choice = random.choice(enemy.moves)

                    if decide_first() == "player":
                        turn_order = [("player", player_choice), ("enemy", enemy_choice)]
                    else:
                        turn_order = [("enemy", enemy_choice), ("player", player_choice)]

                    state = "action"
                    timer = pygame.time.get_ticks()

        draw_text(playerPokemon.name, 60, 20)
        draw_text(enemy.name, 380, 20)

        draw_hp_bar(60, 72, playerPokemon.stats["HP"], playerPokemon.max_hp)
        draw_hp_bar(380, 72, enemy.stats["HP"], enemy.max_hp)

        if player_status:
            draw_text("Status: " + player_status, 60, 104)
        if enemy_status:
            draw_text("Status: " + enemy_status, 380, 104)

        draw_moves()
        draw_text(battle_message, 60, 330)

    # ===== STATE LOGIC =====
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

    # WIN CHECK
        if playerPokemon.stats["HP"] <= 0:
            draw_text("You Lost!", 250, 200)
            game_state ="world"
        elif enemy.stats["HP"] <= 0:
            draw_text("You Won!", 250, 200)
            game_state ="world"

        pygame.display.flip()

pygame.quit()

