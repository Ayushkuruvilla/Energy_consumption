import time
import pyautogui
import subprocess
import os
import psutil

folder_path = "C:\\Users\\91948\\Documents\\Q3\\energibridge-\\"

def open_terminal():
    """Opens a new Command Prompt (cmd.exe) and returns the process object."""
    process = subprocess.Popen("start cmd.exe", shell=True)
    time.sleep(3)  # Wait for the terminal to open
    print(f"Opened new Command Prompt with PID: {process.pid}")
    return process

def generate_command(script_function, count, total_count):
    """Generates the command to run in the new terminal."""
    if script_function == "edge":
        script_path = f"{folder_path}webscript_edge.py"
        command = f'energibridge -o output2\\edge_{count}_{total_count}.csv --summary -- python {script_path}'
    elif script_function == "brave":
        script_path = f"{folder_path}webscript_brave.py"
        command = f'energibridge -o output2\\brave_{count}_{total_count}.csv --summary -- python {script_path}'
    else:
        raise ValueError(f"Unknown script function: {script_function}")

    return command

def energyBridge(command):
    """Starts a new admin Command Prompt, runs the command, and returns the process."""
    try:
        # Using PowerShell to start cmd as administrator
        process = subprocess.Popen(
            f'powershell -Command "Start-Process cmd -ArgumentList \'/c {command}\' -Verb RunAs"',
            shell=True
        )
        print(f"Running command in admin terminal: {command} (PID: {process.pid})")
        return process  # Return process object so `test_vlc.py` can track it
    except Exception as e:
        print(f"Error launching command as admin: {e}")
        return None