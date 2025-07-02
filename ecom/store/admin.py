from django.contrib import admin

# Register your models here.

from store.models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ['pname', 'prize', 'discount_price']

admin.site.register(Product, ProductAdmin)

# admin.site.register(Product)



