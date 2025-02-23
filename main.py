import time
import random
import subprocess
import os
import psutil
import ebridge
import webscript_edge
import webscript_brave

def cleanup():
    """Function to clean up after each iteration if needed."""
    print("Cleaning up...")
    time.sleep(5)  # Simulate cleanup time

def close_terminal(process):
    """Closes the specific terminal window used for energy measurement."""
    if process is None:
        print("Warning: Terminal process is None, skipping closure.")
        return
    
    try:
        parent = psutil.Process(process.pid)
        for child in parent.children(recursive=True):  
            child.terminate()
        parent.terminate()
        print(f"Closed subprocess terminal with PID: {process.pid}")
    except psutil.NoSuchProcess:
        print(f"Process {process.pid} already closed or does not exist.")

def experiment():
    N = 1  # Number of iterations per function/test

    scripts = [webscript_edge.edge, webscript_brave.brave]

    # Duplicate and shuffle the list to run each script 30 times
    script_order = scripts * N
    random.shuffle(script_order)
    total_iterations = len(script_order)

    # Dictionary to keep track of the count for each script
    script_count = {script.__name__: 0 for script in scripts}

    # Execute each script in random order
    for count, script in enumerate(script_order, start=1):
        # Increment count for the current script
        script_count[script.__name__] += 1

        # Print iteration status
        print(f"Iteration {count}/{total_iterations}, {script_count[script.__name__]}/30 for {script.__name__}")

        # Generate command for energy measurement
        command = ebridge.generate_command(script.__name__, script_count[script.__name__], count)

        # Open a new terminal and run the command
        terminal_process = ebridge.energyBridge(command)

        # Run the script in parallel
        script()

        # Wait before the next iteration
        print("sleeping before next iteration...")
        time.sleep(10)

        cleanup()

        # Close the subprocess terminal and wait before the next iteration
        #close_terminal(terminal_process)
        #time.sleep(20)  # Sleep for 20 sec between iterations

if __name__ == '__main__':
    experiment()