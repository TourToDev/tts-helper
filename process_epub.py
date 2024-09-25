import os
import argparse
from ebooklib import epub
from ebooklib import ITEM_DOCUMENT
from bs4 import BeautifulSoup

def epub_to_txt_chunks(epub_file, output_folder):
    book = epub.read_epub(epub_file)
    os.makedirs(output_folder, exist_ok=True)
    chapter_count = 1

    for item in book.get_items_of_type(ITEM_DOCUMENT):
        soup = BeautifulSoup(item.get_body_content(), 'html.parser')
        text = soup.get_text()
        output_file = os.path.join(output_folder, f'chapter_{chapter_count}.txt')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)

        print(f'Saved: {output_file}')
        chapter_count += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert EPUB to TXT.')
    parser.add_argument('epub_file', type=str, help='Path to the EPUB file.')
    args = parser.parse_args()

    # Create output folder based on EPUB file name
    epub_name = os.path.splitext(os.path.basename(args.epub_file))[0]
    output_folder = os.path.join('./output_txts', epub_name)

    epub_to_txt_chunks(args.epub_file, output_folder)
