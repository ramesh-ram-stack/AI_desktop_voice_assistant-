# pip install matplotlib
import matplotlib.pyplot as plt
import os

def focus_graph():
    if not os.path.exists("focus.txt"):
        print("No focus data found.")
        return

    with open("focus.txt", "r") as file:
        lines = file.readlines()

    focus_durations = []
    for line in lines:
        if "Focus session:" in line:
            try:
                duration = float(line.split("Focus session:")[1].split("hours")[0].strip())
                focus_durations.append(duration)
            except:
                continue

    if not focus_durations:
        print("No valid focus session durations found.")
        return

    x_values = list(range(1, len(focus_durations) + 1))
    y_values = focus_durations

    print("Focus durations:", y_values)

    plt.plot(x_values, y_values, color="red", marker="o")
    plt.title("Your Focused Time", fontsize=16)
    plt.xlabel("Session Number", fontsize=14)
    plt.ylabel("Focus Time (Hours)", fontsize=14)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
