import os

directory = "./uav"  # Replace with the actual directory path
counter = 1

# Retrieve the list of files and sort them
files = [filename for filename in os.listdir(
    directory) if filename.endswith(".png")]
files.sort()

for filename in files:
    file_parts = filename.split("_")
    if len(file_parts) > 1:
        number_part = file_parts[1].split(".")[0]
        new_filename = f"uav{counter:04}.png"
        counter += 1
        new_filepath = os.path.join(directory, new_filename)
        old_filepath = os.path.join(directory, filename)
        os.rename(old_filepath, new_filepath)
