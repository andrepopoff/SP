from django.shortcuts import render
from .vk_handler.vk_topics import VkHandler
import os


MY_USER_ID = '7978511'
APP_ID = '6273721'


def main(request):
    return render(request, 'mainapp/index.html')


def account(request):
    path = os.path.join('mainapp', 'vk_handler', 'pass.txt')

    with open(path, 'r') as f:
        login, password = [line.rstrip() for line in f]

    vk_handler = VkHandler(MY_USER_ID, APP_ID, login, password)
    comments = vk_handler.get_all_album_comments()

    return render(request, 'mainapp/account.html', {'items': comments['items']})

