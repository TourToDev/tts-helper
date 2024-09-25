from bs4 import BeautifulSoup

# Load your local HTML file
with open('D:/Workspace/tts/text_processing/phil_of_mind.html', 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'html.parser')

# Find all chapters
chapters = soup.find_all('h1')

for i, chapter in enumerate(chapters):
    chapter_title = chapter.get_text(strip=True)
    chapter_content = []

    # Get all following <p> elements until the next <h3>
    for sibling in chapter.find_next_siblings():
        if sibling.name == 'h1':
            break
        if sibling.name == 'p':
            chapter_content.append(sibling.get_text(strip=True))

    # Write to a TXT file
    with open(f'./phil_of_mind/chapter_{i + 1}.txt', 'w', encoding='utf-8') as f:
        f.write(chapter_title + '\n\n' + '\n'.join(chapter_content))