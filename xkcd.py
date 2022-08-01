import os
import random
import urllib.parse

import environs
import requests
from pathvalidate import sanitize_filename

from api_vk import VkApi


class Xkcd:
    """
    Интерфейс для скачивания случайных комиксов xkcd.
    """

    def __init__(self):
        self.session = requests.Session()
        self.url = 'https://xkcd.com/'
        self.comic = None

    def get_random_comic(self):
        """
        Получает случайный комикс.
        """
        last_comic = self.session.get(f'{self.url}info.0.json')
        last_comic.raise_for_status()
        last_comic_num = last_comic.json()['num']

        random_comic_url = f'{self.url}{random.randint(1, last_comic_num)}/info.0.json'
        resp = self.session.get(f'{random_comic_url}')
        resp.raise_for_status()
        self.comic = resp.json()

    def get_filename(self, text: str) -> str:
        """
        Сервисная функция для получения названия файла с расширением.
        Очищает строку от запрещенных символов.

        :param text: строка, например ".../comics/images/python.png"
        :return имя файла с расширением, например "python.png"
        """
        clear_url = urllib.parse.unquote(urllib.parse.urlsplit(text).path)
        filename = sanitize_filename(os.path.basename(clear_url))
        self.comic.update({'filename': filename})
        return filename

    def download_comic(self, dir_='files/xkcd'):
        """
        Сохраняет комикс на диск.

        :param dir_: название директории, которая будет создана в корне проекта.
        """
        os.makedirs(dir_, exist_ok=True)
        url = self.comic['img']
        resp = self.session.get(url)
        resp.raise_for_status()

        filename = self.get_filename(url)
        comic_path = f'{dir_}/{filename}'
        self.comic.update({'comic_path': comic_path})

        with open(comic_path, 'wb') as file:
            file.write(resp.content)


def main():
    env = environs.Env()
    env.read_env()
    vk_token = env.str('VK_TOKEN')
    group_id = env.int('VK_GROUP_ID')

    xkcd = Xkcd()
    xkcd.get_random_comic()
    xkcd.download_comic()
    vk = VkApi(vk_token, group_id, xkcd.comic)
    vk.get_server_address()
    vk.upload_image_on_server()
    vk.save_comic_in_album()
    vk.public_comic_on_wall()


if __name__ == '__main__':
    main()
