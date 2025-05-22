import time
import datetime
import ctypes
import sys
import os

def is_admin():
    """Check if the script is running with administrator privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def convert_to_float_time(time_str):
    """Convert HH:MM string to float (e.g. '14:30' -> 14.5)."""
    try:
        parts = time_str.strip().split(":")
        if len(parts) != 2:
            raise ValueError
        hour = int(parts[0])
        minute = int(parts[1])
        return hour + minute / 60.0
    except:
        return None

def focus_mode():
    host_path = r"C:\Windows\System32\drivers\etc\hosts"
    redirect = "127.0.0.1"
    website_list = [
        "www.facebook.com", "facebook.com",
        "www.instagram.com", "instagram.com",
        "www.youtube.com", "youtube.com"
    ]

    current_time = datetime.datetime.now().strftime("%H:%M")
    print(f"Current time: {current_time}")
    Stop_Time = input("Enter focus end time in 24hr format (e.g., 14:30): ")

    start = convert_to_float_time(current_time)
    end = convert_to_float_time(Stop_Time)

    if start is None or end is None:
        print("Invalid time format. Please enter time as HH:MM.")
        return

    if end <= start:
        print("End time must be after the current time.")
        return

    focus_duration = round(end - start, 2)
    print(f"\nFocus Mode Activated from {current_time} to {Stop_Time} ({focus_duration} hours)\n")

    # === Block Websites ===
    try:
        with open(host_path, "r+") as file:
            content = file.read()
            for site in website_list:
                entry = f"{redirect} {site}"
                if entry not in content:
                    file.write(entry + "\n")
        print("Websites blocked successfully.")
    except Exception as e:
        print("Failed to write to hosts file. Error:", e)
        return

    # === Monitor time until focus period ends ===
    while True:
        now = datetime.datetime.now().strftime("%H:%M")
        if now >= Stop_Time:
            print("\nFocus time is over. Restoring access to websites...")

            try:
                with open(host_path, "r+") as file:
                    lines = file.readlines()
                    file.seek(0)
                    for line in lines:
                        if not any(site in line for site in website_list):
                            file.write(line)
                    file.truncate()
                print("Websites unblocked.")
            except Exception as e:
                print("Error while unblocking websites:", e)

            # === Log focus session ===
            try:
                with open("focus.txt", "a") as log:
                    log.write(f"Focus session: {focus_duration} hours from {current_time} to {Stop_Time}\n")
            except Exception as e:
                print("Could not write log:", e)

            print("Focus Mode turned OFF.")
            break

        time.sleep(10)

# === MAIN ===
if __name__ == "__main__":
    if is_admin():
        focus_mode()
    else:
        print("Requesting administrator access...")
        # Re-run the script as admin
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
