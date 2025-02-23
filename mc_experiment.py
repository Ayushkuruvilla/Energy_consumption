import random
import subprocess
import time


# Cooldown period between iterations
def cooldown():
    print("Cleaning up...")
    time.sleep(10)

# Command 1: energibridge -o minecraft_test.csv --summary -- python minecraft.py --shaders
# Command 2: energibridge -o minecraft_test.csv --summary -- python minecraft.py
if __name__ == '__main__':
    print("Running experiment")
    # TODO: Run 30 iterations of shader/no shader scripts using energibridge!

    scripts = [
                  ("minecraft.py --shaders", "shaders"),
                  ("minecraft.py", "no_shaders")
              ] * 30  # Duplicate each script 30 times
    random.shuffle(scripts)  # Shuffle the list

    count_shaders = 0
    count_no_shaders = 0

    for count, (script, label) in enumerate(scripts, 1):

        if label == "shaders":
            count_shaders += 1
            relative_count = count_shaders
        else:
            count_no_shaders += 1
            relative_count = count_no_shaders

        output_file = f"minecraft_output/{label}_{relative_count}_{count}.csv"
        command = f"energibridge -o {output_file} --summary -- python {script}"
        print(f"Running {count}/60: {command}")
        try:
            subprocess.run(command, shell=True, check=True)  # Run the command
            cooldown()
        except subprocess.CalledProcessError as e:
            print(f"Error running {command}: {e}")