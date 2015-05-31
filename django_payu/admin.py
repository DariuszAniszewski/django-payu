from django.contrib import admin

from django_payu.models import PayuPayment


class PayuPaymentAdmin(admin.ModelAdmin):
    list_display = ["payment_id", "payment_status", "payu_id", "product_name", "total_price", "creation_timestamp",
                    "modification_timestamp"]
    date_hierarchy = "creation_timestamp"
    list_filter = ["payment_status"]
    readonly_fields = ["payment_id"]

admin.site.register(PayuPayment, PayuPaymentAdmin)