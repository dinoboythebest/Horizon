import pygame
import random

pygame.init()

# Screen
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Pokemon Battle")

# Fonts
font = pygame.font.SysFont(None, 30)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Player + Enemy
player_hp = 100
enemy_hp = 100

turn = "player"

def draw_text(text, x, y):
    img = font.render(text, True, BLACK)
    screen.blit(img, (x, y))

moves = [
    {"name": "Tackle", "damage": 10, "type": "attack"},
    {"name": "Fireball", "damage": 18, "type": "fire"},
    {"name": "Heal", "heal": 12, "type": "heal"},
    {"name": "Poison Sting", "damage": 6, "type": "poison"}
]
statuses=("poison","burn")
player_status = None
enemy_status = None



running = True
while running:
    screen.fill(WHITE)

    # Draw HP
    draw_text(f"Player HP: {player_hp}", 50, 50)
    draw_text(f"Enemy HP: {enemy_hp}", 350, 50)

    # Draw buttons (simple text)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if turn == "player":
            draw_text("press 1 to tackle", 100, 250)
            draw_text("Press 2 to fireball",300, 250)
            draw_text("Press 3 to heal", 100, 300)
            draw_text("Press 4 to poison sting",300, 300)



            if event.type == pygame.KEYDOWN :
                if event.key==pygame.K_1:
                    move = moves[0]
                    if move["type"] == "attack":
                        damage = move["damage"]
                        enemy_hp -= damage
                        print(f"You used {moves['name']} for {damage} damage")
                elif event.key == pygame.K_2:
                    move = moves[1]
                    if move["type"] == "fire":
                            damage = move["damage"]
                            enemy_hp -= damage
                            burntrue = random.randint(1,5)
                            if burntrue==3:
                                enemy_status = "burn"
                                print("Enemy is burned!")
                elif event.key == pygame.K_3:
                    move = moves[2]
                    if move["type"] == "heal":
                        heal = move["heal"]
                        player_hp += heal
                        print(f"You healed {heal} HP")
                elif event.key == pygame.K_4:
                    move = moves[3]
                    if move["type"] == "poison":
                        damage = move["damage"]
                        enemy_hp -= damage
                        poisontrue = random.randint(1,5)
                    if poisontrue==3 or poisontrue==4:
                        enemy_status = "poison"
                        print("Enemy is poisoned!")
                else:
                    print("thats not a move click again")


            
            
            
            turn="enemy"
            if player_status==statuses[0]:
                player_hp-=3
                poisonchance = random.randint(1,5)   
                if poisonchance==3:
                    player_status=None
                    poisonchance=0
                    print(f"Player was cured of {player_status}")
            elif player_status==statuses[1]:
                player_hp-=6
                burnchance = random.randint(1,5)   
                if burnchance==3 or burnchance==4:
                    player_status=None
                    burnchance=0
                    print(f"Player was cured of {player_status}")

                    
    # Enemy turn
    if turn == "enemy" and enemy_hp > 0:
        pygame.time.delay(500)
        if enemy_status==statuses[0]:
            enemy_hp-=3
            poisonchance = random.randint(1,5)   
            if poisonchance==3:
                enemy_status=None
                poisonchance=0
                print(f"Enemy was cured of {enemy_status}")
        elif enemy_status==statuses[1]:
            enemy_hp-=6
            burnchance = random.randint(1,5)   
            if burnchance==3 or burnchance==4:
                enemy_status=None
                burnchance=0
                print(f"Enemy was cured of {player_status}")
        enemymove=random.randint(1, 4)
        if enemymove==1:
            player_hp-=5
            burnchance=random.randint(1,5)
            if burnchance==3:
                    player_status="burn"
                    print("enemy used fireball,dealt 5 damage and burned")
            else:
                print("enemy used fireball and dealt 5 damage")
        
        elif enemymove==2:
            enemy_hp+=5
            print("enemy healed 5hp")

        elif enemymove==3:
            player_hp-=10
            print("enemy dealt 10 damage")

        elif enemymove==4:
            player_hp-=5
            poisonchance=random.randint(1,5)
            if poisonchance==3:
                player_status="poison"
                print("enemy used poison sting ,dealt 5 damage and poisoned")
             


        
        turn = "player"
        

    # Win/Lose
    if player_hp <= 0:
        draw_text("You Lost!", 250, 200)
        running=False


    elif enemy_hp <= 0:
        draw_text("You Won!", 250, 200)
        running=False


    pygame.display.flip()



pygame.quit()