import requests
from bs4 import BeautifulSoup

import os
import shutil

templates_folder = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    'templates'
)

if os.path.exists(templates_folder):
    shutil.rmtree(templates_folder)

os.mkdir(templates_folder)

current_page = 1

valid_chars = frozenset('-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')


def gather_memes(page_number):
    meme_page = BeautifulSoup(
        requests.get('https://knowyourmeme.com/photos/templates/page/{0}'.format(page_number), headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        }).text,
        'html.parser'
    )

    meme_templates = meme_page.find_all(class_='item')

    if not meme_templates:
        return False

    for meme_template in meme_templates:
        meme_name = meme_template.find('strong')

        if not meme_name or meme_name.text == 'El Shaddai':
            continue

        with open(
                '{0}/{1}.jpg'.format(
                    templates_folder,
                    ''.join(
                        c for c in meme_name
                        .text
                        .replace('\n', ' ') if c in valid_chars
                    )
                ), 'wb') as template_file:

            while True:
                try:
                    template_file.write(
                        requests.get(meme_template.find('img')['data-src']).content
                    )
                    break

                except requests.exceptions.ConnectionError:
                    pass

    print('Finished page #{0}'.format(page_number))

    return True


memes_gathered = gather_memes(current_page)

while memes_gathered:
    current_page += 1
    memes_gathered = gather_memes(current_page)
