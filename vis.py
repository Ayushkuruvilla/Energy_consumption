import itertools
from math import isnan
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import os
import glob
import pandas
import json
from statistics import mean, median


def outliers(x, threshold=3):
    """Return the outliers for normal distributions

    Uses a z-score threshold of 3
    """
    x = np.array(x)
    z_scores = np.abs(stats.zscore(x))
    outliers = x[z_scores > threshold]
    return outliers


def remove_outliers(x, outliers):
    """Remove the outliers from x"""
    return np.setdiff1d(x, outliers)


def remove_outliers_based_on(x_1, x_2, x_3, threshold=3):
    """Remove all datapoints from x_1, x_2 and x_3 with indices corresponding to the outliers of x_1.

    Outliers are determined using a z-score with a threshold of 3.

    Keyword arguments:
    x_1 -- the dataset to determine the outliers from
    x_2 -- dataset with the same dimension as x_1
    x_3 -- dataset with the same dimension as x_1
    """

    x_1 = np.array(x_1)
    x_2 = np.array(x_2)
    x_3 = np.array(x_3)
    z_scores = np.abs(stats.zscore(x_1))
    y_1 = x_1[z_scores <= threshold]
    y_2 = x_2[z_scores <= threshold]
    y_3 = x_3[z_scores <= threshold]

    return y_1, y_2, y_3


class SimulationResult:
    def __init__(self, label, path_glob):
        self.label = label
        self.path_glob = path_glob
        self.time = []
        self.temp = []
        self.energy = []
        self.energy_norm = []
        self.gpu_usage = []
        self.gpu_temp = []
        self.power = []
        self.n = 0
        self.stats = {}
    
    def get_data(self):
        min_energy = float('inf')
        max_energy = float('-inf')

        print(f"\nProcessing files for {self.label}: {glob.glob(self.path_glob)}")

        """Get the execution time, CPU energy, and CPU temperature."""
        for energibridge_data_file in glob.glob(self.path_glob):
            try:
                df = pandas.read_csv(energibridge_data_file, sep=",")

                # Check if 'Time' column exists and has valid values
                if "Time" not in df.columns or df["Time"].isnull().all():
                    #print(f"Warning: 'Time' column missing or all values are NaN in {energibridge_data_file}")
                    continue
                # Compute execution time
                this_time = int(df["Time"].iloc[-1] - df["Time"].iloc[0])
                this_time_s = this_time / 1000

                self.time.append(this_time_s)

                # Check if 'PACKAGE_ENERGY (J)' column exists
                if "CPU_ENERGY (J)" not in df.columns or df["CPU_ENERGY (J)"].isnull().all():
                    print(f"Warning: 'CPU_ENERGY (J)' column missing or all values are NaN in {energibridge_data_file}")
                    continue

                # Compute energy consumption
                this_energy = float(df["CPU_ENERGY (J)"].iloc[-1] - df["CPU_ENERGY (J)"].iloc[0]) % 65536

                min_energy = min(min_energy, this_energy)
                max_energy = max(max_energy, this_energy)
                self.energy.append(this_energy)
                self.power.append(this_energy / this_time_s)
                self.n += 1

            except Exception as e:
                print(f"Error processing {energibridge_data_file}: {e}")

        # Normalize energy values
        if min_energy < max_energy:  # Prevent division by zero
            self.energy_norm = [(e - min_energy) / (max_energy - min_energy) for e in self.energy]
        else:
            print("Warning: min_energy and max_energy are the same, skipping normalization")
            
    def key_val(self):
        return {
            "time": self.time,
            "temp": self.temp,
            "energy": self.energy,
            "power": self.power,
            "gpu_temp": self.gpu_temp,
        }
    
    def get_stats(self):
        for key, val in self.key_val().items():
            if len(val) == 0:
                continue
            self.stats[key] = {}
            _, pvalue = stats.shapiro(val)
            self.stats[key]["shapiro-pvalue"] = pvalue
            self.stats[key]["mean"] = mean(val)
            self.stats[key]["median"] = median(val)
            self.stats[key]["std"] = float(np.std(val))
            self.stats[key]["min"] = min(val)
            self.stats[key]["max"] = max(val)
            self.stats[key]["25p"] = np.percentile(val, 25)
            self.stats[key]["75p"] = np.percentile(val, 75)
        
            #self.stats[key]["ttest-pvalue"] = pvalue
        return json.dumps(self.stats, indent=2)
    def compare(self, other):
        print("--")
        for key, val in self.key_val().items():
            if len(val) == 0:
                continue
            #print(f"- {key}:")
            # bit verbose, but compare all equal keys
            for key2, val2 in other.key_val().items():
                if key != key2 or len(val2) == 0:
                    continue
                _, pvalue = stats.ttest_ind(
                    val, val2, equal_var=False, alternative="two-sided"
                )
                if isnan(pvalue):
                    continue
                print(f"Comparing {key}")
                print(f"t-test p-value: {pvalue}")
                for skey in ["mean", "median"]:
                    v1 = self.stats[key][skey]
                    v2 = other.stats[key][skey]
                    difference = v1 - v2
                    rel1 = 100 * (v1 - v2) / v2 
                    rel2 = 100 * (v2 - v1) / v1
                    print(f"{skey} of {self.label}: {v1:.2f}, {other.label}: {v2:.2f}")
                    print(f"Absolute difference in {skey} ({v1:.2f} - {v2:.2f}): {abs(difference)}")
                    print(f"Relative increase in {skey} ({v1:.2f} -> {v2:.2f}): {rel2:.2f}%")
                    print(f"Relative increase in {skey} ({v2:.2f} -> {v1:.2f}): {rel1:.2f}%")
                    
        print("--")
    
    def log_stats(self):
        #print(f"Stats for {self.label}, with {len(self.energy)} samples:")
        #print(json.dumps(self.stats, indent=2))
        
        for key, val in self.key_val().items():
            print(f"Outliers for {key}: {len(outliers(val))}")

# Function to plot both boxplot and violin plot
def plot_violin_and_boxplot(data, title, ylabel, filename, ticks, labels, save_dir):
    if len(data) > 0:  # Only plot if data exists
        plt.figure()
        plt.boxplot(data)
        plt.violinplot(data)
        plt.title(title)
        plt.ylabel(ylabel)
        plt.xticks(ticks=ticks, labels=labels)
        plt.grid(linestyle="--", linewidth=0.5)
        plt.show(block=False)
        plt.savefig(os.path.join(save_dir, filename), dpi=300)


def visualize(directory):
    tool, target = directory.split('_')[0], directory.split('_')[1]
    if tool == 'bandit':
        simulations = [
            SimulationResult("Runs with minimum configs (1)", f"analysis/{directory}/bandit-basic_*.csv"),
            SimulationResult("Runs with full configs (73)", f"analysis/{directory}/bandit_*.csv"),
        ]
    elif tool == 'semgrep':
        simulations = [
            SimulationResult("Runs with minimum rules (1)", f"analysis/{directory}/semgrep-1_*.csv"),
            SimulationResult("Runs with bandit ruleset (90)", f"analysis/{directory}/semgrep-90_*.csv"),
        ]
    else:
        raise ValueError('Unknown directory detected!')

    print(tool, target)

    for sim in simulations:
        sim.get_data()
        print(sim.label)
        print(sim.time)
        print(sim.get_stats())
    for sim in simulations:
        sim.log_stats()

    for comb in itertools.combinations(simulations, 2):
        s1, s2 = comb
        print(f"Comparing {s1.label} and {s2.label}")
        print(s1.compare(s2))

        ################################################################################
        # Plots
        ################################################################################

        # Labels that should be consistent accross figures
        y_label_energy = "Energy [J]"

        energy_values = [sim.energy for sim in simulations if len(sim.energy) > 0]
        norm_energy_values = [sim.energy_norm for sim in simulations if len(sim.energy_norm) > 0]
        power_values = [sim.power for sim in simulations if len(sim.power) > 0]
        time_values = [sim.time for sim in simulations if len(sim.time) > 0]
        # temp_values = [sim.temp for sim in simulations if len(sim.temp) > 0]  # Only include if temp data exists

        ticks = [i + 1 for i in range(len(simulations))]
        labels = [f'{sim.label}\n(n={sim.n})' for sim in simulations]

        save_dir = os.path.join('analysis', directory)

        # CPU Energy (Normalized)
        plot_violin_and_boxplot(norm_energy_values, "CPU Energy (Normalized)", "Normalized Energy",
                                f"energy_norm_plot_{directory}.png", ticks, labels, save_dir)

        # CPU Average Power
        plot_violin_and_boxplot(power_values, "CPU Average Power [W]", "Average Power [W]", f"power_plot_{directory}.png", ticks, labels, save_dir)

        # CPU Energy
        plot_violin_and_boxplot(energy_values, "CPU Energy [J]", y_label_energy, f"energy_plot_{directory}.png", ticks, labels, save_dir)

        # Execution Time
        plot_violin_and_boxplot(time_values, "Execution Time [s]", "Time [s]", f"execution_time_plot_{directory}.png", ticks, labels, save_dir)

        # Ensuring the plots remain open
        plt.show()

if __name__ == '__main__':
    directories = os.listdir('analysis')
    for directory in directories:
        visualize(directory)