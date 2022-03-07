
from unicodedata import name
from django.urls import path,include
from .views import *
urlpatterns = [
    path('',home,name="home"),
    path('vacancy/',vacancy,name="vac"),
    path('book/',book,name="vac"),
    path('clear/',clear_db,name="db_clear")

]
