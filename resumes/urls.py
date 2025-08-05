from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('match/', views.match_resume, name='match_resume'),
    path('history/', views.match_history, name='match_history'),
    path('profile/', views.profile_view, name='profile'),
    


    
]
