from django.contrib import admin
from features.models import (
    FeaturesVendorsProfileModel,
    FeaturesPurchaseOrderModel,
    FeaturesHistoricalPerformanceModel,
)
# Register your models here.

@admin.register(FeaturesVendorsProfileModel)
class FeaturesVendorsProfileModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "vendor_code", 
        "name", 
        "contact_details"
        )
    search_fields = (
        "id",
        "vendor_code", 
        "name", 
        "contact_details"
    )

@admin.register(FeaturesPurchaseOrderModel)
class FeaturesPurchaseOrderModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "vendor_id", 
        "po_number", 
        "order_date"
        )
    search_fields = (
        "id",
        "vendor_id", 
        "po_number", 
        "order_date"
    )

@admin.register(FeaturesHistoricalPerformanceModel)
class FeaturesHistoricalPerformanceModelAdmin(admin.ModelAdmin):
    list_display = (
        "vendor_id", 
        "date",
        )
    search_fields = (
        "vendor_id", 
        "date",
    )
