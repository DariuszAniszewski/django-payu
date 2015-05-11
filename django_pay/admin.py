from django.contrib import admin
from django_pay.models import Product, PayuPayment


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price_net", "price_total", "vat_rate", "pkwiu_code"]
    readonly_fields = ["uid"]


class PayuPaymentAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "quantity", "status", "price_net", "price_total", "creation_timestamp",
                    "modification_timestamp"]
    date_hierarchy = "creation_timestamp"
    list_filter = ["status"]
    readonly_fields = ["uid"]

admin.site.register(Product, ProductAdmin)
admin.site.register(PayuPayment, PayuPaymentAdmin)