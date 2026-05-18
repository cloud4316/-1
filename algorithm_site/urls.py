from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

def handle_chrome_devtools(request):
    """Обработка запросов Chrome DevTools"""
    return HttpResponse('', status=404)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('works.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    # Обработка Chrome DevTools
    path('.well-known/<path:path>', handle_chrome_devtools, name='chrome_devtools'),
]

# Медиафайлы отдаём всегда (студенты загружают решения, DEBUG не важен)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
