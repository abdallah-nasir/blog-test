from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include




urlpatterns = [
    path('admin/', admin.site.urls),
    #Django allauth
    path("",include("BlogApp.urls",namespace="home")),
    path("marketing/",include("marketing.urls",namespace="marketing")),
    #this is the TextEditor
    path('ckeditor/', include('ckeditor_uploader.urls')),
     path('accounts/', include('allauth.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)