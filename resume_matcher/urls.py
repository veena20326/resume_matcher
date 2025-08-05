from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('resumes/', include('resumes.urls')),  # ✅ Connect app
    path('', include('resumes.urls')),  # NEW: for login/register
    
]

# ✅ Media file support (resume PDF upload)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
