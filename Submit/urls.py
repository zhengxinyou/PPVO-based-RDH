from django.conf.urls import url

from Submit import views

urlpatterns = [
    url(r'^index/', views.index),
    url(r'^embed/', views.UploadView.as_view(), name='embed'),
    url(r'^get/', views.get_image),
    url(r'^getinfo/', views.getInfoView.as_view(), name='getinfo'),
    url(r'^extract/', views.extractImgView.as_view(), name='extract')
]