import subprocess

class SoundLevel:
    def __init__(self, custom_level=100):
        """Initialize with a default custom volume level (0–200 scale)."""
        self.custom_level = custom_level
        self.set_volume(self.custom_level)  # Apply initial volume

    def set_volume(self, new_level):
        """
        Sets new custom volume and updates system volume.
        Custom level range: 0–200, where 0 = mute, 200 = max.
        """
        self.custom_level = new_level

        # Force mute if nearly zero
        if new_level < 5:
            system_volume = 0
        else:
            # Scale 0–200 → 0–100 (but cutoff anything below 5 to zero)
            system_volume = int(max(0, min(100, (new_level / 200) * 100)))

        # Set macOS system volume via AppleScript
        subprocess.run(["osascript", "-e", f"set volume output volume {system_volume}"])
        return system_volume

    def get_volume(self):
        """
        Returns the current system volume (0–100 scale).
        """
        output = subprocess.check_output(["osascript", "-e", "output volume of (get volume settings)"])
        return int(output.strip())