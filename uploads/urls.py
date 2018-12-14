from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from uploads.core import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^uploads/simple/$', views.simple_upload, name='simple_upload'),
    url(r'^uploads/simple/model/', views.model, name='model'),
    url(r'^admin/', admin.site.urls),
    url(r'^form/$',views.form,name="form"),
    url(r'^upload',views.upload,name="upload"),
    url(r'^export/csv/$', views.export_users_csv, name='export_users_csv'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
