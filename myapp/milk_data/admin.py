# core/admin.py

from django.contrib import admin
from .models import Breed, District, Supplier, Cow, MilkSubmission

# This customization improves how the Supplier list is displayed in the admin panel.
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    # Columns to display in the supplier list
    list_display = ('name', 'rf_no', 'district', 'total_cows', 'warning_count')
    # Fields to search by
    search_fields = ('name', 'rf_no')
    # Filters that appear on the side
    list_filter = ('district', 'warning_count')

# This customization improves the Cow list display.
@admin.register(Cow)
class CowAdmin(admin.ModelAdmin):
    list_display = ('cow_name', 'supplier', 'breed', 'last_vaccination_date')
    search_fields = ('cow_name', 'supplier__name')
    list_filter = ('breed', 'supplier__district')

# This customization improves the Milk Submission list display.
@admin.register(MilkSubmission)
class MilkSubmissionAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'quality_of_milk', 'timestamp')
    search_fields = ('supplier__name',)
    list_filter = ('quality_of_milk', 'timestamp', 'supplier__district')

# Register the simple models without special customizations.
admin.site.register(Breed)
admin.site.register(District)