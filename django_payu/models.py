from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_payu.helpers import PaymentStatus


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


class PayuPayment(models.Model):
    payment_id = models.CharField(max_length=64, primary_key=True, help_text=_("Will be auto-generated"))
    payment_status = models.CharField(max_length=16, choices=STATUSES)
    payment_description = models.TextField(default="Your description")
    payu_id = models.CharField(max_length=128, blank=True, null=True)
    buyer_first_name = models.CharField(max_length=64)
    buyer_last_name = models.CharField(max_length=64)
    buyer_email = models.EmailField()
    buyer_ip_address = models.GenericIPAddressField(protocol="IPv4")
    product_name = models.CharField(max_length=128)
    product_unit_price = models.IntegerField()
    product_quantity = models.IntegerField(default=1)

    creation_timestamp = models.DateTimeField(auto_now_add=True)
    modification_timestamp = models.DateTimeField(auto_now=True)

    payu_messages_log = models.TextField()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.payment_id:
            self.payment_id = uuid4().hex
        super(PayuPayment, self).save(force_insert, force_update, using, update_fields)

    @property
    def total_price(self):
        return self.product_unit_price * self.product_quantity
