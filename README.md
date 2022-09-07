# Автопостинг комиксов Xkcd в группу Вконтакте

Скрипт позволяет загружать комикс по api VK в группу Вконтакте.

## Подготовка
1. Скачайте проект:<br>

```commandline
git clone https://github.com/NankuF/sending_comics_in_vk.git
```

2. Перейдите в директорию:<br>

```commandline
cd sending_comics_in_vk
```

3. Создайте виртуальное окружение:<br>

```commandline
python -m venv venv
```

4. Активируйте окружение:<br>

```commandline
. ./venv/bin/activate
```
5. Установите зависимости:<br>

```commandline
pip install -r requirements.txt
```
6. Создайте группу в Вконтакте.
7. Узнайте ее id: [Узнать id.](https://regvk.com/id/)
8. Создайте приложение типа `standalone-приложение`: [Создать.](https://vk.com/apps?act=manage)
9. Скопируйте id приложения и вставьте его в url в следующем пункте.
10. Получите токен доступа к api vk:
    вставьте этот url в адресную строку, в ответном url будет указан token.
```text
https://oauth.vk.com/authorize?client_id=YOUR_APP_ID&display=page&scope=photos,groups,wall,offline&response_type=token&v=5.131&state=123456
```
11. Создайте файл `.env` и сохраните в нем ваш токен, id группы и интервал публикации в секундах:
```text
VK_TOKEN=your_token
VK_GROUP_ID=your_group_id
PUBLICATION_INTERVAL=86400  #  86400 секунд = 24 часа
```

## Запуск
```commandline
python xkcd.py
```

### Запуск в докере на сервере
1. Создать файл .env
2. Выполнить команду
```commandline
docker run -d --name sending_comics_in_vk --restart always --env-file .env nanku/sending_comics_in_vk
```

## Результат
Комикс загрузится на стену группы Вконтакте.<br>
![img.png](img.png)<br>