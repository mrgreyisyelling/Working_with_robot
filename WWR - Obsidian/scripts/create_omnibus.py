import os
import time
import shutil
import zipfile
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Create an omnibus file and archive individual files.")
parser.add_argument('--remove-originals', action='store_true', help="Remove original files after creating the archive")
args = parser.parse_args()

# Define the target directory and output folder
target_directory = "/home/mike/Documents/Programming/Working_with_robot/WWR - Obsidian"
filtered_folder = os.path.join(target_directory, "filtered")
archive_folder = os.path.join(target_directory, "archive")
os.makedirs(filtered_folder, exist_ok=True)  # Ensure the filtered folder exists
os.makedirs(archive_folder, exist_ok=True)  # Ensure the archive folder exists

# Create a timestamped filename
timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
output_file = os.path.join(filtered_folder, f"omnibus_{timestamp}.md")

# List to store file structure
file_structure = []

# Define folders to include and exclude
include_folders = [
    "/home/mike/Documents/Programming/Working_with_robot/WWR - Obsidian",
]
exclude_folders = [
    "/home/mike/Documents/Programming/Working_with_robot/WWR - Obsidian/filtered",
    "/home/mike/Documents/Programming/Working_with_robot/WWR - Obsidian/archive",
    "/home/mike/Documents/Programming/Working_with_robot/WWR - Obsidian/recent trash"
]

# Walk through the specified folders (no recursion)
with open(output_file, "w", encoding="utf-8") as outfile:
    for folder in include_folders:
        folder_path = os.path.join(target_directory, folder)
        if not os.path.exists(folder_path):
            continue

        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        files = sorted(files, key=lambda x: os.path.getmtime(os.path.join(folder_path, x)), reverse=True)

        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            
            # Exclude previous omnibus files
            if file_name.startswith("omnibus_") and file_name.endswith(".md"):
                continue
            
            # Include only text and markdown files
            if file_name.endswith((".txt", ".md")):
                file_structure.append(file_path.replace(target_directory, ""))  # Store file structure
                
                # Read and write file content
                with open(file_path, "r", encoding="utf-8") as infile:
                    outfile.write(f"# 🔹 {file_name} 🔹\n")  # Header for each file
                    outfile.write(infile.read() + "\n\n\n\n")  # Increased break between file sections

    # Append file structure at the end
    outfile.write("# 📌 FILE STRUCTURE 📌\n")
    for file_path in file_structure:
        outfile.write(f"- {file_path}\n")

print(f"✅ Omnibus file created: {output_file}")

# Create a folder to store individual files in the archive
archive_individual_folder = os.path.join(archive_folder, f"files_{timestamp}")
os.makedirs(archive_individual_folder, exist_ok=True)

# Copy individual files to the archive folder
for file_path in file_structure:
    full_file_path = os.path.join(target_directory, file_path.strip("/"))
    shutil.copy(full_file_path, archive_individual_folder)

# Create a zip archive including the omnibus file and the individual files
archive_file = os.path.join(archive_folder, f"omnibus_{timestamp}.zip")
shutil.make_archive(archive_file.replace('.zip', ''), 'zip', archive_individual_folder)

# Add the omnibus file to the archive
with zipfile.ZipFile(archive_file, 'a') as zipf:
    zipf.write(output_file, os.path.basename(output_file))

# Delete the individual files folder after archiving
shutil.rmtree(archive_individual_folder)

print(f"✅ Archive file created: {archive_file}")

# Optionally remove the original files
if args.remove_originals:
    for file_path in file_structure:
        full_file_path = os.path.join(target_directory, file_path.strip("/"))
        os.remove(full_file_path)
    print("🗑️ Original files removed.")

# Cleanup: Keep only the 3 most recent omnibus files and limit total size to 50MB
existing_files = sorted(
    [f for f in os.listdir(filtered_folder) if f.startswith("omnibus_") and f.endswith(".md")],
    key=lambda x: os.path.getmtime(os.path.join(filtered_folder, x)),
    reverse=True
)

# Remove older files beyond the latest 3
for old_file in existing_files[3:]:
    os.remove(os.path.join(filtered_folder, old_file))
    existing_files.remove(old_file)  # Update the list after removal

# Check total size of stored omnibus files and remove oldest if exceeding 50MB
total_size = sum(os.path.getsize(os.path.join(filtered_folder, f)) for f in existing_files)
while total_size > 50 * 1024 * 1024 and len(existing_files) > 1:
    oldest_file = existing_files.pop()
    os.remove(os.path.join(filtered_folder, oldest_file))
    total_size = sum(os.path.getsize(os.path.join(filtered_folder, f)) for f in existing_files)

print(f"🧹 Cleanup complete: Kept latest 3 omnibus files, ensuring storage remains under 50MB.")