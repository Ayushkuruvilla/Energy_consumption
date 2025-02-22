import subprocess
import pyautogui as pt
from time import sleep

# Path to Minecraft Launcher
game_PATH = "C:/Program Files (x86)/Minecraft Launcher/MinecraftLauncher.exe"


# Navigate to the world file.
def setup_world():
    # Open Launcher (10 seconds).
    subprocess.Popen([game_PATH], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    sleep(10)

    # Click on 'Play' and load the game (30 seconds).
    nav_to_image('images\play.png', 5)
    sleep(30)

    # Navigate to the world (1 second).
    nav_to_image('images\singleplayer.png', 5)
    sleep(1)

    # Open and load the world (4 seconds).
    nav_to_image('images\icon.png', 5)
    sleep(4)


# Run the experiment.
def player_script():
    # Reset the condition
    pt.keyDown('t')
    pt.write('/tp @p -189.410822 52 -186.3 -180 0', interval=0.05)
    pt.keyDown('enter')

    pt.keyDown('t')
    pt.write('/time set day', interval=0.05)
    pt.keyDown('enter')

    #TODO: I would recommend starting energibridge right around here...

    duration = 10

    while duration != 0:
        move_character('w', 2)
        duration -= 1
        print('Time remaining: ', duration)

    #TODO: And ending it here!


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
    pt.keyDown('esc')
    nav_to_image('images\close.png', 5)
    sleep(5)  # Wait for processes to end.


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
    print("Running minecraft simulation")
    run(shaders=True) # Configure whether shaders are enabled here.
