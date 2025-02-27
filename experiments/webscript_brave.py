import subprocess
import time
import pyautogui
import keyboard

# Path to Brave Browser (Update if needed)
BRAVE_PATH = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"

# ChatGPT URL
CHATGPT_URL = "https://chat.openai.com/"

# Prompt to be typed in ChatGPT
PROMPT = "What is the capital of France?"

# Estimated duration per run (seconds) to match energy measurement duration
RUN_DURATION = 25  # Adjust as needed (covers opening, typing, waiting, closing)

def run():
    print("\n==== Running test on Brave ====")

    # Open ChatGPT in Brave
    subprocess.Popen([BRAVE_PATH, CHATGPT_URL], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Wait for ChatGPT to load
    time.sleep(5)

    # Click on the ChatGPT input field (adjust cursor position if needed)
    pyautogui.click(500, 500)

    # Type the prompt and press Enter
    pyautogui.write(PROMPT, interval=0.05)
    keyboard.press_and_release("enter")

    # Wait for response (simulate reading time)
    time.sleep(10)

    # Close Brave
    print("Closing Brave...")
    subprocess.run("taskkill /F /IM brave.exe", shell=True)

    # Wait for the energy measurement to complete
    print(f"Waiting for energy measurement to complete ({RUN_DURATION}s total)...")
    time.sleep(RUN_DURATION)  # Ensure that the total run time matches the energy measurement

    print("\nBrave test completed.\n")

def brave():
    run()
    
if __name__ == "__main__":
    run()
