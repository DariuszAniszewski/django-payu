from django.conf.urls import url

from django_payu import views

urlpatterns = [
    url(r'^payu/notify$', views.payu_notify, name='django_pay_payu_notify'),
]