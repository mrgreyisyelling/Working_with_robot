import os
import shutil
import time

# Define the source and destination directories
source_directory = "/home/mike/Documents/Programming/Working_with_robot/WWR - Obsidian/filtered"
destination_directory = "/home/mike/Documents/Programming/Working_with_robot/WWR - Obsidian/archive/omnibus_storage"
os.makedirs(destination_directory, exist_ok=True)  # Ensure the destination folder exists

# Create a timestamped archive filename
timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
archive_file = os.path.join(destination_directory, f"omnibus_{timestamp}.zip")

# Create a zip archive of the source folder
shutil.make_archive(archive_file.replace('.zip', ''), 'zip', source_directory)

print(f"✅ Archive file created: {archive_file}")