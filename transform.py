import os
import sys

def is_empty_or_whitespace(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read().strip()
    return len(content) == 0

def rename_and_cleanup_files(folder_path):
    # Iterate through the files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            old_txt_path = os.path.join(folder_path, filename)

            # Check if the file is empty or contains only whitespace
            if is_empty_or_whitespace(old_txt_path):
                os.remove(old_txt_path)
                print(f"Deleted empty or whitespace-only file: {old_txt_path}")
                continue  # Skip to the next file

            # Read the first line of the TXT file
            with open(old_txt_path, 'r', encoding='utf-8') as file:
                first_line = file.readline().strip()
                new_name = first_line[:20]  # Get the first 20 characters

            # Define new filenames
            new_txt_filename = f"{new_name}.txt"
            old_mp3_filename = filename.replace('.txt', '.mp3')
            new_mp3_filename = f"{new_name}.mp3"

            # Rename the TXT file
            new_txt_path = os.path.join(folder_path, new_txt_filename)
            os.rename(old_txt_path, new_txt_path)
            print(f"Renamed TXT: {old_txt_path} -> {new_txt_path}")

            # Rename the corresponding MP3 file if it exists
            old_mp3_path = os.path.join(folder_path, old_mp3_filename)
            new_mp3_path = os.path.join(folder_path, new_mp3_filename)

            if os.path.exists(old_mp3_path):
                os.rename(old_mp3_path, new_mp3_path)
                print(f"Renamed MP3: {old_mp3_path} -> {new_mp3_path}")
            else:
                print(f"MP3 file not found: {old_mp3_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <folder_path>")
        sys.exit(1)

    folder_to_transform = sys.argv[1]
    rename_and_cleanup_files(folder_to_transform)
