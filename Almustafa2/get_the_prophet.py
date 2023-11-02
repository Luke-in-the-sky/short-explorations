import requests
from bs4 import BeautifulSoup

FULL_TEXT_FILENAME = 'the_prophet.txt'
SPLIT_ON_PARAGRAPHS_FILENAME = 'the_prophet__split_on_paragraphs.csv'
SEP__NEW_PARAGRAPH = '<new_paragraph>'

def get_raw_text_from_gutenberg(output_file=FULL_TEXT_FILENAME):
    # get the full text
    url = 'https://www.gutenberg.org/files/58585/58585-h/58585-h.htm#link15'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    result = []
    start = False
    for line in soup.find_all('p'):
        pre = ''
        if 'class' in line.attrs and 'p2' in line['class']:
            pre=SEP__NEW_PARAGRAPH
        parsed = pre + line.getText().replace('\r\n', ' ').strip()
        if 'Almustafa, the chosen and the beloved' in parsed:
            start = True
        if start:
            result.append(parsed)

    all_the_text = '\n'.join(result)

    with open(output_file, 'w+') as f:
        f.write(all_the_text)


def split_on_paragraphs(shuffle=False):
    import re
    import pandas as pd

    with open(FULL_TEXT_FILENAME, 'r') as f:
        lines = f.readlines()

    all_text = ''.join(lines)

    chapters = re.findall(r'## ([^\n]+)\n([^#]+)', all_text)
    new_splits = [
        f"""## {title}
        {paragraph}"""
        for title, chapter in chapters
        for paragraph in chapter.split(SEP__NEW_PARAGRAPH)

        if title not in ['The Coming of the Ship', 'The Farewell']
    ]

    df = pd.DataFrame(new_splits, columns=['text'])
    if shuffle:
        df = df.sample(frac=1)
    df.to_csv(SPLIT_ON_PARAGRAPHS_FILENAME)


# get_raw_text_from_gutenberg()
split_on_paragraphs(shuffle=True)
