from django.conf.urls import url

from django_payu import views

urlpatterns = [
    url(r'^payu/start$', views.start_payment, name='django_pay_payu_start'),
    url(r'^payu/notify$', views.payu_notify, name='django_pay_payu_notify'),
    url(r'^payu/continue/(?P<payment_id>\w+)/$', views.payu_continue, name='django_pay_payu_continue'),
    url(r'^payu/status/(?P<payment_id>\w+)/$', views.payu_status, name='django_pay_payu_status'),
]