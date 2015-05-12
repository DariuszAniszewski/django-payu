from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_pay.helpers import PaymentStatus


STATUSES = (
    (PaymentStatus.STATUS_NEW, _("New")),
    (PaymentStatus.STATUS_STARTED, _("Started")),
    (PaymentStatus.STATUS_FAILED, _("Failed")),
    (PaymentStatus.STATUS_COMPLETED, _("Completed")),
)

CURRENCIES = (
    ("pln", "PLN"),
    ("eur", "EUR"),
    ("usd", "USD"),
)


class Product(models.Model):
    uid = models.CharField(max_length=64, primary_key=True, help_text=_("Will be auto-generated"))
    name = models.CharField(max_length=128)
    price_net = models.IntegerField()
    price_total = models.IntegerField()
    vat_rate = models.FloatField(default=0.23)
    pkwiu_code = models.CharField(blank=True, null=True, max_length=16)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.uid:
            self.uid = uuid4().hex
        super(Product, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return u"{}".format(self.name)


class Payment(models.Model):
    uid = models.CharField(max_length=64, primary_key=True, help_text=_("Will be auto-generated"))
    user = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=16, choices=STATUSES)

    creation_timestamp = models.DateTimeField(auto_now_add=True)
    modification_timestamp = models.DateTimeField(auto_now=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.uid:
            self.uid = uuid4().hex
        super(Payment, self).save(force_insert, force_update, using, update_fields)

    @property
    def price_net(self):
        return self.product.price_net * self.quantity

    @property
    def price_total(self):
        return self.product.price_total * self.quantity


class PayuPayment(Payment):
    payu_id = models.CharField(max_length=128, blank=True, null=True)