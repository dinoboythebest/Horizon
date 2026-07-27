def start_game():
    print("--- WELCOME TO THE SHADOW FOREST ---")
    print("You are standing at a fork in the road.")
    choice = input("Do you want to go 'left' toward the mountains or 'right' toward the cave? ").lower()

    if choice == "left":
        mountain_path()
    elif choice == "right":
        cave_path()
    else:
        print("That wasn't an option! Try again.")
        start_game()

def mountain_path():
    print("\nThe air gets cold. You see a giant eagle.")
    choice = input("Do you 'climb' onto the eagle or 'hide' in the bushes? ").lower()
    
    if choice == "climb":
        print("The eagle flies you to safety. YOU WIN!")
    else:
        print("The eagle spots you and takes your lunch. YOU LOSE.")

def cave_path():
    print("\nIt's dark. You hear a growl.")
    choice = input("Do you 'run' or 'light' a match? ").lower()
    
    if choice == "light":
        print("The light scares away a small bat. You find gold! YOU WIN!")
    else:
        print("You tripped in the dark. YOU LOSE.")

start_game()