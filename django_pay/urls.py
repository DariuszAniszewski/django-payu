from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^test$', views.test_view, name='test_view'),
    url(r'^payu/start$', views.start_payment, name='django_pay_payu_start'),
    url(r'^payu/notify$', views.test_view, name='django_pay_payu_notify'),
    url(r'^payu/continue/(?P<payment_id>\w+)/$', views.payu_continue, name='django_pay_payu_continue'),
    url(r'^payu/status/(?P<payment_id>\w+)/$', views.payu_status, name='django_pay_payu_status'),
]