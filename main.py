import os
import random
import subprocess
import time
import warmup

if __name__ == '__main__':
    print("Running static analysis energy experiment")

    print("Beginning warmup phase...")
    warmup.fibonacci_warmup()
    print("Warmup finished!")

    # Ensure output directory exists
    output_dir = "analysis_energy"
    os.makedirs(output_dir, exist_ok=True)  # Creates the directory if it does not exist

    iterations = 30
    analysis_tools = [
        (r'pylint --recursive=y "C:\Users\91948\Documents\Q3\Sustainable\pyEnergiBridge"', "pylint_temp"),
        (r'pylint --recursive=y "C:\Users\91948\Documents\Q3\Sustainable\requests"', "pylint_requests"),
    ] * iterations  # Duplicate each tool 30 times
    random.shuffle(analysis_tools)  # Shuffle the list

    count_pylint_temp = 0
    count_pylint_requests = 0

    for count, (cmd, tool) in enumerate(analysis_tools, 1):

        if tool == "pylint_temp":
            count_pylint_temp += 1
            relative_count = count_pylint_temp
        else:
            count_pylint_requests += 1
            relative_count = count_pylint_requests

        output_file = os.path.join(output_dir, f"{tool}_{relative_count}_{count}.csv")
        command = f'energibridge -o "{output_file}" --summary -g -- {cmd}'
        print(f"Running {tool}_{relative_count}_{count}/{iterations*2}")

        try:
            subprocess.run(command, shell=True, check=True)  # Run the command
        except subprocess.CalledProcessError as e:
            print(f"Error running {command}: {e}")

        print("Resting...")
        time.sleep(20)  # Resting time (20 seconds)
        print("Done!")
