import edge_tts
import asyncio
import os
import argparse
import re

# Function to extract numbers from file names
def natural_sort_key(text):
    return [int(num) if num.isdigit() else num for num in re.split(r'(\d+)', text)]


async def text_to_speech(file_path):
    # Extract the filename without extension for the MP3 file
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    
    # Open and read the content of the text file
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    # Define the language and voice for the speech
    en_uk_voice = "en-GB-RyanNeural"
    us_ava_voice = "en-US-AvaNeural"
    us_male_voice = "en-US-RogerNeural"
    voice = en_uk_voice

    # Construct the MP3 file path to save in the same folder as the TXT file
    mp3_file = os.path.join(os.path.dirname(file_path), f"{file_name}.mp3")
    
        # Check if the MP3 file already exists
    if os.path.exists(mp3_file):
        print(f"MP3 file already exists: {mp3_file}")
        return  # Skip this file

    # Convert the text to speech and save it as an MP3 file
    communicate = edge_tts.Communicate(text, voice, rate="+5%")
    await communicate.save(mp3_file)

    print(f"Saved speech as: {mp3_file}")

async def process_folder(folder_path):
    # Get the list of files
    file_list = os.listdir(folder_path)

    # Sort the file list using the natural sort key
    file_list.sort(key=natural_sort_key)

    for file_name in file_list:
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)
            await text_to_speech(file_path)

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Convert TXT files to MP3 using edge-tts.")
    parser.add_argument("folder", type=str, help="Path to the folder containing TXT files")
    args = parser.parse_args()

    # Run the async function to process all text files in the specified folder
    asyncio.run(process_folder(args.folder))

if __name__ == "__main__":
    main()
