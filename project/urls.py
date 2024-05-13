from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from news import views
from django.views.generic import TemplateView


router = routers.DefaultRouter()
router.register(r'news2', views.NewsViewset, basename='news')
router.register(r'articles2', views.ArtcViewset, basename='articles')
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')), # подключаем встроенные эндопинты для работы с локализацией
    path('admin/', admin.site.urls),
    path('news/', include('news.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('swagger-ui/', TemplateView.as_view(
       template_name='swagger-ui.html',
       extra_context={'schema_url':'openapi-schema'}
   ), name='swagger-ui'),
]
