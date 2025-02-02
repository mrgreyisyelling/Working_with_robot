import os
import time

# Define the target directory and output folder
target_directory = "/home/mike/Documents/Programming/Working_with_robot/WWR - Obsidian"
filtered_folder = os.path.join(target_directory, "filtered")
os.makedirs(filtered_folder, exist_ok=True)  # Ensure the folder exists

# Create a timestamped filename
timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
output_file = os.path.join(filtered_folder, f"omnibus_{timestamp}.md")

# List to store file structure
file_structure = []

# Walk through the directory (excluding 'scripts/' and 'filtered/' folders)
with open(output_file, "w", encoding="utf-8") as outfile:
    for root, dirs, files in os.walk(target_directory):
        if "scripts" in dirs:
            dirs.remove("scripts")  # Exclude 'scripts' directory
        if "filtered" in dirs:
            dirs.remove("filtered")  # Exclude 'filtered' directory

        for file_name in files:
            # Exclude previous omnibus files
            if file_name.startswith("omnibus_") and file_name.endswith(".md"):
                continue
            
            # Include only text and markdown files
            if file_name.endswith((".txt", ".md")):
                file_path = os.path.join(root, file_name)
                file_structure.append(file_path.replace(target_directory, ""))  # Store file structure
                
                # Read and write file content
                with open(file_path, "r", encoding="utf-8") as infile:
                    outfile.write(f"# 🔹 {file_name} 🔹\n")  # Header for each file
                    outfile.write(infile.read() + "\n\n")  # File content

    # Append file structure at the end
    outfile.write("# 📌 FILE STRUCTURE 📌\n")
    for file_path in file_structure:
        outfile.write(f"- {file_path}\n")

print(f"✅ Omnibus file created: {output_file}")

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