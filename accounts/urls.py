
from django.urls import path
from accounts.views import login_views, logout_view, register_view




urlpatterns = [
    path('login/', login_views, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
]