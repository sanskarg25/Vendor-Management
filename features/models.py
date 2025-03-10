import datetime, pytz
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

timezone = pytz.timezone("Asia/Kolkata")

class TimeStampedModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True

class FeaturesVendorsProfileModel(TimeStampedModel):
    vendor_code = models.CharField(unique=True)
    name = models.CharField(max_length=1000)
    contact_details = models.TextField()
    address = models.TextField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    class Meta:
        verbose_name = "Vendor Profile Model"
        verbose_name_plural = "Vendor Profile Models"


class FeaturesPurchaseOrderModel(TimeStampedModel):
    po_number = models.CharField(unique=True)
    vendor = models.ForeignKey(
        FeaturesVendorsProfileModel,
        on_delete=models.CASCADE,
        related_name="FeaturesPurchaseOrder_vendor"
    )
    order_date = models.DateField(auto_now_add=True)
    delivery_date = models.DateField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField()
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Purchase Order Model"
        verbose_name_plural = "Purchase Order Models"

class FeaturesHistoricalPerformanceModel(TimeStampedModel):
    vendor = models.ForeignKey(
        FeaturesVendorsProfileModel,
        on_delete=models.CASCADE,
        related_name="FeaturesHistoricalPerformanceModel_vendor"
    )
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    class Meta:
        verbose_name = "Historical Performance Model"
        verbose_name_plural = "Historical Performance Models"
