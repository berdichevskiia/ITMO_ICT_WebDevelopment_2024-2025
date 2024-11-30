from datetime import date, timedelta

from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rent_api.models import RentUnit
from rent_api.serializers import RentUnitSerializer, RentUnitListSerializer, LeaseSerializer
from rent_api.utils import get_free_dates, parse_or_return


class PropertyListView(ListCreateAPIView):
    serializer_class = RentUnitListSerializer
    queryset = RentUnit.objects.filter(is_displayed=True)
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer(self, *args, **kwargs):
        if self.request.method == 'POST':
            return RentUnitSerializer
        return super().get_serializer(*args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PropertyDetailedView(RetrieveUpdateAPIView):
    model = RentUnit
    serializer_class = RentUnitSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = RentUnit.objects.all()

    def perform_update(self, serializer):
        obj = self.get_object()
        if obj.owner != self.request.user:
            raise PermissionDenied("You do not have permission to modify this object.")
        serializer.save()


class PropertyFreeDatesView(APIView):
    lookup_field = 'pk'

    def get(self, request, pk):
        start_date = parse_or_return(request.GET.get('start_date', date.today()))
        end_date = parse_or_return(request.GET.get('end_date', start_date + timedelta(days=30)))
        rent_unit = RentUnit.objects.get(pk=pk)

        if end_date < start_date:
            return Response({'error': 'End date must be before start date.'})

        return Response(
            get_free_dates(rent_unit, start_date, end_date)
        )


class CreateLeaseSuggestionsView(CreateAPIView):
    serializer_class = LeaseSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def perform_create(self, serializer):
        rent_unit = RentUnit.objects.get(pk=self.kwargs['pk'])
        dt_start = serializer.data['dt_start']
        dt_end = serializer.data['dt_end']

        if self.request.user == rent_unit.owner:
            raise PermissionDenied("Property owner can't lease his own property")

        available_dates = get_free_dates(rent_unit, dt_start, dt_end)
        if len(available_dates) != (dt_end - dt_start).days:
            raise PermissionDenied("Lease overlapping")

        serializer.save(tenant=self.request.user,
                        rent_unit=rent_unit)

        return Response({'success': 'Lease successfully created.'})
