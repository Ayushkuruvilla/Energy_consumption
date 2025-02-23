import subprocess
import pyautogui as pt
from time import sleep
import os
import argparse

# Path to Minecraft Launcher
game_PATH = "C:/Program Files (x86)/Minecraft Launcher/MinecraftLauncher.exe"
images_PATH = os.path.dirname(os.path.abspath(__file__))+"\\images\\"


# Navigate to the world file (45 seconds total).
def setup_world():
    # Open Launcher (10 seconds).
    subprocess.Popen([game_PATH], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    sleep(10)

    # Click on 'Play' and load the game (30 seconds).
    nav_to_image(images_PATH+'play.png', 5)
    sleep(30)

    # Navigate to the world (1 second).
    nav_to_image(images_PATH+'singleplayer.png', 5)
    sleep(1)

    # Open and load the world (4 seconds).
    nav_to_image(images_PATH+'icon.png', 5)
    sleep(4)


# Run the experiment (~15 seconds total)
def player_script():
    # Reset the condition
    pt.keyDown('t')
    pt.write('/tp @p -189.410822 52 -186.3 -180 0', interval=0.05)
    pt.keyDown('enter')

    pt.keyDown('t')
    pt.write('/time set day', interval=0.05)
    pt.keyDown('enter')

    duration = 10

    while duration != 0:
        move_character('w', 2)
        duration -= 1
        print('Time remaining: ', duration)


# Run the experiment (execution averages ~75 seconds)
def run(shaders=False):
    print("\n==== Running test on minecraft ====")

    # STEP 1: Launch the game and navigate to the world.
    print("Setting up the world.")
    setup_world()

    # STEP 2: Toggle shaders if needed.
    if shaders:
        print("Shaders : ENABLED.")
        pt.keyDown('k')  # Enable shaders
        sleep(5) # Some time to enable shaders to load

        player_script()
        pt.keyDown('k')  # Disable shaders
    else:
        print("Running player script")
        player_script()

    # STEP 3: Close the game and log.
    print("Closing game...")
    pt.hotkey('alt', 'f4')


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

    if action == 'walking':
        print('Walking')

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
