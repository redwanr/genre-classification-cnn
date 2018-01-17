import os
import shutil
import time

from bs4 import BeautifulSoup
import urllib.request

def main():

    processed_games = set()

    cleanup()
    os.mkdir('../hackathon_data')

    with open('products') as f:
        _ = f.readline()
        products = [line.strip('\n') for line in  f.readlines()]

    for product in products:
        time.sleep(1) 
        records = product.split('\t')
        product_id, game_name, game_genre, product_url = records[0], records[1], records[2], records[3]
        if game_name not in processed_games:
            processed_games.add(game_name)
            build_node(product_id, clean_game_name(game_name), game_genre, product_url)
            get_images(product_id, clean_game_name(game_name), game_genre, product_url)


def cleanup():
    try:
        shutil.rmtree('../hackathon_data')
    except Exception as e:
        pass


def build_node(product_id, game_name, game_genre, product_url):
    os.mkdir(os.path.join('../hackathon_data', game_name))
    with open(os.path.join('../hackathon_data', game_name, 'attributes'), 'w') as f:
        f.write('{}\t{}\t{}\t{}'.format(product_id, game_name, game_genre, product_url))


def clean_game_name(game_name):
    return game_name.replace('/', '')


def get_images(product_id, game_name, game_genre, product_url):
    try:
        product_page = urllib.request.urlopen(product_url)
        soup = BeautifulSoup(product_page, 'html.parser')
        thumbnail_tags = soup.find_all('img', class_='thumbnail-item__content')

        urls = []
        for thumbnail_tag in thumbnail_tags:
            urls.append(thumbnail_tag.attrs['src'])

        urls_deduped = set(urls)

        for url in urls:
            try:
                urllib.request.urlretrieve(url, os.path.join('../hackathon_data', game_name, url.split('/')[-1]))
            except Exception as e:
                print ('Failed to get url {} for game {}'.format(url, game_name))
    except Exception as e:
        print ('Failed to get product page {} for game {}'.format(product_url, game_name))
             
if __name__ == '__main__':
    main()
