from django.contrib import admin

from rent_api.models import RentUnit, Lease, Review

# Register your models here.
admin.site.register(RentUnit)
admin.site.register(Lease)
admin.site.register(Review)