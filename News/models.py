 
 
from django.db import models

from Home.models import MyUser
 
#from django.contrib.auth.models import User

 
    
# Create your models here.
class Article(models.Model):
    author = models.CharField(max_length=1000,default=None, blank=True, null=True)
    title = models.CharField(max_length=1000,default=None, blank=True, null=True)
    description = models.CharField(max_length=1000,default=None, blank=True, null=True)
    url = models.CharField(max_length=1000,default=None, blank=True, null=True)
    urlToImage = models.CharField(max_length=1000,default=None, blank=True, null=True)
    publishedAt = models.CharField(max_length=1000,default=None, blank=True, null=True)
    content = models.CharField(max_length=1000,default=None, blank=True, null=True)
    #source =Source
     
    def __str__(self):
        return f"{self.title}"
    
    
class Source (models.Model):
     #id = models.CharField(max_length=225)
     name = models.CharField(max_length=500,default=None, blank=True, null=True)
     def __str__(self):
        return f"{self.name}"
    
    
class MyFavorite(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, default=1)
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, default=1)
    def __str__(self):
        return f"{self.article.title}"   