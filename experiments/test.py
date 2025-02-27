import subprocess
import time
import webbrowser

# Define the browsers and their respective commands
BROWSERS = {
    "chrome": "C:/Program Files/Google/Chrome/Application/chrome.exe",
    "brave": "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe",
    "edge": "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
}

# Define the website to test
TEST_URL = "https://www.example.com"

# Define the energy measurement command
ENERGI_COMMAND = 'energibridge.exe -o results.csv --summary timeout 20'

# Number of test iterations
ITERATIONS = 30

for i in range(ITERATIONS):
    print(f"Iteration {i + 1} of {ITERATIONS}")

    for browser, path in BROWSERS.items():
        print(f"Opening {browser}...")

        # Open the browser with the test URL
        subprocess.Popen([path, TEST_URL], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Wait a bit for the browser to load
        time.sleep(5)

        # Run the energy measurement command with admin privileges
        print(f"Measuring energy consumption for {browser}...")
        subprocess.run(f'powershell -Command "Start-Process cmd -ArgumentList \'/c {ENERGI_COMMAND}\' -Verb RunAs"', shell=True)

        # Wait 10 seconds before the next browser test
        time.sleep(10)

print("Test completed.")