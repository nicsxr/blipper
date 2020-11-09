import account.views as views
from django.urls import path

urlpatterns = [
	path('register/', views.registration_view, name='registration'),
	path('logout/', views.logout_view, name='logout'),
	path('login/', views.login_view, name='login'),
	path('settings/', views.user_update_view, name='settings'),
]