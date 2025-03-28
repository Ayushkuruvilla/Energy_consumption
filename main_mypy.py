import os
import subprocess
import time
import itertools
import random

def run_experiment():
    print("Starting static analysis energy experiment with mypy.")

    # Define paths to the repositories
    repos = {
        #"pyEnergiBridge": r"C:\Users\91948\Documents\Q3\Sustainable\pyEnergiBridge",
        "requests": r"C:\Users\91948\Documents\Q3\Sustainable\requests"
    }

    # Define configuration files
    config_files = [
        "mypy_baseline.ini",
        "mypy_moderate.ini",
        "mypy_strict.ini",
        "mypy_ignore_imports.ini"
    ]

    # Ensure output directories exist
    output_dir = "analysis_energy"
    log_dir = "analysis_logs"
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)

    iterations = 30

    # Create a list of all (config_file, repo_name, repo_path, iteration) combinations
    experiment_cases = list(itertools.product(config_files, repos.items(), range(1, iterations + 1)))

    # Shuffle the experiment order
    random.shuffle(experiment_cases)

    # Run the experiments in randomized order
    for config_file, (repo_name, repo_path), iteration in experiment_cases:
        output_file = os.path.join(output_dir, f"{repo_name}_{config_file}_{iteration}.csv")
        command = f'energibridge -o "{output_file}" --summary -g -- mypy --config-file {config_file} "{repo_path}"'
        print(f"Running {repo_name} with {config_file}, iteration {iteration}/{iterations}")

        log_file_path = os.path.join(log_dir, f"{repo_name}_{config_file}_{iteration}.log")
        with open(log_file_path, "w") as log_file:
            result = subprocess.run(command, shell=True, stdout=log_file, stderr=subprocess.STDOUT)
            if result.returncode != 0:
                print(f"Command exited with non-zero status ({result.returncode}) for: {command}")

        print("Resting for 5 seconds...")
        time.sleep(5)

    print("Experiment completed.")

if __name__ == '__main__':
    run_experiment()
