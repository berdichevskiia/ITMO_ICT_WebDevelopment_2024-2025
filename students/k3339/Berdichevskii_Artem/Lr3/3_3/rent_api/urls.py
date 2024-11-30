from django.contrib import admin
from django.urls import path, include

from .views.landlords import MyPropertyView, MyReviewView, MyBookingsView, MyBookingsUpdateView, MyArchiveView, \
    LandlordPropertyView, LandlordDetailedView
from .views.views import IndexForApi
from .views.properies import PropertyListView, PropertyDetailedView, PropertyFreeDatesView, \
    CreateLeaseSuggestionsView
from .views.tenant import TenantRentsListView, TenantRentsDetailView, TenantLeaseReviewCRUDView

urlpatterns = [
    path('', IndexForApi.as_view(), name='index'),

    path('properties/', PropertyListView.as_view(), name='property-list'),
    path('properties/<int:pk>/', PropertyDetailedView.as_view(), name='property-details'),
    path('properties/<int:pk>/free_dates/', PropertyFreeDatesView.as_view(), name='property-free-dates'),
    path('properties/<int:pk>/book/', CreateLeaseSuggestionsView.as_view(), name='book-property'),

    path('tenant/', TenantRentsListView.as_view(), name='tenant-lease-list'),
    path('tenant/<int:pk>/', TenantRentsDetailView.as_view(), name='tenant-lease-details'),
    path('tenant/<int:pk>/review/', TenantLeaseReviewCRUDView.as_view(), name='review-tenant-lease-crud'),


    path('landlord/me/', MyPropertyView.as_view(), name='my-property'),
    path('landlord/me/reviews/', MyReviewView.as_view(), name='my-reviews'),
    path('landlord/me/bookings/', MyBookingsView.as_view(), name='my-bookings'),
    path('landlord/me/bookings/<int:pk>/', MyBookingsUpdateView.as_view(), name='my-bookings-update'),
    path('landlord/me/archive/', MyArchiveView.as_view(), name='my-archive'),

    path('landlord/', LandlordPropertyView.as_view(), name='landlord-property'),
    path('landlord/<int:pk>/', LandlordDetailedView.as_view(), name='landlord-details'),

    path("admin/", admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
