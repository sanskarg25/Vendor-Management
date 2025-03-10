import logging
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from vendor_management.settings import logger
from features.serializers import (
    FeaturesVendorCreationSerializer,
    FeaturesVendorListSerializer,
    FeaturesVendorGetDetailsSerializer,
    FeaturesVendorUpdateSerializer,
    FeaturesVendorDeleteSerializer,
    FeaturesPurchaseOrderCreationSerializer,
    FeaturesPurchaseOrderListSerializer,
    FeaturesPurchaseOrderGetDetailsSerializer,
    FeaturesPurchaseOrderUpdateSerializer,
    FeaturesPurchaseOrderDeleteSerializer,
    FeaturesVendorAcknowledgementSerializer,
    FeaturesHistoricalPerformanceSerializer,
)

class FeaturesVendorsAPI(APIView):
    """
    APIView to perform POST,GET operations for all vendors
    """
    api_logger = logging.LoggerAdapter(logger,{"app_name":"FeaturesVendorsAPI"})

    def post(self,request):
        """
        Creating vendors
        """
        try:
            serializer = FeaturesVendorCreationSerializer(
                data=request.data,
                context={"request": request},
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Vendor Created Successfully"},
                    status=status.HTTP_200_OK,
                )
            else:
                for key in serializer.errors.keys():
                    error = serializer.errors[key]
                    if type(error) == type([]):
                        error = error[0]
                    else:
                        error = serializer.errors
                return Response(
                    {"message": error, "data": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            self.api_logger.info(f"Exception creating vendor, {str(e)}")
            return Response(
                {"message": "Something went wrong", "data": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
    
    def get(self,request):
        """
        List of all vendors
        """
        try:
            serializer = FeaturesVendorListSerializer(
                data=request.GET.dict(),
                context={"request": request},
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data["data"],
                    status=status.HTTP_200_OK,
                )
            else:
                for key in serializer.errors.keys():
                    error = serializer.errors[key]
                    if type(error) == type([]):
                        error = error[0]
                    else:
                        error = serializer.errors
                return Response(
                    {"message": error, "data": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            self.api_logger.info(f"Exception getting vendors, {str(e)}")
            return Response(
                {"message": "Something went wrong", "data": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
class FeaturesVendorByIDAPI(APIView):
    """
    APIView to perform GET,PUT,DELETE operations for vendor by ID
    """
    api_logger = logging.LoggerAdapter(logger,{"app_name":"FeaturesVendorAPI"})


    def get(self,request,vendor_id=None):
        """
        List of all vendors
        """
        try:
            vendor_id = self.kwargs.get('vendor_id')
            serializer = FeaturesVendorGetDetailsSerializer(
                data=request.GET.dict(),
                context={"request": request,"vendor_id":vendor_id},
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data["details"],
                    status=status.HTTP_200_OK,
                )
            else:
                for key in serializer.errors.keys():
                    error = serializer.errors[key]
                    if type(error) == type([]):
                        error = error[0]
                    else:
                        error = serializer.errors
                return Response(
                    {"message": error, "data": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            self.api_logger.info(f"Exception getting vendor details, {str(e)}")
            return Response(
                {"message": "Something went wrong", "data": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
    
    def put(self,request,vendor_id=None):
        """
        Updating vendor
        """
        try:
            vendor_id = self.kwargs.get("vendor_id")
            serializer = FeaturesVendorUpdateSerializer(
                data=request.data,
                context={"request": request,"vendor_id":vendor_id},
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Vendor Updated Successfully"},
                    status=status.HTTP_200_OK,
                )
            else:
                for key in serializer.errors.keys():
                    error = serializer.errors[key]
                    if type(error) == type([]):
                        error = error[0]
                    else:
                        error = serializer.errors
                return Response(
                    {"message": error, "data": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            self.api_logger.info(f"Exception updating vendor, {str(e)}")
            return Response(
                {"message": "Something went wrong", "data": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self,request,vendor_id=None):
        """
        Deleting vendor
        """
        try:
            vendor_id = self.kwargs.get("vendor_id")
            serializer = FeaturesVendorDeleteSerializer(
                data=request.data,
                context={"request": request,"vendor_id":vendor_id},
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Vendor Deleted Successfully"},
                    status=status.HTTP_200_OK,
                )
            else:
                for key in serializer.errors.keys():
                    error = serializer.errors[key]
                    if type(error) == type([]):
                        error = error[0]
                    else:
                        error = serializer.errors
                return Response(
                    {"message": error, "data": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            self.api_logger.info(f"Exception deleting vendor, {str(e)}")
            return Response(
                {"message": "Something went wrong", "data": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

class FeaturesPurchaseOrderAPI(APIView):
    """
    APIView to perform POST,GET operations for all purchase order
    """
    api_logger = logging.LoggerAdapter(logger,{"app_name":"FeaturesPurchaseOrderAPI"})

    def post(self,request):
        """
        Creating purchase order
        """
        try:
            serializer = FeaturesPurchaseOrderCreationSerializer(
                data=request.data,
                context={"request": request},
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Purchase Order Created Successfully"},
                    status=status.HTTP_200_OK,
                )
            else:
                for key in serializer.errors.keys():
                    error = serializer.errors[key]
                    if type(error) == type([]):
                        error = error[0]
                    else:
                        error = serializer.errors
                return Response(
                    {"message": error, "data": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            self.api_logger.info(f"Exception creating purchase order, {str(e)}")
            return Response(
                {"message": "Something went wrong", "data": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
    
    def get(self,request):
        """
        List of all purchase orders
        """
        try:
            serializer = FeaturesPurchaseOrderListSerializer(
                data=request.GET.dict(),
                context={"request": request},
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data["data"],
                    status=status.HTTP_200_OK,
                )
            else:
                for key in serializer.errors.keys():
                    error = serializer.errors[key]
                    if type(error) == type([]):
                        error = error[0]
                    else:
                        error = serializer.errors
                return Response(
                    {"message": error, "data": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            self.api_logger.info(f"Exception getting purchase orders, {str(e)}")
            return Response(
                {"message": "Something went wrong", "data": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
class FeaturesPurchaseOrderByIDAPI(APIView):
    """
    APIView to perform GET,PUT,DELETE operations for purchase order by ID
    """
    api_logger = logging.LoggerAdapter(logger,{"app_name":"FeaturesPurchaseOrderByIDAPI"})


    def get(self,request,po_id=None):
        """
        List of purchase order by ID
        """
        try:
            po_id = self.kwargs.get("po_id")
            serializer = FeaturesPurchaseOrderGetDetailsSerializer(
                data=request.GET.dict(),
                context={"request": request,"po_id":po_id},
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data["details"],
                    status=status.HTTP_200_OK,
                )
            else:
                for key in serializer.errors.keys():
                    error = serializer.errors[key]
                    if type(error) == type([]):
                        error = error[0]
                    else:
                        error = serializer.errors
                return Response(
                    {"message": error, "data": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            self.api_logger.info(f"Exception getting purchase order details, {str(e)}")
            return Response(
                {"message": "Something went wrong", "data": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
    
    def put(self,request,po_id=None):
        """
        Updating purchase orders
        """
        try:
            po_id = self.kwargs.get("po_id")
            serializer = FeaturesPurchaseOrderUpdateSerializer(
                data=request.data,
                context={"request": request,"po_id":po_id},
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Purchase Order Updated Successfully"},
                    status=status.HTTP_200_OK,
                )
            else:
                for key in serializer.errors.keys():
                    error = serializer.errors[key]
                    if type(error) == type([]):
                        error = error[0]
                    else:
                        error = serializer.errors
                return Response(
                    {"message": error, "data": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            self.api_logger.info(f"Exception updating purchase order, {str(e)}")
            return Response(
                {"message": "Something went wrong", "data": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self,request,po_id=None):
        """
        Deleting purchase order
        """
        try:
            po_id = self.kwargs.get("po_id")
            serializer = FeaturesPurchaseOrderDeleteSerializer(
                data=request.data,
                context={"request": request,"po_id":po_id},
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Purchase Order Deleted Successfully"},
                    status=status.HTTP_200_OK,
                )
            else:
                for key in serializer.errors.keys():
                    error = serializer.errors[key]
                    if type(error) == type([]):
                        error = error[0]
                    else:
                        error = serializer.errors
                return Response(
                    {"message": error, "data": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            self.api_logger.info(f"Exception deleting purchase order, {str(e)}")
            return Response(
                {"message": "Something went wrong", "data": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

class FeaturesPOAcknowledgementAPI(APIView):
    """
    APIView to acknowledge purchase orders
    """
    api_logger = logging.LoggerAdapter(logger,{"app_name":"FeaturesPOAcknowledgementAPI"})


    def post(self,request,po_id=None):
        """
        Acknowledgement of purchase orders by id
        """
        try:
            po_id = self.kwargs.get("po_id")
            serializer = FeaturesVendorAcknowledgementSerializer(
                data=request.data,
                context={"request": request,"po_id":po_id},
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message" : "Purchase order acknowledged successfully"},
                    status=status.HTTP_200_OK,
                )
            else:
                for key in serializer.errors.keys():
                    error = serializer.errors[key]
                    if type(error) == type([]):
                        error = error[0]
                    else:
                        error = serializer.errors
                return Response(
                    {"message": error, "data": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            self.api_logger.info(f"Exception acknowledging purchase order, {str(e)}")
            return Response(
                {"message": "Something went wrong", "data": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

class FeaturesHistoricalPerformanceAPI(APIView):
    """
    APIView to getting performance metrics of vendors
    """
    api_logger = logging.LoggerAdapter(logger,{"app_name":"FeaturesHistoricalPerformanceAPI"})


    def get(self,request,vendor_id=None):
        """
        Performance metrics of vendor by id
        """
        try:
            vendor_id = self.kwargs.get("vendor_id")
            serializer = FeaturesHistoricalPerformanceSerializer(
                data=request.GET.dict(),
                context={"request": request,"vendor_id":vendor_id},
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data["data"],
                    status=status.HTTP_200_OK,
                )
            else:
                for key in serializer.errors.keys():
                    error = serializer.errors[key]
                    if type(error) == type([]):
                        error = error[0]
                    else:
                        error = serializer.errors
                return Response(
                    {"message": error, "data": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            self.api_logger.info(f"Exception getting historical performance metrics, {str(e)}")
            return Response(
                {"message": "Something went wrong", "data": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )