import vk
import re
from db_models import StopAlbum, db_session, TopicMessage


MY_USER_ID = '7978511'
APP_ID = '6273721'


class VkHandler:
    def __init__(self, my_user_id, app_id):
        self.__my_user_id = my_user_id
        self.__app_id = app_id

        self.__vk_session = vk.AuthSession(app_id=APP_ID, user_login='andre-popoff@mail.ru', user_password='Lub08m270388',
                                    scope='groups')
        self.__vk_api = vk.API(self.__vk_session, timeout=30)

    def create_first_topic_msg(self):
        pattern = r'_[0-9]+$'
        # 'https://vk.com/album-47985581_237024723'

        album_link = input('Введите ссылку на альбом: ')
        album_id = re.search(pattern, album_link).group()[1:]
        album_info = self.__vk_api.photos.getAlbums(v='5.0', owner_id=-47985581, album_ids=album_id)

        stop_album = StopAlbum(album_info['items'][0]['title'], album_link, 1)
        db_session.add(stop_album)
        db_session.commit()

        with open('first_topic_text.txt', 'r') as f:
            f.read().rstrip()

        q_first_text = db_session.query(TopicMessage).filter_by(id=1).first()
        first_text = q_first_text.text
        album = '{}: {}'.format(stop_album.name, stop_album.link)
        text = first_text + '\n' + album

        return text

    def create_new_topic(self):
        topic_title = input('Название списка: ')
        first_text = self.create_first_topic_msg()
        new_topic = self.__vk_api.board.addTopic(v='5.0', group_id=47985581,
                                          title=topic_title, text=first_text,
                                          from_group=1)
        print(new_topic)


if __name__ == '__main__':
    vk_handler = VkHandler(MY_USER_ID, APP_ID)
    vk_handler.create_new_topic()
