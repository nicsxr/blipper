import main.views as views
from django.urls import path

urlpatterns = [
	path('', views.home_view, name='home'),
	path('profile/<id>', views.profile_view, name='profile'),

	path('like/<id>', views.like_post, name='like'),
	path('follow/<id>', views.follow_user, name='follow'),
	path('search/<name>', views.search_user, name='search'),
]