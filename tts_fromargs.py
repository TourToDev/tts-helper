import edge_tts
import asyncio
import os
import argparse
import re

# Function to extract numbers from file names for natural sorting
def natural_sort_key(text):
    return [int(num) if num.isdigit() else num for num in re.split(r'(\d+)', text)]

# Function to process text-to-speech and generate subtitles
async def text_to_speech_with_subtitle(file_path, generate_subs):
    # Extract the filename without extension for the MP3 and SRT files
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    
    # Open and read the content of the text file
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return

    # Define the language and voice for the speech
    en_uk_voice = "en-GB-RyanNeural"
    voice = en_uk_voice

    # Construct the MP3 and SRT file paths to save in the same folder as the TXT file
    mp3_file = os.path.join(os.path.dirname(file_path), f"{file_name}.mp3")
    srt_file = os.path.join(os.path.dirname(file_path), f"{file_name}.srt")

    # Check if the MP3 file already exists
    mp3_exists = os.path.exists(mp3_file)
    if mp3_exists:
        if not generate_subs:
            print(f"MP3 file already exists and --generate-subs not set: {mp3_file}. Skipping.")
            return  # Skip this file
        else:
            print(f"MP3 file exists: {mp3_file}. Generating subtitles as per --generate-subs flag.")

    # Initialize the TTS communicator and subtitle maker
    communicate = edge_tts.Communicate(text, voice)
    submaker = edge_tts.SubMaker()

    # If MP3 does not exist, generate it along with subtitles
    if not mp3_exists:
        try:
            with open(mp3_file, "wb") as mp3:
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        mp3.write(chunk["data"])  # Write audio data
                    elif chunk["type"] == "WordBoundary":
                        submaker.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])  # Capture word boundaries for subtitles
            print(f"Saved speech as: {mp3_file}")
        except Exception as e:
            print(f"Error generating MP3 for {file_path}: {e}")
            return
    else:
        # If MP3 exists and subtitles need to be generated
        try:
            async for chunk in communicate.stream():
                if chunk["type"] == "WordBoundary":
                    submaker.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])  # Capture word boundaries for subtitles
        except Exception as e:
            print(f"Error processing subtitles for {file_path}: {e}")
            return

    # Check if subtitles already exist
    subs_exists = os.path.exists(srt_file)
    if subs_exists and not generate_subs:
        print(f"Subtitle file already exists and --generate-subs not set: {srt_file}. Skipping subtitle generation.")
        return  # Skip subtitle generation

    # Write the subtitle file (WebVTT format)
    try:
        with open(srt_file, "w", encoding="utf-8") as srt:
            srt.write(submaker.generate_subs())
        print(f"Saved subtitles as: {srt_file}")
    except Exception as e:
        print(f"Error writing subtitles for {file_path}: {e}")

async def process_folder(folder_path, generate_subs):
    # Get the list of files
    try:
        file_list = os.listdir(folder_path)
    except Exception as e:
        print(f"Error accessing folder {folder_path}: {e}")
        return

    # Sort the file list using the natural sort key
    file_list.sort(key=natural_sort_key)

    # Process each text file in the folder
    for file_name in file_list:
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)
            await text_to_speech_with_subtitle(file_path, generate_subs)

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Convert TXT files to MP3 with subtitles using edge-tts.")
    parser.add_argument("folder", type=str, help="Path to the folder containing TXT files")
    parser.add_argument(
        "--generate-subs",
        action="store_true",
        help="Generate subtitles even if MP3 files already exist"
    )
    args = parser.parse_args()

    # Run the async function to process all text files in the specified folder
    asyncio.run(process_folder(args.folder, args.generate_subs))

if __name__ == "__main__":
    main()
