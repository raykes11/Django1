from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.generic import TemplateView
from .forms import UserRegister, NumberPage
from django.http import HttpResponse,HttpResponseServerError
from django import forms
from .models import *
# Create your views here.


class Mather(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dict"] = {'Title':Title,"Live":Live,"NotLive":NotLive,'Info':Infos}
        context["other"] = [Title,Live,NotLive,Infos]
        return context


class Menu(Mather):
    template_name = 'fourth_task/menu.html'


class Infos(Mather):
    template_name = 'fourth_task/info.html'
    extra_context={
        "title": "Информация",
        'text' : 'общий список',
        'url'  : '/title/info',
        'name' : 'ИНФО'
    }
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        info = Info.objects.all()
        form = NumberPage()
        per_page = 1
        if request.method == "GET":
            per_page = request.GET.get('number')
        paginator = Paginator(info, per_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        dict_ = {'page_obj': page_obj, 'per_page': per_page, 'form': form}
        return render(request, self.template_name, self.get_context_data(**dict_))

class Title(Mather):
    template_name = 'fourth_task/title.html'
    extra_context={
        "title": "Игра началась",
        'text' : 'Ахалай махалай',
        'url'  : '/title',
        'name' : 'Главная страница'
    }
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class Live(Mather):
    template_name = 'fourth_task/live.html'
    extra_context={
        "title": "Ты выйграл",
        'text' : 'Возьми с полки приражек',
        'url'  : '/title/live',
        'name' : 'Выйграть'
    }
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        games = Game.objects.all()
        context['games'] = games
        context['list'] = ['Черствый','Свежий','Подозрительный']
        return context
class NotLive(Mather):
    template_name = 'fourth_task/not_live.html'
    extra_context={
        "title": "Ты проиграл",
        'text' : 'С тебя  пиражек',
        'url'  : '/title/not_live',
        'name' : 'Проиграть'
    }
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list'] = []
        return context

def sign_up_by_html(request):
    info = {'error': [],'number': 1}
    if request.method == "POST":
        is_corect = True
        login = request.POST.get("login")
        password = request.POST.get("password")
        repeat_password = request.POST.get("repeat_password")
        age = request.POST.get("age")
        print(f'''
        login {login}
        password {password}
        repeat_password {repeat_password}
        age {age}
        ''')
        if password != repeat_password:
            is_corect = False
            info['error'].append('Пароли не совпадают.')
        if int(age) < 18:
            is_corect = False
            info['error'].append('Вы должны быть старше 18.')

        bayers = Buyer.objects.filter(name__contains=login).count()
        if bayers > 0:
            is_corect = False
            info['error'].append('Пользователь уже существует.')
        if is_corect:
            Buyer.objects.create(name=login,balance=1500,age=age)
            return HttpResponse(f"Приветствуем, {login}!")
    return render(request,"fifth_task/registration_page.html", {'info':info})


def sign_up_by_django (request):
    info = {'error': [],'number': 2}
    if request.method == "POST":
        is_corect = True
        form = UserRegister(request.POST)
        if form.is_valid():
            login = form.cleaned_data["login"]
            password = form.cleaned_data["password"]
            repeat_password = form.cleaned_data["repeat_password"]
            age = form.cleaned_data["age"]
        login = request.POST.get("login")
        bayers = Buyer.objects.filter(name__contains=login).count()
        if bayers > 0:
            is_corect = False
            info['error'].append('Пользователь уже существует')
        password = hash(request.POST.get("password"))
        repeat_password = hash(request.POST.get("repeat_password"))
        if password != repeat_password:
            is_corect = False
            info['error'].append('Пароли не совпадают')
        age = request.POST.get("age")
        if int(age)<18:
            is_corect = False
            info['error'].append('Вы должны быть старше 18')
        if is_corect:
            Buyer.objects.create(name=login,balance=1500,age=age)
            return HttpResponse(f"Приветствуем, {login}!")
    else:
        form = UserRegister()
    return render(request,"fifth_task/registration_page.html",{"form":form,'info':info})



def retetet(request):
    info = Info.objects.all()
    per_page = 0
    if request.method == "POST":
        print(f"""
        {request.method} 
        {request.POST.get('number')}
        """)
        form = NumberPage(request.POST)
        per_page = request.POST.get('number')
    if per_page == 0:
        per_page = 3
    paginator = Paginator(info, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    form = NumberPage()

    return render(request,"fourth_task/info.html",{"form":form,'info':per_page})