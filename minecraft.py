import subprocess
import pyautogui as pt
from time import sleep
import os
import argparse

# Path to Minecraft Launcher
game_PATH = "C:/Program Files (x86)/Minecraft Launcher/MinecraftLauncher.exe"
images_PATH = os.path.dirname(os.path.abspath(__file__))+"\\images\\"



# Navigate to the world and load it (5 seconds).
def load_world():
    nav_to_image(images_PATH + 'singleplayer.png', 5)
    sleep(1)
    nav_to_image(images_PATH + 'icon.png', 2)
    sleep(4)

# Quit the game and go back to the title screen (10 seconds).
def back_to_title():
    pt.keyDown('esc')
    sleep(1)
    nav_to_image(images_PATH + 'save_and_quit.png', 1)
    sleep(9)


# Run the experiment (~ 40 seconds)
def player_script():

    print("Running player script...")

    # Set time designated for shader loading.
    sleep(5)

    # Reset the condition (teleport to starting position, set time (lighting) to day.
    pt.keyDown('t')
    pt.write('/tp @p -189.410822 52 -172.3 -180 0', interval=0.05)
    pt.keyDown('enter')

    pt.keyDown('t')
    pt.write('/time set day', interval=0.05)
    pt.keyDown('enter')

    # Walk in a straight line for ~30 seconds.
    duration = 15
    while duration != 0:
        move_character('w', 2)
        duration -= 1

# Run the experiment (~60 seconds)
def run(shaders=False):
    print("\n==== Running test on minecraft ====")

    sleep(5)  # Starting buffer

    # STEP 1: Launch the game and navigate to the world.
    print("Loading the world.")
    load_world()

    # STEP 2: Toggle shaders if needed.
    if shaders:
        print("Shaders : ENABLED.")
        pt.keyDown('k')  # Enable shaders
        player_script()
        pt.keyDown('k')  # Disable shaders
    else:
        print("Shaders : DISABLED.")
        player_script()

    # STEP 3: Back to title screen.
    print("Back to title screen.")
    back_to_title()


# Find buttons
def nav_to_image(image, clicks, off_x=0, off_y=0):
    position = pt.locateCenterOnScreen(image, confidence=.7)

    if position is None:
        print(f'{image} was not found.')
        return 0
    else:
        pt.moveTo(position, duration=.1)  # How fast the mouse moves.
        pt.moveRel(off_x, off_y)
        pt.click(clicks=clicks, interval=.3)  # Intervals between clicks.


# Moves the player. Make sure to map the key bindings in game beforehand.
def move_character(key_press, duration, action='walking'):
    pt.keyDown(key_press)
    sleep(duration)
    pt.keyUp(key_press)


if __name__ == "__main__":

    # Arguments
    parser = argparse.ArgumentParser(description="Run Minecraft simulation with optional shaders.")
    parser.add_argument(
        "--shaders",
        action="store_true",
        help="Enable shaders in the simulation"
    )

    args = parser.parse_args()

    # Run the experiment
    print("Running Minecraft simulation")

    shaders = args.shaders
    if shaders:
        print("Running Minecraft simulation with shaders enabled.")
    else:
        print("Running Minecraft simulation without shaders.")

    run(shaders=shaders)
