import subprocess
import time
import pyautogui
import keyboard

# Define browser paths (Update if needed)
BROWSERS = {
    "chrome": "C:/Program Files/Google/Chrome/Application/chrome.exe",
    "brave": "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
}

directory = f"output_3"
# Define ChatGPT URL
CHATGPT_URL = "https://chat.openai.com/"

# Define the prompt to be typed in ChatGPT
PROMPT = "What is the capital of France?"

# Number of test iterations
ITERATIONS = 30

# Estimated duration per run (seconds) to match energy measurement duration
RUN_DURATION = 25  # Adjust as needed (covers opening, typing, waiting, closing)

for i in range(ITERATIONS):
    print(f"\n==== Iteration {i + 1} of {ITERATIONS} ====")

    for browser_name, browser_path in BROWSERS.items():
        print(f"\nRunning test on {browser_name}...")

        # Save energy measurement result in a separate file for each run
        output_file = directory+f"/results_{browser_name}_run_{i+1}.csv"

        # Start energibridge.exe to measure energy (it will run for the full iteration duration)
        energi_command = f'energibridge.exe -o {output_file} --summary timeout {RUN_DURATION}'
        print(f"Starting energy measurement for {browser_name} (Timeout: {RUN_DURATION}s)...")
        energy_process = subprocess.Popen(
            f'powershell -Command "Start-Process cmd -ArgumentList \'/c {energi_command}\' -Verb RunAs"',
            shell=True
        )

        # Open ChatGPT in the browser
        subprocess.Popen([browser_path, CHATGPT_URL], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Wait for ChatGPT to load
        time.sleep(5)

        # Click on the ChatGPT input field (adjust cursor position if needed)
        pyautogui.click(500, 500)  

        # Type the prompt and press Enter
        pyautogui.write(PROMPT, interval=0.05)
        keyboard.press_and_release("enter")

        # Wait for response (simulate reading time)
        time.sleep(10)

        # Close the browser
        print(f"Closing {browser_name}...")
        subprocess.run("taskkill /F /IM chrome.exe", shell=True)
        subprocess.run("taskkill /F /IM brave.exe", shell=True)

        # Wait for the energy process to finish
        print(f"Waiting for energy measurement to complete ({RUN_DURATION}s total)...")
        time.sleep(RUN_DURATION)  # Ensure that the total run time matches the energy measurement

    print(f"\nIteration {i + 1} completed.\n")

print("Test completed. Energy consumption data saved.")