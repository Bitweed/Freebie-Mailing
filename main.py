import asyncio
import requests
from bs4 import BeautifulSoup
from loguru import logger
import tg_sender
import time

logger.add('debug.log', format='{time} {level} {message}', rotation="8:00", compression='zip')

headers = {'UserAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/103.0.0.0 Safari/537.36'}

resp = requests.get('https://www.playground.ru/news/freebies', headers=headers)
soup = BeautifulSoup(resp.text, 'lxml')

all_news = soup.find('div', {"id": "postListContainer"}).find_all('a')


def get_last_link():  # Get last link
    for i in all_news:
        if i['href'][0: 5] == 'https':
            logger.debug('Last link: ' + i['href'])
            return i['href']


def saving_link(last_new):  # Save latest the new link
    with open('last_new.txt', 'w') as f:
        f.write(last_new)
    logger.info('Last link saved: ' + last_new)


def get_post_info(link):  # Scrapping post and send message to channel
    resp_post = requests.get(link, headers=headers)
    soup_post = BeautifulSoup(resp_post.text, 'lxml')

    header = '<b>' + soup_post.find('h1', class_='post-title').text + '</b> \n\n'
    # content_text = '\n'.join(soup_post.find('div', class_='article-content js-post-item-content').find_all('p'))
    all_content = soup_post.find('div', class_='article-content js-post-item-content')
    content_text_list = all_content.find_all('p')
    content_text = ''.join(i.text for i in content_text_list)
    try:
        image = all_content.find('img')['src']
        try:
            asyncio.run(tg_sender.make_post_img(header, content_text, image))
        except Exception:
            asyncio.run(tg_sender.make_post(header, content_text, image))
        logger.info('Message sent to the channel')
    except TypeError:
        asyncio.run(tg_sender.make_post_without_img(header, content_text))
        logger.error('Message sent to the channel without image!')


def main():  # Checking if link updated
    with open('last_new.txt', 'r') as f:  # Read saved last link
        saved_link = f.read()
    logger.debug('Read "last_new.txt": ' + saved_link)

    last_new = get_last_link()

    if saved_link != last_new:  # Check if link updated
        logger.info('Checked! Links were different')
        saving_link(last_new)
        get_post_info(last_new)
    else:
        logger.info('Checked! Links are the same')

    # time.sleep(3600)  # Loop script
    # main()


if __name__ == '__main__':
    main()