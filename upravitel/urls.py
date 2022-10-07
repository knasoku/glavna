from django.urls import path, include
from . import views as upravitel_views


urlpatterns = [
    path('', upravitel_views.upravitel_home, name='upravitel_home'),
    path('zgrada/<zgrada_id>/', upravitel_views.zgrada_home, name='zgrada_home'),
    path('zgradaupdate/<zgrada_id>/', upravitel_views.zgrada_update, name='zgrada_update'),
    path('dodadistanar/<zgrada_id>/', upravitel_views.dodadi_stanar, name='dodadi_stanar'),
    path('izbrisistanar/<zgrada_id>/', upravitel_views.izbrisi_stanar, name='izbrisi_stanar'),
    path('create/', upravitel_views.create, name='create'),
    path('announcement/', upravitel_views.announcement, name='announcement'),

]
