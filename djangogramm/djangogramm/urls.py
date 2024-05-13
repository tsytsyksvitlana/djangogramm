from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('post.urls')),
    path('', include('user_profile.urls')),
    path('', include('authenticate.urls')),
    path('', include('comment.urls')),
]

# if settings.DEBUG:
urlpatterns += static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
)
