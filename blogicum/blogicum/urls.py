from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from pages.views import page_not_found, internal_server_error, forbidden
from blog.views import RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls', namespace='blog')),
    path('pages/', include('pages.urls', namespace='pages')),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/registration/', RegisterView.as_view(), name='registration'),
]

handler403 = forbidden
handler404 = page_not_found
handler500 = internal_server_error


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
