import subprocess
import time
import os


def run_vlc(video_file, hw_accel):
    print(video_file)
    """
    Launch VLC with hardware acceleration enabled or disabled.
    """
    accel_flag = "--avcodec-hw=dxva2" if hw_accel else "--avcodec-hw=none"
    vlc_exe = r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe"  # Adjust if needed
    # --play-and-exit: automatically exits after playback
    command = [vlc_exe, video_file, accel_flag, "--play-and-exit"]
    print(command)

    return subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def measure_energy(test_name, video_file, hw_accel, duration, output_dir):
    """
    Runs energibridge and VLC concurrently, then terminates both after a fixed duration.
    """
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"results_{test_name}.csv")

    # Build energibridge command (ensure energibridge.exe is in your PATH or provide full path)
    energibridge_cmd = f'energibridge.exe -o "{output_file}" --summary timeout {duration}'

    # IMPORTANT: energibridge.exe requires admin privileges.
    energibridge_proc = subprocess.Popen(energibridge_cmd, shell=True)

    # Launch VLC with the desired hardware acceleration setting.
    vlc_proc = run_vlc(video_file, hw_accel)

    # Wait for video to finish playing
    time.sleep(15)

    # Terminate VLC
    print(f"\nClosing VLC...\n")
    vlc_proc.terminate()

    # Terminate energibridge
    energibridge_proc.terminate()

    # Wait for the energy process to finish
    print(f"\nWaiting for energy measurement to complete ({duration}s total)...\n")
    time.sleep(5)  # Ensure that the total run time matches the energy measurement

# Parameters
video_file = r"TESTVIDEO.mp4"  # Your test video file
output_dir = r"output_vlc"  # Where to save the CSV results
duration = 20  # Duration (in seconds) for each test run
num_runs = 30

print("\nRunning tests for VLC with hardware acceleration DISABLED...")
for i in range(1, num_runs + 1):
    test_name = f"vlc_hw_disabled_run_{i}"
    print(f"Test {i}/{num_runs} (HW disabled)...")
    measure_energy(test_name, video_file, hw_accel=False, duration=duration, output_dir=output_dir)
    print(f"\nIteration {i} completed.\n")

print("Running tests for VLC with hardware acceleration ENABLED...")
for i in range(1, num_runs + 1):
    test_name = f"vlc_hw_enabled_run_{i}"
    print(f"Test {i}/{num_runs} (HW enabled)...")
    measure_energy(test_name, video_file, hw_accel=True, duration=duration, output_dir=output_dir)
    print(f"\nIteration {i} completed.\n")

print("\nAll tests completed.\n")
