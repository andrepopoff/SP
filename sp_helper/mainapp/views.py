from django.shortcuts import render


def main(request):
    return render(request, 'mainapp/index.html')


def account(request):
    return render(request, 'mainapp/account.html')

