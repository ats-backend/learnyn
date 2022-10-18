from django.shortcuts import render


def index(request):
    return render(request, 'base.html')


def profile(request):
    return render(request, 'edit_profile.html')


def item_list(request):
    return render(request, 'items_list.html')

def item_list_two(request):
    return render(request, 'item_list_2.html')


def results(request):
    return render(request, 'results.html')

def detail(request):
    return render(request, 'detail.html')


