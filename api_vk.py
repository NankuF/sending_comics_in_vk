import os

import requests


class VkApi:
    """
    Загружает случайный комикс xkcd в группу Вк.
    Для работы необходимо получить:
    1. token авторизации для приложения в Вк.
    Вставьте этот url в адресную строку, в ответном url будет указан token.
    https://oauth.vk.com/authorize?client_id=YOUR_APP_ID&display=page&scope=photos,groups,wall,offline&response_type=token&v=5.131&state=123456
    2. id вашей группы. https://regvk.com/id/

    У приложения должны быть права: scope=photos,groups,wall,offline
    """

    def __init__(self, token, group_id, comic):
        self.session = requests.Session()
        self.api_vk_method = 'https://api.vk.com/method/'
        self.token = token
        self.group_id = group_id
        self.payload = {}
        self.comic = comic
        self.comic_path = comic['comic_path']
        self.message = comic['alt']
        self.server_url = None
        self.photo_info = None

    def get_server_address(self):
        """
        Получает адрес сервера, на который необходимо загрузить комикс.
        """
        url = f'{self.api_vk_method}photos.getWallUploadServer'
        self.payload.update({'access_token': self.token, 'v': '5.131', 'group_id': self.group_id})
        resp = self.session.get(url, params=self.payload)
        resp.raise_for_status()
        self.server_url = resp.json()['response']['upload_url']

    def upload_image_on_server(self):
        """
        Загружает комикс на сервер.
        """
        with open(self.comic_path, 'rb') as file:
            files = {'photo': file}
            response = self.session.post(self.server_url, files=files)
            response.raise_for_status()
        server, photo, hash_ = response.json().values()
        self.payload.update({'server': server, 'photo': photo, 'hash': hash_})

    def save_comic_in_album(self):
        """
        Сохраняет комикс в альбоме.
        """
        url = f'{self.api_vk_method}photos.saveWallPhoto'
        resp = self.session.post(url, params=self.payload)
        resp.raise_for_status()
        self.photo_info = resp.json()['response'][0]

    def public_comic_on_wall(self):
        """
        Публикует комикс на стене.
        """
        owner_id = self.photo_info['owner_id']
        media_id = self.photo_info['id']
        self.payload.update(
            {'from_group': 1,
             'attachments': f'photo{owner_id}_{media_id}',
             'message': self.message,
             'owner_id': f'-{self.group_id}',
             }
        )
        url = f'{self.api_vk_method}wall.post'
        resp = self.session.post(url, params=self.payload)
        resp.raise_for_status()
        if resp.json()['response'].get('post_id'):
            os.remove(self.comic_path)
        else:
            print('Комикс не опубликован!')
