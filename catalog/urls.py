from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('',views.books,name='books'),
    path('',views.authors,name='authors'),
] 