from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path('signup', views.signup, name="signup"),
    path('login', views.login, name="login"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('show', views.show, name="show"),
    path('add', views.add, name="add"),
    path('myplaces', views.myplaces, name="myplaces"),
    path('place/<id>', views.place, name="place"),
    path('removePlace/<id>', views.removing, name="removePlace")
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
