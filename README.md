# Energy Consumption Experiment

This repository contains scripts and data for measuring and comparing energy consumption across different web browsers. The experiment is conducted using **EnergyBridge** and produces results stored in dedicated output folders.

---

## **Project Structure**
```
📁 output/         # Stores experimental results from the first set of runs
📁 output-2/       # Stores experimental results from the second set of runs
📄 main.py        # Main script to execute multiple runs and manage the experiment
📄 ebridge.py     # EnergyBridge integration script for collecting energy consumption data
📄 vis.py         # Script to generate visualizations from the results
📄 webscript_brave.py  # Script for running a single Brave browser test (executed 30 times in main.py)
📄 webscript_edge.py   # Script for running a single Edge browser test (executed 30 times in main.py)
📁 test_gpt/      # Initial/older versions of the experiment scripts
📁 test/          # Additional early versions of the code
```

---

## **Setup Instructions**
### **1. Ensure the RAPL Service is Running (Only If Not Already Done)**
The **RAPL (Running Average Power Limit) service** is required for EnergyBridge to function properly. If you haven’t set it up yet, follow these steps:

#### **Install and Start the RAPL Service**
```sh
sc create rapl type=kernel binPath="C:\Users\91948\Documents\Q3\energibridge-\LibreHardwareMonitor.sys"
sc start rapl
```
*(Replace the path with the correct location of `LibreHardwareMonitor.sys`.)*

---

## **Running the Experiment**
1. **Set up EnergyBridge**  
   - Point to your `energibridge.exe` in the `folder_path` variable inside `ebridge.py`.  
   - Modify the `generate_command` function in `ebridge.py` to match your setup.

2. **Verify EnergyBridge is Working**  
   Test it manually by running:
   ```sh
   energibridge.exe -o results.csv --summary timeout 20
   ```
   If the command runs successfully and generates a `results.csv` file, EnergyBridge is functioning correctly.

3. **Run the Experiment**  
   Execute the `main.py` script with **administrator privileges** to avoid access issues:
   ```sh
   python main.py
   ```

---

## **Generating Visualizations**
After running the experiment, use `vis.py` to generate plots based on the collected energy consumption data:
```sh
python vis.py
```
The generated plots will help compare energy consumption between **Brave** and **Edge**.

---

## **Notes**
- The experiment is executed **30 times** per browser to ensure statistically valid comparisons.
- The `test_gpt/` and `test/` directories contain older versions of the experiment scripts.

---

## **Contributors**
- **Ayush Kuruvilla**
