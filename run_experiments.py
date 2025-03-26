import os
import random
import subprocess
import time
from pathlib import Path

import warmup

def run(target, experiment, output_dir):
    print(f"Running static analysis experiment on {target}...")

    print("Beginning warmup phase of 60 seconds...")
    warmup.fibonacci_warmup()
    print("Warmup finished!")

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)  # Creates the directory if it does not exist

    iterations = 30

    analysis_tools = []
    if experiment == 'bandit':
        analysis_tools = [
                             (fr'bandit -c .bandit --severity-level all --confidence-level all -r {target}', "bandit"),
                             (fr'bandit -c .bandit_basic --severity-level high --confidence-level high -r {target}',
                              "bandit-basic"),
                         ] * iterations  # Duplicate each tool 30 times
    elif experiment == 'semgrep':
        analysis_tools = [
                             (fr'semgrep scan requests --config=p/bandit', 'semgrep-90'),
                             (fr'semgrep scan requests --config={target}/.semgrep.yml', "semgrep-1"),

                         ] * iterations  # Duplicate each tool 30 times
    random.shuffle(analysis_tools)  # Shuffle the list

    count_advanced = 0
    count_basic = 0

    for count, (cmd, tool) in enumerate(analysis_tools, 1):

        if tool == "bandit" or tool == "semgrep-90":
            count_advanced += 1
            relative_count = count_advanced
        else:
            count_basic += 1 or tool == "semgrep-1"
            relative_count = count_basic

        output_file = os.path.join(output_dir, f"{tool}_{relative_count}_{count}.csv")
        command = f'energibridge.exe -o "{output_file}" --summary {cmd}'
        print(f"Running {tool}_{relative_count}_{count}/{iterations * 2}")

        try:
            subprocess.run(command, shell=True, check=True)  # Run the command
        except subprocess.CalledProcessError as e:
            print(f"Error running {command}: {e}")

        print("Resting...")
        time.sleep(20)  # Resting time (20 seconds)
        print("Done!")

    print(f"Experiment complete!")

    print("Beginning cooldown of 40 seconds...")
    time.sleep(40)
    print(f"Cooldown over! Results saved to {output_file}")


if __name__ == '__main__':
    experiments = ['bandit', 'semgrep']
    targets = ['requests', 'DeepSeek-V3', 'vllm']

    for target in targets:
        for experiment in experiments:
            target_repo = Path('target_repos') / target
            output_dir = Path('analysis') / f'{experiment}_{target}'
            run(target_repo, experiment, output_dir)


