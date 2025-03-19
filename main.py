import random
import subprocess
import time
import warmup


if __name__ == '__main__':
    print("Running static analysis energy experiment")

    print("Beginning warmup phase...")
    warmup.fibonacci_warmup()
    print("Warmup finished!")

    iterations = 30
    analysis_tools = [
        ('pylint --recursive=y "C:\Users\91948\Documents\Q3\Sustainable\pyEnergiBridge"', "pylint temp"),
        ('pylint --recursive=y "C:\Users\91948\Documents\Q3\Sustainable\requests"', "pylint requests"),
    ] * iterations  # Duplicate each tool 30 times
    random.shuffle(analysis_tools)  # Shuffle the list

    count_sonarscanner = 0
    count_pylint = 0

    for count, (cmd, tool) in enumerate(analysis_tools, 1):

        if tool == "sonarscanner":
            count_sonarscanner += 1
            relative_count = count_sonarscanner
        else:
            count_pylint += 1
            relative_count = count_pylint

        output_file = f"analysis_energy/{tool}_{relative_count}_{count}.csv"
        command = f"energibridge -o {output_file} --summary -g -- {cmd}"
        print(f"Running {tool}_{relative_count}_{count}/{iterations*2}")
        try:
            subprocess.run(command, shell=True, check=True)  # Run the command
        except subprocess.CalledProcessError as e:
            print(f"Error running {command}: {e}")

        print("Resting...")
        time.sleep(20)  # Resting time (20 seconds)
        print("Done!")
