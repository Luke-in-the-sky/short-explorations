import requests
from bs4 import BeautifulSoup


# get the full text
url = 'https://www.gutenberg.org/files/58585/58585-h/58585-h.htm#link15'
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

result = []
start = False
for line in soup.find_all('p'):
    pre = ''
    if 'class' in line.attrs and 'p2' in line['class']:
        pre='<new_paragraph>'
    parsed = pre + line.getText().replace('\r\n', ' ').strip()
    if 'Almustafa, the chosen and the beloved' in parsed:
        start = True
    if start:
        result.append(parsed)

all_the_text = '\n'.join(result)

with open('the_prophet_raw.txt', 'w+') as f:
    f.write(all_the_text)
