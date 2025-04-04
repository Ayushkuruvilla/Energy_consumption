# Energy Consumption Experiment

This repository contains scripts and data for measuring and comparing energy consumption of static analysis tools. The experiment is conducted using EnergiBridge, and results are stored in a dedicated output folder.

---
# **Framework/Tool Devloped**
[Check out sast-energy-monitor on PyPI](https://pypi.org/project/sast-energy-monitor/)

# **Project Structure**
```

📂 Energy_Consumption/      # Root directory
│
├── 📂 analysis_energy/     # Stores experimental results (CSV files)
│   ├── pylint_temp_1_1.csv
│   ├── pylint_requests_1_2.csv
│   └── ... (more results)
│
├── 📂 Project_1/           # Folder containing the first project experiment
│   ├── (project-specific files go here)
│
├── 📄 main.py              # Main script to execute and manage the experiment
├── 📄 warmup.py            # Script for pre-experiment computational warmup
│
├── 📄 README.md            # Documentation and instructions
│
└── 📄 .gitignore           # Specifies files and directories to ignore in Git

```

---
# Energy Consumption Experiment

This repository contains scripts and data for measuring and comparing energy consumption betwen using and playing Minecraft with a Shader pack vs without . The experiment is conducted using **EnergyBridge** and produces results stored in dedicated output folders.

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
