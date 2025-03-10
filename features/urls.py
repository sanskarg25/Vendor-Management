from django.urls import path
from features.views import (
    FeaturesVendorsAPI,
    FeaturesVendorByIDAPI,
    FeaturesPurchaseOrderAPI,
    FeaturesPurchaseOrderByIDAPI,
    FeaturesPOAcknowledgementAPI,
    FeaturesHistoricalPerformanceAPI,
)

urlpatterns = [
    path(
        "vendors/",
        FeaturesVendorsAPI.as_view(),
        name="FeaturesVendorsAPIView"
    ),
    path(
        "vendors/<int:vendor_id>/",
        FeaturesVendorByIDAPI.as_view(),
        name="FeaturesVendorByIDAPIView"
    ),
    path(
        "purchase_orders/",
        FeaturesPurchaseOrderAPI.as_view(),
        name="FeaturesPurchaseOrderAPIView"
    ),
    path(
        "purchase_orders/<int:po_id>/",
        FeaturesPurchaseOrderByIDAPI.as_view(),
        name="FeaturesPurchaseOrderByIDAPIView"
    ),
    path(
        "purchase_orders/<int:po_id>/acknowledge",
        FeaturesPOAcknowledgementAPI.as_view(),
        name="FeaturesPOAcknowledgementAPIView"
    ),
    path(
        "vendors/<int:vendor_id>/performance",
        FeaturesHistoricalPerformanceAPI.as_view(),
        name="FeaturesHistoricalPerformanceAPIView"
    ),
]