from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home_view, name='home' ),
    path('login/', views.login_view, name='login' ),
    path('logout/', views.logout_view, name='logout' ),
    path('register/', views.register_view, name='register' ),
    path('supprimer/<str:name>/', views.supprimer, name='supprimer'),
    path('update/<str:name>/', views.update, name='update'),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)