import vk
import re
from db_models import StopAlbum, db_session, TopicMessage

MY_USER_ID = '7978511'
APP_ID = '6273721'

vk_session = vk.AuthSession(app_id=APP_ID, user_login='andre-popoff@mail.ru', user_password='Lub08m270388',
                             scope='groups')
vk_api = vk.API(vk_session, timeout=30)
pattern = r'_[0-9]+$'

# 'https://vk.com/album-47985581_237024723'

try:
    album_link = input('Введите ссылку на альбом: ')
    album_id = re.search(pattern, album_link).group()[1:]
    album_info = vk_api.photos.getAlbums(v='5.0', owner_id=-47985581, album_ids=album_id)

    stop_album = StopAlbum(album_info['items'][0]['title'], album_link, 1)
    db_session.add(stop_album)
    db_session.commit()

    with open('first_topic_text.txt', 'w') as f:
        q_first_text = db_session.query(TopicMessage).filter_by(id=1).first()
        first_text = q_first_text.text
        album = '{}: {}'.format(stop_album.name, stop_album.link)
        text = first_text + '\n' + album
        f.write(text)

except AttributeError:
    print('Неверная ссылка на альбом!')
