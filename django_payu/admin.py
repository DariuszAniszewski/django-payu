from django.contrib import admin

from django_payu.models import PayuPayment


class PayuPaymentAdmin(admin.ModelAdmin):
    list_display = ["user", "quantity", "status", "price_net", "price_total", "creation_timestamp",
                    "modification_timestamp"]
    date_hierarchy = "creation_timestamp"
    list_filter = ["status"]
    readonly_fields = ["uid"]

admin.site.register(PayuPayment, PayuPaymentAdmin)