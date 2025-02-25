| Author | Title | Image | Date | Summary |
|--------|-------|-------|------|---------|
| Andrea,Ayush Kuruvilla,Sahar Marossi,Yulin Chen | **Minecraft Energy Consumption Comparison with and without Shaders** | ![Cover](../img/p1_measuring_software/gX_template/cover.png) | 15/02/2025 | This article presents a roadmap on how to properly set up a scientific methodology to measure energy consumption in Minecraft with and without shaders. We outline unbiased energy measurement strategies, discuss methodology and replication, and analyze results to draw meaningful conclusions about energy efficiency. |



## Problem Statement

Measuring energy consumption in gaming applications is a challenging task, especially when comparing different graphical settings. Minecraft is a widely popular game that allows extensive graphical modifications, including shader packs that enhance visual fidelity but may significantly impact power consumption. 

This article focuses on comparing the energy consumption of Minecraft when running with and without shaders. Our goal is to measure how much additional power is required to render advanced lighting effects and reflections provided by shader packs and to discuss the implications for gamers and developers aiming for energy efficiency.

## Methodology

The experiment follows a structured process to measure energy consumption with minimal bias. The methodology includes:

- **Warmup Phase:** A Fibonacci sequence warmup function (`warmup.fibonacci_warmup()`) is executed before starting the experiment to ensure system stability and prevent initial spikes in energy consumption.
- **Iteration-Based Execution:** The experiment consists of 30 iterations per condition (with shaders and without shaders), shuffled randomly to minimize potential external influences.
- **Automated Execution:** Each test instance is run using a subprocess command with `energibridge`, ensuring consistent logging of GPU and CPU energy consumption.
- **Output Logging:** Each test generates an output CSV file containing detailed energy consumption data.
- **Resting Periods:** A 20-second rest period is included between each iteration to prevent thermal throttling and ensure consistency.`

## Experiment (Per Iteration)

- Open Minecraft Launcher (10 seconds).

- Launch the game (30 seconds).

- Navigate and load the world (10 seconds).

- Run player experiment (~40 seconds).

- Buffer time (5 seconds). Load shaders if enabled.

- Teleport player to start location. Set time to day (for lighting).

- Walk forward for ~30 seconds through the map (designed to benchmark shader-lighting).

- Disable shaders if enabled.

- Close game via Alt-F4.

- Rest for 60 seconds.

- Total experiment time averages ~90 seconds.

## Setup

### Hardware Specifications:
- **Processor:** Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz
- **GPU:** NVIDIA Quadro P2000
- **Installed RAM:** 16.0 GB (15.8 GB usable)
- **Monitor Refresh Rate:** 60Hz
- **Desktop Resolution:** 1920 x 1080
- **Color Format:** RGB
- **Color Space:** Standard Dynamic Range (SDR)

### Software Setup:
- **Minecraft Version:** 1.21.4
- **Modded Instance:** Iris-Fabric-1.8.8+MC1.21.4
- **Shaderpack:** Complementary Shaders 4.7.2
- **World File:** Lighting World (TODO: Share file)

## Replication

To ensure the experiment is replicable:
- The **same hardware and software settings** must be maintained across all runs.
- The **game world must be identical** for all test iterations.
- **All background processes and unnecessary peripherals must be disabled** to minimize external factors affecting energy consumption.
- The **GPU power should be logged at fixed intervals** (e.g., 2 seconds after execution and at peak load).

## Results

We will compare the power consumption values collected from running Minecraft with and without shaders. Data will be presented in tabular and graphical formats to highlight differences in energy usage.

## Discussion

## Limitations

- Energy measurements depend on system conditions and may vary slightly.
- Different shader packs may lead to different power consumption profiles.
- This experiment does not account for extended gameplay and only considers a limited test duration.

## Conclusion

This study provides an empirical analysis of the energy consumption differences in Minecraft with and without shaders. Our findings highlight the potential trade-offs between visual fidelity and power efficiency, offering insights for gamers and developers seeking optimized performance and sustainability.

By following proper scientific measurement techniques, we ensure that our results remain valid and reproducible, ultimately contributing to better energy efficiency practices in gaming and software development.

