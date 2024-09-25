import edge_tts
import asyncio
import os

async def text_to_speech(file_path):
    # Extract the filename without extension for the MP3 file
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    
    # Open and read the content of the text file
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    # Define the language and voice for the speech
    voice = "en-US-AvaMultilingualNeural"  # Example voice

    # Convert the text to speech and save it as an MP3 file
    mp3_file = os.path.join(os.path.dirname(file_path), f"{file_name}.mp3")
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(mp3_file)

    print(f"Saved speech as: {mp3_file}")

async def process_folder(folder_path):
    # Iterate over all TXT files in the specified folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)
            await text_to_speech(file_path)

# Specify the folder containing the TXT files
folder = "./test"

# Run the async function to process all text files in the folder
asyncio.run(process_folder(folder))
