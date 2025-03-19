# Energy Consumption Experiment

This repository contains scripts and data for measuring and comparing energy consumption betwen using and playing Minecraft with a Shader pack vs without . The experiment is conducted using **EnergyBridge** and produces results stored in dedicated output folders.

---
## **Video showing our Minecraft Experiment Shader vs No Shader difference**
[Watch the Video](https://www.youtube.com/watch?v=WmE67KBySDA)

## **Project Structure**
```

📄 mc_experiment.py        # Main script to execute multiple randomized runs and manage the experiment
📄 minecraft.py            # Script to simulate Minecraft runthrough with/without shaders ( Run 60 times)
📄 ebridge.py              # EnergyBridge integration script for collecting energy consumption data
📄 new_vis.py                  # Script to generate visualizations from the results
📁 minecraft_output/       # Stores experimental results from 60 runs of minecraft
📁 experiments/            # Contains other experiments tested out by the team
```

---

## **Setup Instructions**
### **1. Ensure the RAPL Service is Running (Only If Not Already Done)**
The **RAPL (Running Average Power Limit) service** is required for EnergyBridge to function properly. If you haven’t set it up yet, follow these steps:

#### **Install and Start the RAPL Service**
```sh
sc create rapl type=kernel binPath="C:\Users\91948\Documents\Q3\Sustainable\Energy_consumption\LibreHardwareMonitor.sys"
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
   Execute the `mc_experiment.py` script with **administrator privileges** to avoid access issues:
   ```sh
   python mc_experiment.py
   ```

---

## **Generating Visualizations**
After running the experiment, use `new_vis.py` to generate plots based on the collected energy consumption data:
```sh
python new_vis.py
```
The generated plots will help compare energy consumption between minecraft with and without shaders.

---

## **Notes**
- The experiment is executed **30 times** with and without shaders each to ensure statistically valid comparisons.
- The experiments folder contain other experiments tested out by the team to evaluate significance 

---

## **Contributors**
- **Ayush Kuruvilla**
- **Sahar Marossi**
- **Andrea Onofrei**
- **Yulin Chen**
