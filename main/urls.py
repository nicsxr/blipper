import main.views as views
from django.urls import path

urlpatterns = [
	path('', views.home_view, name='home'),
	path('like/<id>', views.like_post, name='like'),
]