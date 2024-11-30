from django.contrib.auth.models import User
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rent_api.models import RentUnit, Review, Lease
from rent_api.serializers import RentUnitListSerializer, LeaseSerializer, ReviewListSerializer, \
    LeaseListSerializer, UserRealEstateSerializer, UserLandlordInfoSerializer


class MyPropertyView(ListAPIView):
    serializer_class = RentUnitListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return RentUnit.objects.filter(owner=self.request.user)


class MyReviewView(ListAPIView):
    serializer_class = ReviewListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(lease__rent_unit__owner=self.request.user)


class MyBookingsView(ListAPIView):
    serializer_class = LeaseListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Lease.objects.filter(lease__rent_unit__owner=self.request.user, confirmed=False)


class MyArchiveView(ListAPIView):
    serializer_class = LeaseListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Lease.objects.filter(lease__rent_unit__owner=self.request.user, confirmed=True)


class MyBookingsUpdateView(RetrieveUpdateAPIView):
    serializer_class = LeaseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Lease.objects.filter(lease__rent_unit__owner=self.request.user, confirmed=False)


class LandlordPropertyView(ListAPIView):
    serializer_class = UserRealEstateSerializer
    queryset = User.objects.prefetch_related('rentunit_set')


class LandlordDetailedView(RetrieveAPIView):
    serializer_class = UserLandlordInfoSerializer
    queryset = User.objects.prefetch_related('rentunit_set')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        response_data = serializer.data

        reviews = ReviewListSerializer(data=Review.objects.filter(lease__rent_unit__owner_id=instance.id), many=True)
        reviews.is_valid()
        response_data['reviews'] = reviews.data
        return Response(response_data)
