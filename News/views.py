import email
from django.shortcuts import render, redirect,get_object_or_404
 
from django.contrib.auth import authenticate, login

from .forms import UserRegisterForm
from django.contrib import messages
from .models import Article, MyFavorite
from django.views import generic
from django.utils import timezone
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
import requests
from django.contrib.auth.decorators import login_required

# Create your views here.
def welcome(request):
    if  Article.objects.count()>0:
        return render(request, 'news/index.html', {'article_list': Article.objects.all()})      
        
     
    return add_i_db(request)
 
def detail(request, id):
    myarticle  = get_object_or_404(Article, pk=id)
    fav = False
    if   request.user.is_authenticated:
        vfav = MyFavorite.objects.filter(article=myarticle , author=request.user).values()
        if  vfav:
            fav=True

    return render(request, "news/detail.html", {"article": myarticle,"myfav":fav })
    
def signup(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data['username']
            new_user = authenticate(
                email=form.cleaned_data['email'],
                username=username, 
                                    password=form.cleaned_data['password1']
                                    )
            new_user = form.save()
            login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f'Account created for {username}')
            return redirect("/")
    else:
        form = UserRegisterForm()
    return render(request, "registration/signup.html", {"form": form})

 
        
#def setupNews():
def add_i_db(request):
    template_name = 'news/index.html'
    context_object_name = 'article_list'
    is_paginated = True
    paginate_by = 200
    
    url = settings.NEWS_API_BASE_URL+"/top-headlines?country=sa&apiKey="+settings.NEWS_API_KEY
     
    response = requests.get(url)
    articles = response.json()['articles']
    
    # pagination
    paginator = Paginator(articles, paginate_by)
    page = request.GET.get('page')
    try:
        article_list = paginator.page(page)
    except PageNotAnInteger:
        article_list = paginator.page(1)
    except EmptyPage:
        article_list = paginator.page(paginator.num_pages)
    
    for article in article_list:
        x = article['publishedAt']
        article['publishedAt'] = datetime.strptime(x, '%Y-%m-%dT%H:%M:%SZ').strftime("%B %d %Y, %I:%M %p")
        anews= Article()
        anews.author=article['author']
        anews.title=article['title']
        anews.description=article['description']
        anews.url=article['url']
        anews.urlToImage=article['urlToImage']
        anews.content=article['content']
        anews.save()
        

    return render(request, template_name, {'article_list': article_list})  
    
@login_required()
def myfavorit(request):
    
     if  Article.objects.count()>0:
            return render(request, 'news/favorite.html', {'favorite_list':
                MyFavorite.objects.filter(author=request.user)})      
      
    
@login_required()
def deletefav(request, id):
    
    myarticle  = get_object_or_404(Article, pk=id)
     
    fav = MyFavorite.objects.filter(article=myarticle , author=request.user)
    if fav:   
        fav.delete()
    messages.warning(request, f'Favorite deleted!')
    return render(request, "news/detail.html", 
                  {"article": get_object_or_404(Article, pk=id),"myfav":False })
    

@login_required()
def addfav(request,id):
    
    article  = get_object_or_404(Article, pk=id)
    fav= MyFavorite() 
    current_user = request.user
     
    fav.article = get_object_or_404(Article, pk=id)
    fav.author= request.user #current_user.id
    fav.save()
    return render(request, "news/detail.html", 
                  {"article": get_object_or_404(Article, pk=id),"myfav":True })
