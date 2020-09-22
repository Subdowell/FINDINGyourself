
from django.urls import path
from accounts.views import login_views, logout_views, register_views, update_views, delete_views, contact_views

urlpatterns = [
    path('login/', login_views, name='login'),
    path('logout/', logout_views, name='logout'),
    path('register/', register_views, name='register'),
    path('update/', update_views, name='update'),
    path('delete/', delete_views, name='delete'),
    path('contact/', contact_views, name='contact'),
]