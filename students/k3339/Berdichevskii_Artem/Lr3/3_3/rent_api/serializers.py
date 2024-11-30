from django.contrib.auth.models import User
from rest_framework import serializers

from .models import RentUnit, Lease, Review


class TruncatedTextField(serializers.CharField):
    def to_representation(self, value):
        value = super().to_representation(value)
        return value[:97] + '...' if value else value


class RentUnitListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentUnit
        fields = [
            'id',
            'cost',
            'per_period',
            'address',
            'area_sq_m'
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class RentUnitSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = RentUnit
        fields = '__all__'
        depth = 1


class LeaseListSerializer(serializers.ModelSerializer):
    rent_unit = RentUnitListSerializer(read_only=True)
    confirmed = serializers.BooleanField(default=False, required=False)

    class Meta:
        model = Lease
        fields = [
            'id',
            'rent_unit',
            'dt_start',
            'dt_end',
            'confirmed']
        depth = 1


class LeaseSerializer(serializers.ModelSerializer):
    rent_unit = RentUnitListSerializer(read_only=True, required=False)
    tenant = UserSerializer(read_only=True, required=False)
    confirmed = serializers.BooleanField(default=False, required=False)

    class Meta:
        model = Lease
        fields = '__all__'
        depth = 1


class ReviewListSerializer(serializers.ModelSerializer):
    description = TruncatedTextField(read_only=True)

    class Meta:
        model = Review
        fields = ['dt_published', 'rating', 'description']


class ReviewSerializer(serializers.ModelSerializer):
    lease = LeaseSerializer(read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        depth = 1




class UserRealEstateSerializer(serializers.ModelSerializer):
    rent_units = RentUnitListSerializer(read_only=True, required=False, many=True, source='rentunit_set')

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'rent_units'
        ]


class UserLandlordInfoSerializer(serializers.ModelSerializer):
    rent_units = RentUnitListSerializer(read_only=True, required=False, many=True, source='rentunit_set')

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'rent_units',
        ]
