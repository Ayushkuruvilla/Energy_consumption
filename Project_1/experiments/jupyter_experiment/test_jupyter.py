import subprocess
import time

import psutil

notebooks = {
    "Jupyter-notebook": "C:/Users/chena/PycharmProjects/Energy_consumption/jupyter_experiment/example-data-analysis-notebook.ipynb",
    "Jupyter-lab": "C:/Users/chena/PycharmProjects/Energy_consumption/jupyter_experiment/example-data-analysis-lab.ipynb",
}

directory = f"output_jupyter"

# Number of test iterations
ITERATIONS = 30

# Estimated duration per run (seconds) to match energy measurement duration
RUN_DURATION = 20  # Adjust as needed (covers opening, typing, waiting, closing)


for i in range(ITERATIONS):
    print(f"\n==== Iteration {i + 1} of {ITERATIONS} ====")

    for notebook_name, notebook_path in notebooks.items():
        print(f"\nRunning test on {notebook_name}...")

        # Save energy measurement result in a separate file for each run
        output_file = directory+f"/results_{notebook_name}_run_{i+1}.csv"

        # Start energibridge.exe to measure energy (it will run for the full iteration duration)
        energi_command = f'energibridge.exe -o {output_file} --summary timeout {RUN_DURATION}'
        print(f"Starting energy measurement for {notebook_name} (Timeout: {RUN_DURATION}s)...")
        energy_process = subprocess.Popen(
            f'powershell -Command "Start-Process cmd -ArgumentList \'/c {energi_command}\' -Verb RunAs"',
            shell=True
        )

        # Open notebook in the browser
        if notebook_name == "Jupyter-notebook":
            process = subprocess.Popen(["jupyter", "notebook", notebook_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            process = subprocess.Popen(["jupyter", "lab", notebook_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Wait for notebook to load
        time.sleep(15)

        # Close the browser
        print(f"Closing {notebook_name}...")
        subprocess.run("taskkill /F /IM msedge.exe", shell=True)
        # Terminate Jupyter Notebook process
        process.terminate()

        # Ensure all child processes are terminated
        try:
            parent = psutil.Process(process.pid)
            for child in parent.children(recursive=True):  # Kill all child processes
                child.terminate()
            parent.terminate()
        except psutil.NoSuchProcess:
            print("Process already terminated.")

        # Wait for the energy process to finish
        print(f"Waiting for energy measurement to complete ({RUN_DURATION}s total)...")
        time.sleep(5)  # Ensure that the total run time matches the energy measurement

    print(f"\nIteration {i + 1} completed.\n")

print("Test completed. Energy consumption data saved.")