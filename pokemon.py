import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Pokemon Battle")

font = pygame.font.SysFont(None, 30)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def draw_text(text, x, y):
    img = font.render(text, True, BLACK)
    screen.blit(img, (x, y))

# MOVES
enemymoves = [
    {"name": "Tackle", "damage": 8, "type": "attack"},
    {"name": "Fireball", "damage": 16, "type": "fire"},
    {"name": "Heal", "heal": 10, "type": "heal"},
    {"name": "Poison Sting", "damage": 4, "type": "poison"}
]

playermoves = [
    {"name": "Tackle", "damage": 10, "type": "attack"},
    {"name": "Fireball", "damage": 18, "type": "fire"},
    {"name": "Heal", "heal": 12, "type": "heal"},
    {"name": "Poison Sting", "damage": 6, "type": "poison"}
]

# STATS

# HP


# STATUS
player_status = None
enemy_status = None

# UI
selected_move = 0

def draw_moves():
    for i, move in enumerate(playermoves):
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

def decide_first():
    return "player" if player.stats["Speed"] >= enemy.stats["Speed"] else "enemy"


class Pokemon:
    def __init__(self, name, Speed, attack, hp):
        self.name = name
        self.max_hp = hp
        # makes it a dictionary
        self.stats = {
            "Speed": Speed,
            "Attack": attack,
            "HP": hp
            
        }
    def apply_status(self, status):
        if status == "poison":
            self.stats["HP"] -= 3
        elif status == "burn":
            self.stats["HP"] -= 6
            

pikachu = Pokemon("Pikachu", 100, 55, 90)
charizard = Pokemon("Charizard", 80, 84, 150)
bulbasaur = Pokemon("Bulbasaur", 45, 49, 120)
snorlax = Pokemon("Snorlax", 30, 110, 300)
player = pikachu
enemy=charizard
print(f"{player.stats['Speed']}")
print(f"{enemy.stats}")
player.max_hp = 150
enemy.max_hp = 100 
for stat in enemy.stats:
    enemy.stats[stat] *= 0.9

player.stats["HP"] = player.max_hp
enemy.stats["HP"] = enemy.max_hp
def use_move(user, move):
    global player_status, enemy_status, battle_message
    
    if user == "player":
        atk = player.stats["Attack"]
        target = "enemy"
    else:
        atk = enemy.stats["Attack"]
        target = "player"

    message = f"{user.capitalize()} used {move['name']}"

    if move["type"] == "heal":
        if user == "player":
            player.stats["HP"] = min(player.stats["HP"] + move["heal"], player.max_hp)
        else:
            enemy.stats["HP"] = min(enemy.stats["HP"] + move["heal"], enemy.max_hp)
        return message

    # damge
    damage = atk * (move["damage"] / 60) * 0.5
    if is_crit():
        damage *= 1.5
        message += " (CRIT!)"

    if target == "enemy":
        enemy.stats["HP"] -= damage
    else:
        player.stats["HP"] -= damage

    # STATUS EFFECTS
    if move["type"] == "fire" and random.randint(1,100) <= 20:
        if target == "enemy" and enemy_status is None:
            enemy_status = "burn"
            battle_message="enemy took"+enemy_status+"damage"
        elif target == "player" and player_status is None:
            player_status = "burn"
            battle_message="enemy took"+enemy_status+"damage"

    if move["type"] == "poison" and random.randint(1,100) <= 30:
        if target == "enemy" and enemy_status is None:
            enemy_status = "poison"
            battle_message="player took"+player_status+"damage"

        elif target == "player" and player_status is None:
            player_status = "poison"
            battle_message="player took"+player_status+"damage"


    return message

# ===== STATE MACHINE =====
state = "player_input"
battle_message = ""
timer = 0
delay = 1200  # ms

player_choice = None
enemy_choice = None
turn_order = []

game_state = "world"
if pygame.key.get_pressed()[pygame.K_SPACE]:
    game_state = "battle"

clock = pygame.time.Clock()
running=True



while running:
    
    dt = clock.tick(60)
    screen.fill(WHITE)
    if game_state == "world":
        
        screen.fill((50, 200, 50))  # grass background
        pygame.display.flip()
   
        
    
    elif game_state == "battle":
        draw_text("Player", 50, 20)
        draw_text("Enemy", 350, 20)

        draw_hp_bar(50, 50, player.stats["HP"], player.max_hp)
        draw_hp_bar(350, 50, enemy.stats["HP"], enemy.max_hp)

        if player_status:
            draw_text(player_status, 50, 80)
        if enemy_status:
            draw_text(enemy_status, 350, 80)

        draw_moves()
        draw_text(battle_message, 120, 350)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                battle = False

            if state == "player_input" and event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RIGHT and selected_move % 2 == 0:
                    selected_move += 1
                elif event.key == pygame.K_LEFT and selected_move % 2 == 1:
                    selected_move -= 1
                elif event.key == pygame.K_DOWN and selected_move < 2:
                    selected_move += 2
                elif event.key == pygame.K_UP and selected_move >= 2:
                    selected_move -= 2

                elif event.key == pygame.K_RETURN:
                    player_choice = playermoves[selected_move]
                    enemy_choice = random.choice(enemymoves)

                    if decide_first() == "player":
                        turn_order = [("player", player_choice), ("enemy", enemy_choice)]
                    else:
                        turn_order = [("enemy", enemy_choice), ("player", player_choice)]

                    state = "action"
                    timer = pygame.time.get_ticks()

    # ===== STATE LOGIC =====
        if state == "action":
            if pygame.time.get_ticks() - timer > delay:
                if turn_order:
                    user, move = turn_order.pop(0)
                    battle_message = use_move(user, move)
                    timer = pygame.time.get_ticks()
                else:
                    player.apply_status(player_status)
                    enemy.apply_status(enemy_status)
                    player.stats["HP"] = max(0, player.stats["HP"])
                    enemy.stats["HP"] = max(0, enemy.stats["HP"])
                    state = "player_input"

    # WIN CHECK
        if player.stats["HP"] <= 0:
            draw_text("You Lost!", 250, 200)
        elif enemy.stats["HP"] <= 0:
            draw_text("You Won!", 250, 200)

        pygame.display.flip()

pygame.quit()