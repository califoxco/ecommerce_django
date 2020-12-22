from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('register/', user_views.register, name="register"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
