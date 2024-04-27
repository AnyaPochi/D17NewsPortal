from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')), # подключаем встроенные эндопинты для работы с локализацией
    path('admin/', admin.site.urls),
    path('news/', include('news.urls')),

    path('accounts/', include('allauth.urls')),
    # path('', include('news.urls')),
]
