# --- GAME DATA ---
player = {
    "name": "",
    "hp": 10,
    "inventory": ["rusty key"]
}

def show_status():
    print(f"\n--- STATUS ---")
    print(f"HP: {player['hp']}")
    print(f"Inventory: {player['inventory']}")
    print("--------------")


def battle(enemy_hp):
    print("\nA battle starts!")

    while enemy_hp > 0 and player["hp"] > 0:
        print("\nChoose an action:")
        print("attack | defend | run")

        fightaction = input("choose one: ").lower().strip()

        if fightaction == "attack":
            print("You hit the enemy!")
            enemy_hp -= 3

        elif fightaction == "defend":
            print("You block some damage!")
            player["hp"] -= 1

        elif fightaction == "run":
            print("You ran away!")
            return False

        else:
            print("Invalid action.")
            continue

        if enemy_hp > 0:
            print("The enemy attacks!")
            player["hp"] -= 2

        show_status()

    if player["hp"] <= 0:
        print("You died...")
        return False
    else:
        print("You defeated the enemy!")
        return True


def dungeon_room():
    print("\nYou enter a damp room. There is a 'chest' and a 'door'.")

    while True:
        action = input("What do you do? ").lower().strip()

        if action == "chest":
            if "sword" not in player["inventory"]:
                print("You found a shiny sword!")
                player["inventory"].append("sword")
            else:
                print("The chest is empty.")
            show_status()

        elif action == "door":
            print("A goblin jumps out!")

            if "sword" in player["inventory"]:
                win = battle(6)  # fight goblin
                if win:
                    win_game()
                    break
                else:
                    break
            else:
                print("You have no weapon!")
                player["hp"] -= 5
                show_status()

                if player["hp"] <= 0:
                    print("You died...")
                    break

        else:
            print("I don't understand that command.")


def win_game():
    print("\nCONGRATULATIONS! You escaped the dungeon.")


# --- START GAME ---
player["name"] = input("What is your name, hero? ")
print(f"Welcome, {player['name']}.")

dungeon_room()