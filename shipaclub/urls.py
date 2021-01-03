from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# отключение кеширования
from django.contrib.staticfiles.views import serve
from django.views.decorators.cache import never_cache

urlpatterns = [
    path('accounts/', include('Accounts.urls')),
    path('posts/', include('PBoard.urls')),
    path('', include('Mainpage.urls')),
    path('admin/', admin.site.urls),
]
if settings.DEBUG:
    urlpatterns +=  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns.append(path('static/<path:path>', never_cache(serve)))#отключение кеширования 