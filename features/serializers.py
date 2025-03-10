import datetime, random, pytz, logging, threading
from vendor_management.settings import logger
from rest_framework import serializers
from features.models import (
    FeaturesVendorsProfileModel,
    FeaturesPurchaseOrderModel,
    FeaturesHistoricalPerformanceModel,
)

timezone = pytz.timezone("Asia/Kolkata")

class FeaturesVendorCreationSerializer(serializers.Serializer):
    """
    Serializer for creating vendors
    """
    api_logger = logging.LoggerAdapter(logger, {"app_name": "FeaturesVendorCreationSerializer"})

    vendor_code = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    address = serializers.CharField(required=True)
    contact_details = serializers.CharField(required=True)
    on_time_delivery_rate = serializers.FloatField(required=False)
    quality_rating_avg = serializers.FloatField(required=False)
    average_response_time = serializers.FloatField(required=False)
    fulfillment_rate = serializers.FloatField(required=False)

    def validate(self, data):
        """ validations for creating vendor """

        if FeaturesVendorsProfileModel.objects.filter(vendor_code=data["vendor_code"]).exists():
            raise serializers.ValidationError("Vendor already exists!")

        if FeaturesVendorsProfileModel.objects.filter(contact_details=data["contact_details"]).exists():
            raise serializers.ValidationError("Vendor contact details already exists!")
        return data
    
    def create(self, validated_data):
        """ creating vendor """

        FeaturesVendorsProfileModel.objects.create(
            vendor_code = validated_data["vendor_code"],
            name = validated_data["name"],
            address = validated_data["address"],
            contact_details = validated_data["contact_details"],
            on_time_delivery_rate = validated_data.get("on_time_delivery_rate", 0.0),
            quality_rating_avg = validated_data.get("quality_rating_avg", 0.0),
            average_response_time = validated_data.get("average_response_time", 0.0),
            fulfillment_rate = validated_data.get("fulfillment_rate", 0.0),
            created_date=datetime.datetime.now(timezone),
            updated_date=datetime.datetime.now(timezone)
        )
        return validated_data
    
class FeaturesVendorListSerializer(serializers.Serializer):
    """
    Serializer for getting vendors list
    """
    api_logger = logging.LoggerAdapter(logger, {"app_name": "FeaturesVendorListSerializer"})

    data = serializers.CharField(required=False)
    
    def create(self, validated_data):
        """ creating list of vendors """

        vendors = list(FeaturesVendorsProfileModel.objects.all().values().order_by("-updated_date"))
        
        for vendor in vendors:
            vendor['created_date'] = str(vendor['created_date'])
            vendor['updated_date'] = str(vendor['updated_date'])

        validated_data["data"] = {
                                "total_vendors": len(vendors),
                                "vendors": vendors
                            }
        return validated_data

class FeaturesVendorGetDetailsSerializer(serializers.Serializer):
    """
    Serializer for vendor details by id
    """
    api_logger = logging.LoggerAdapter(logger, {"app_name": "FeaturesVendorGetDetailsSerializer"})

    details = serializers.CharField(required=False)

    def validate(self, data):
        """ validation of vendor existence """
        vendor_id = self.context["vendor_id"]
        if not FeaturesVendorsProfileModel.objects.filter(id=vendor_id):
            raise serializers.ValidationError("Vendor doesnot exists!")
        return data
    
    def create(self, validated_data):
        """ creating details by id """
        vendor_id = self.context["vendor_id"]
        vendor = FeaturesVendorsProfileModel.objects.filter(id=vendor_id).values()[0]
        vendor["created_date"] = str(vendor["created_date"])
        vendor["updated_date"] = str(vendor["updated_date"])
        validated_data["details"] = {"vendor_details": vendor}
        return validated_data

class FeaturesVendorUpdateSerializer(serializers.Serializer):
    """
    Serializer for updating vendor
    """
    api_logger = logging.LoggerAdapter(logger, {"app_name": "FeaturesVendorUpdateSerializer"})

    vendor_code = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    contact_details = serializers.CharField(required=False)
    on_time_delivery_rate = serializers.FloatField(required=False)
    quality_rating_avg = serializers.FloatField(required=False)
    average_response_time = serializers.FloatField(required=False)
    fulfillment_rate = serializers.FloatField(required=False)

    def validate(self, data):
        """ validations for updating vendor """
        vendor_id = self.context["vendor_id"]
        if not FeaturesVendorsProfileModel.objects.filter(id=vendor_id).exists():
            raise serializers.ValidationError("Vendor doesnot exists!")
        
        vendor_contact_details = FeaturesVendorsProfileModel.objects.get(id=vendor_id).contact_details
        if "contact_details" in data and vendor_contact_details != data["contact_details"]:
            if FeaturesVendorsProfileModel.objects.filter(contact_details=data["contact_details"]).exists():
                raise serializers.ValidationError("Vendor contact details exists!")
        return data
    
    def create(self, validated_data):
        """ updating vendor """
        vendor_id = self.context["vendor_id"]
        vendor_obj = FeaturesVendorsProfileModel.objects.get(id=vendor_id)

        for key, value in validated_data.items():
            setattr(vendor_obj, key, value)
        
        vendor_obj.updated_date = datetime.datetime.now(timezone)
        vendor_obj.save()

        return validated_data

class FeaturesVendorDeleteSerializer(serializers.Serializer):
    """
    Serializer for deleting vendor
    """
    api_logger = logging.LoggerAdapter(logger, {"app_name": "FeaturesVendorDeleteSerializer"})
    
    def validate(self, data):
        """ validations for deleting vendor """
        vendor_id = self.context["vendor_id"]
        if not FeaturesVendorsProfileModel.objects.filter(id=vendor_id).exists():
            raise serializers.ValidationError("Vendor doesnot exists!")

        return data
    
    def create(self, validated_data):
        """ deleting vendor """
        vendor_id = self.context["vendor_id"]
        FeaturesVendorsProfileModel.objects.get(id=vendor_id).delete()

        return validated_data
    
class FeaturesPurchaseOrderCreationSerializer(serializers.Serializer):
    """
    Serializer for creating purhcase orders
    """
    api_logger = logging.LoggerAdapter(logger, {"app_name": "FeaturesPurchaseOrderCreationSerializer"})

    po_number = serializers.CharField(required=True)
    vendor_id = serializers.IntegerField(required=True)
    order_date = serializers.DateField(required=True)
    delivery_date = serializers.DateField(required=True)
    items = serializers.JSONField(required=True)
    quantity = serializers.IntegerField(required=True)
    status = serializers.CharField(required=True)
    issue_date = serializers.DateTimeField(required=False)

    def validate(self, data):
        """ validations for creating purchase order """

        if FeaturesPurchaseOrderModel.objects.filter(po_number=data["po_number"]).exists():
            raise serializers.ValidationError("PO number already exists!")

        if not FeaturesVendorsProfileModel.objects.filter(id=data["vendor_id"]).exists():
            raise serializers.ValidationError("Vendor not exists!")
        return data
    
    def create(self, validated_data):
        """ creating purchase order """

        FeaturesPurchaseOrderModel.objects.create(
            po_number = validated_data["po_number"],
            vendor_id = validated_data["vendor_id"],
            order_date = validated_data["order_date"],
            delivery_date = validated_data["delivery_date"],
            items = validated_data["items"],
            quantity = validated_data["quantity"],
            status = validated_data.get("status", "pending"),
            issue_date = validated_data.get("issue_date", datetime.datetime.now(timezone)),
            created_date=datetime.datetime.now(timezone),
            updated_date=datetime.datetime.now(timezone)
        )
        return validated_data
    
class FeaturesPurchaseOrderListSerializer(serializers.Serializer):
    """
    Serializer for getting purchase order list
    """
    api_logger = logging.LoggerAdapter(logger, {"app_name": "FeaturesPurchaseOrderListSerializer"})

    data = serializers.CharField(required=False)
    
    def create(self, validated_data):
        """ creating list of purchase order """

        purchase_orders = list(FeaturesPurchaseOrderModel.objects.all().values().order_by("-updated_date"))
        
        for purchase_order in purchase_orders:
            purchase_order['created_date'] = str(purchase_order['created_date'])
            purchase_order['updated_date'] = str(purchase_order['updated_date'])

        validated_data["data"] = {
                                "total_purchase_orders": len(purchase_orders),
                                "purchase_orders": purchase_orders
                            }
        return validated_data

class FeaturesPurchaseOrderGetDetailsSerializer(serializers.Serializer):
    """
    Serializer for purchase order details by id
    """
    api_logger = logging.LoggerAdapter(logger, {"app_name": "FeaturesPurchaseOrderGetDetailsSerializer"})

    details = serializers.CharField(required=False)

    def validate(self, data):
        """ validation of purchase order existence """
        po_id = self.context["po_id"]
        if not FeaturesPurchaseOrderModel.objects.filter(id=po_id):
            raise serializers.ValidationError("Purchase Order doesnot exists!")
        return data
    
    def create(self, validated_data):
        """ creating details by id """
        po_id = self.context["po_id"]
        purchase_order = FeaturesPurchaseOrderModel.objects.filter(id=po_id).values()[0]
        purchase_order["created_date"] = str(purchase_order["created_date"])
        purchase_order["updated_date"] = str(purchase_order["updated_date"])
        validated_data["details"] = {"purchase_order_details": purchase_order}
        return validated_data

class FeaturesPurchaseOrderUpdateSerializer(serializers.Serializer):
    """
    Serializer for updating purchase order
    """
    api_logger = logging.LoggerAdapter(logger, {"app_name": "FeaturesVendorUpdateSerializer"})

    po_number = serializers.CharField(required=False)
    vendor_id = serializers.IntegerField(required=False)
    order_date = serializers.DateField(required=False)
    delivery_date = serializers.DateField(required=False)
    items = serializers.JSONField(required=False)
    quantity = serializers.IntegerField(required=False)
    status = serializers.CharField(required=False)
    issue_date = serializers.DateField(required=False)
    quality_rating = serializers.FloatField(required=False)

    def validate(self, data):
        """ validations for updating purchase order """
        po_id = self.context["po_id"]
        if not FeaturesPurchaseOrderModel.objects.filter(id=po_id).exists():
            raise serializers.ValidationError("Purchase Order doesnot exists!")
        
        if "po_number" in data and FeaturesPurchaseOrderModel.objects.filter(po_number=data["po_number"]).exists():
            raise serializers.ValidationError("PO Number already exists!")

        if "vendor_id" in data and not FeaturesVendorsProfileModel.objects.filter(id=data["vendor_id"]).exists():
            raise serializers.ValidationError("Vendor doesnot exists!")

        return data
    
    def create(self, validated_data):
        """ updating purchase order """
        po_id = self.context["po_id"]
        po_obj = FeaturesPurchaseOrderModel.objects.get(id=po_id)
        for key, value in validated_data.items():
            setattr(po_obj, key, value)
        
        po_obj.updated_date = datetime.datetime.now(timezone)
        po_obj.save()

        if "status" in validated_data and validated_data["status"] == "completed":

            """ on time delivery rate calculation """
            on_time_delivery_rate = 0
            completed_pos = FeaturesPurchaseOrderModel.objects.filter(vendor=po_obj.vendor, status="completed")
            completed_on_time_pos = completed_pos.filter(delivery_date__lte=po_obj.delivery_date).count()
            completed_pos = completed_pos.count()
            if completed_pos > 0:
                on_time_delivery_rate = completed_on_time_pos / completed_pos
            
            """ fulfillment rate calculation """
            fulfillment_rate = 0.0
            issued_pos = FeaturesPurchaseOrderModel.objects.filter(vendor=po_obj.vendor)
            successfully_fulfilled_count = issued_pos.filter(status="completed").exclude(quality_rating=0.0).count()
            issued_pos = issued_pos.count()
            if issued_pos > 0:
                fulfillment_rate = successfully_fulfilled_count / issued_pos

            if FeaturesHistoricalPerformanceModel.objects.filter(vendor_id=po_obj.vendor.id).exists():
                performance_obj = FeaturesHistoricalPerformanceModel.objects.get(vendor_id=po_obj.vendor.id)
                performance_obj.on_time_delivery_rate = on_time_delivery_rate
                performance_obj.fulfillment_rate = fulfillment_rate
                performance_obj.date = datetime.datetime.now(timezone)
                performance_obj.save()
            else:
                FeaturesHistoricalPerformanceModel.objects.create(
                    vendor_id=po_obj.vendor.id,
                    date=datetime.datetime.now(timezone),
                    average_response_time=0.0,
                    on_time_delivery_rate=on_time_delivery_rate,
                    quality_rating_avg=0.0,
                    fulfillment_rate=fulfillment_rate
                )

            FeaturesVendorsProfileModel.objects.filter(id=po_obj.vendor.id).update(
                on_time_delivery_rate=on_time_delivery_rate,
                fulfillment_rate=fulfillment_rate,
                updated_date=datetime.datetime.now(timezone)
            )

        if "quality_rating" in validated_data and validated_data["quality_rating"] not in [None, ""]:
            completed_pos = FeaturesPurchaseOrderModel.objects.filter(vendor=po_obj.vendor, status="completed")
            total_quality_rating = 0
            completed_count = 0
            average_quality_rating = 0.0
            for completed_po in completed_pos:
                if completed_po.quality_rating is not None:
                    total_quality_rating += completed_po.quality_rating
                    completed_count += 1

            if completed_count > 0:
                average_quality_rating = total_quality_rating / completed_count
            
            if FeaturesHistoricalPerformanceModel.objects.filter(vendor_id=po_obj.vendor.id).exists():
                performance_obj = FeaturesHistoricalPerformanceModel.objects.get(vendor_id=po_obj.vendor.id)
                performance_obj.quality_rating_avg = average_quality_rating
                performance_obj.date = datetime.datetime.now(timezone)
                performance_obj.save()
            else:
                FeaturesHistoricalPerformanceModel.objects.create(
                    vendor_id=po_obj.vendor.id,
                    date=datetime.datetime.now(timezone),
                    average_response_time=0.0,
                    on_time_delivery_rate=0.0,
                    quality_rating_avg=average_quality_rating,
                    fulfillment_rate=0.0
                )
            FeaturesVendorsProfileModel.objects.filter(id=po_obj.vendor.id).update(
                quality_rating_avg=average_quality_rating,
                updated_date=datetime.datetime.now(timezone)
            )


        return validated_data

class FeaturesPurchaseOrderDeleteSerializer(serializers.Serializer):
    """
    Serializer for deleting purchase order
    """
    api_logger = logging.LoggerAdapter(logger, {"app_name": "FeaturesPurchaseOrderDeleteSerializer"})
    
    def validate(self, data):
        """ validations for deleting purchase order """
        po_id = self.context["po_id"]
        if not FeaturesPurchaseOrderModel.objects.filter(id=po_id).exists():
            raise serializers.ValidationError("Purchase Order doesnot exists!")

        return data
    
    def create(self, validated_data):
        """ deleting purchase order """
        po_id = self.context["po_id"]
        FeaturesPurchaseOrderModel.objects.get(id=po_id).delete()

        return validated_data

class FeaturesVendorAcknowledgementSerializer(serializers.Serializer):
    """
    Serializer for vendor acknowledgement
    """

    def validate(self, data):
        """ validating po id existence """
        po_id = self.context["po_id"]
        if not FeaturesPurchaseOrderModel.objects.filter(id=po_id).exists():
            raise serializers.ValidationError("Purchase Order not exists!")
        return data

    def create(self, validated_data):
        """ creating vendor acknowledgement """
        po_id = self.context["po_id"]
        po_obj = FeaturesPurchaseOrderModel.objects.get(id=po_id)

        po_obj.acknowledgment_date = datetime.datetime.now(timezone)
        po_obj.updated_date = datetime.datetime.now(timezone)
        po_obj.save()

        response_times = []

        valid_purchase_orders = FeaturesPurchaseOrderModel.objects.filter(vendor_id=po_obj.vendor.id).values()
        for po in valid_purchase_orders:
            if po["acknowledgment_date"]:
                response_time = po["acknowledgment_date"] - po["issue_date"]
                response_times.append(response_time)

        """Calculate the average response time"""
        if response_times:
            total_seconds = sum(response.total_seconds() for response in response_times)
            avg_response_time = (total_seconds / len(response_times)) / (60 * 60)
            avg_response_time = round(avg_response_time, 3)

        else:
            avg_response_time = 0.0
        if FeaturesHistoricalPerformanceModel.objects.filter(vendor_id=po_obj.vendor.id).exists():
            performance_obj = FeaturesHistoricalPerformanceModel.objects.get(vendor_id=po_obj.vendor.id)
            performance_obj.average_response_time = avg_response_time  # in hours
            performance_obj.date = datetime.datetime.now(timezone)
            performance_obj.save()
        else:
            FeaturesHistoricalPerformanceModel.objects.create(
                vendor_id=po_obj.vendor.id,
                date=datetime.datetime.now(timezone),
                average_response_time=avg_response_time,
                on_time_delivery_rate=0.0,
                quality_rating_avg=0.0,
                fulfillment_rate=0.0
            )
        
        FeaturesVendorsProfileModel.objects.filter(id=po_obj.vendor.id).update(
            average_response_time=avg_response_time,
            updated_date=datetime.datetime.now(timezone)
        )
        
        return validated_data

class FeaturesHistoricalPerformanceSerializer(serializers.Serializer):
    """
    Serializer for getting vendor performance metrics
    """
    data = serializers.JSONField(required=False)

    def validate(self, data):
        """ validating vendor existence """
        vendor_id = self.context["vendor_id"]
        if not FeaturesHistoricalPerformanceModel.objects.filter(vendor_id=vendor_id).exists():
            raise serializers.ValidationError("Vendor performance details not exists!")
        return data

    def create(self, validated_data):
        """ creating vendor performance metrics """
        vendor_id = self.context["vendor_id"]
        performance_obj = FeaturesHistoricalPerformanceModel.objects.get(vendor_id=vendor_id)

        obj = {
            "id": performance_obj.id,
            "vendor_id" : vendor_id,
            "vendor_name" : performance_obj.vendor.name,
            "vendor_contact" : performance_obj.vendor.contact_details,
            "date" : performance_obj.date,
            "on_time_delivery_rate" : performance_obj.on_time_delivery_rate,
            "quality_rating_avg" : performance_obj.quality_rating_avg,
            "average_response_time" : performance_obj.average_response_time,
            "fulfillment_rate" : performance_obj.fulfillment_rate
        }
        validated_data["data"] = {"performance_details" : obj}
        return validated_data
