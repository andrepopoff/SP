import vk
import re
from .db_models import StopAlbum, db_session, TopicMessage, PaymentInfo


MY_USER_ID = '7978511'
APP_ID = '6273721'


class VkHandler:
    def __init__(self, my_user_id, app_id, login, password):
        self.__my_user_id = my_user_id
        self.__app_id = app_id
        self.__login = login
        self.__password = password
        self.__vk_session = vk.AuthSession(app_id=APP_ID, user_login=self.__login, user_password=self.__password,
                                    scope='groups, photos')
        self.__vk_api = vk.API(self.__vk_session, timeout=10)

    def create_first_topic_msg(self):
        # ----> Позже сделать на django формах

        pattern = r'_[0-9]+$'
        # 'https://vk.com/album-47985581_237024723'

        albums = {}
        album_link = input('Введите ссылку на альбом: ')
        while album_link:
            album_id = re.search(pattern, album_link).group()[1:]
            album_info = self.__vk_api.photos.getAlbums(v='5.0', owner_id=-47985581, album_ids=album_id)

            stop_album = StopAlbum(album_info['items'][0]['title'], album_link, 1)
            stop_album.save_in_db()

            albums[stop_album.link] = stop_album.name
            album_link = input('Введите ссылку на альбом: ')

        q_first_text = db_session.query(TopicMessage).filter_by(id=1).first()
        first_text = q_first_text.text

        for k, v in albums.items():
            first_text += '\n{}: {}'.format(v, k)

        return first_text

    def create_new_topic(self):
        topic_title = input('Название списка: ')
        first_text = self.create_first_topic_msg()
        return self.__vk_api.board.addTopic(v='5.0', group_id=47985581,
                                          title=topic_title, text=first_text,
                                          from_group=1)

    def add_payment_info_in_topic(self, topic_id):
        # ----> Позже сделать на django формах

        pay_id = input('Введите id платежной информации (1 или 2): ')

        q_message = db_session.query(PaymentInfo).filter_by(id=pay_id).first()
        message = '{}\n\nРЕКВИЗИТЫ\nПолучатель: {}\n№ карты: {}\n{}\n\n{}'.format(q_message.first_msg, q_message.recipient,
                                                                                  q_message.card_number,
                                                                                  q_message.card_type, q_message.end_msg)

        self.__vk_api.board.createComment(v='5.0', group_id=47985581,
                                          topic_id=topic_id, message=message,
                                          from_group=1)

    @staticmethod
    def create_new_payment_info():
        # ----> Позже сделать на django формах

        first_msg = input('Текст заголовка: ')
        recipient = input('ФИО владельца карты: ')
        card_number = input('Номер карты: ')
        card_type = input('Тип карты: ')
        end_msg = input('Текст в конце: ')

        pay_info = PaymentInfo(first_msg, recipient, card_number, card_type, end_msg)
        pay_info.save_in_db()

    def get_all_album_comments(self):
        comments = self.__vk_api.photos.getAllComments(v='5.0', owner_id=-47985581, album_id=238502941, offset=0, count=100)
        price_pattern1 = r'(?P<price>\d+)\sруб[\.\s]+'
        price_pattern2 = r'(?P<price>\d+)\sр[\.\s]+'
        price_pattern3 = r'(?P<price>\d+)руб[\.\s]+'
        price_pattern4 = r'(?P<price>\d+)р[\.\s]+'
        count_pattern = r'^\+(?P<count>\d+)'

        for item in comments['items']:
            if str(item['from_id'])[0] == '-':
                user = self.__vk_api.groups.getById(v='5.0', group_id=str(item['from_id'])[1:], fields='photo_100')
            else:
                user = self.__vk_api.users.get(v='5.0', user_ids=item['from_id'], fields='photo_100')
            photo = self.__vk_api.photos.getById(v='5.0', photos='{}_{}'.format(-47985581, item['pid']))
            item['photo_info'] = photo
            item['user_info'] = user

            for p in (price_pattern1, price_pattern2, price_pattern3, price_pattern4):
                price = re.search(p, item['photo_info'][0]['text'])
                if price:
                    item['price'] = price.group('price')
                    break

            count = re.search(count_pattern, item['text'])
            if count:
                item['count'] = count.group('count')

        return comments


if __name__ == '__main__':
    with open('pass.txt', 'r') as f:
        login, password = [line.rstrip() for line in f]

    vk_handler = VkHandler(MY_USER_ID, APP_ID, login, password)
    # vk_handler.add_payment_info_in_topic(37515920)
    # db_session.close()
    print(vk_handler.get_all_album_comments())
