from django.conf.urls import url
from django.contrib import admin


from app.views import *

urlpatterns = [
    url(r'^$', IndexView.as_view()),
    url(r'admin/', admin.site.urls),

    url(r'login$', LoginView.as_view()),
    url(r'logout$', LogoutView.as_view()),

    url(r'new$', FileNewView.as_view()),
    url(r'edit/(?P<store>[-\w]+)$', FileEditView.as_view()),

    url(r'list/all$', ListAllView.as_view()),

    url(r'save$', FileSaveView.as_view()),



]
