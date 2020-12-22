from django.urls import path, re_path

from account.views import Login, Logout, RegisterView

urlpatterns = [
    # path('login/', login_view, name='login'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    # path('logout/', logout_view, name='logout'),
    # path('register/', register_view, name='register'),
    path('register/', RegisterView.as_view(), name='register'),
]