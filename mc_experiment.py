import random
import subprocess
import time


# Cooldown period between iterations
def cooldown():
    print("Waiting before next iteration...")
    time.sleep(10)

if __name__ == '__main__':
    print("Running experiment")
    iterations = 30
    scripts = [
                  ("minecraft.py --shaders", "shaders"),
                  ("minecraft.py", "no_shaders")
              ] * iterations  # Duplicate each script 30 times
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
        command = f"energibridge -o {output_file} --summary -g -- python {script}"
        print(f"Running {label}_{relative_count}_{count}/{iterations*2}")
        try:
            subprocess.run(command, shell=True, check=True)  # Run the command
            time.sleep(60) # Resting time (60 seconds)
        except subprocess.CalledProcessError as e:
            print(f"Error running {command}: {e}")