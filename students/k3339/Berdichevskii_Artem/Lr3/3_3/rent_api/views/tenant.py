from rest_framework import mixins
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListAPIView, \
    RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from rent_api.models import Lease, Review
from rent_api.serializers import LeaseSerializer, LeaseListSerializer, \
    ReviewSerializer


class TenantRentsListView(ListAPIView):
    serializer_class = LeaseListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.GET.get('confirmed', None):
            return Lease.objects.filter(tenant=self.request.user, confirmed=True).order_by('dt_start')
        if self.request.GET.get('pending', None):
            return Lease.objects.filter(tenant=self.request.user, confirmed=False).order_by('dt_start')
        return Lease.objects.filter(tenant=self.request.user).order_by('dt_start')


class TenantRentsDetailView(RetrieveAPIView):
    serializer_class = LeaseSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        return Lease.objects.filter(tenant=self.request.user)


class TenantLeaseReviewCRUDView(mixins.CreateModelMixin, RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        lease_id = self.kwargs['pk']
        return Review.objects.filter(author=self.request.user, lease_id=lease_id)

    def get_object(self):
        try:
            return self.get_queryset().get()
        except Review.DoesNotExist:
            raise NotFound("No Review matches the given query.")

    def perform_create(self, serializer):
        lease_id = self.kwargs['pk']
        try:
            lease = Lease.objects.get(pk=lease_id)
        except Lease.DoesNotExist:
            raise NotFound("Lease not found.")
        if lease.tenant != self.request.user or not lease.confirmed:
            raise PermissionDenied("You do not have permission to comment on this lease.")
        serializer.save(author=self.request.user, lease=lease)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
