from dateutil import parser
import datetime

from .models import Lease


def get_free_dates(rent_unit, start_date, end_date):
    """
    Get a list of dates when a RentUnit is free.

    :param rent_unit: RentUnit object
    :param start_date: Start date to check availability
    :param end_date: End date to check availability
    :return: List of available dates
    """
    overlapping_leases = Lease.objects.filter(
        rent_unit=rent_unit,
        dt_start__lt=end_date,
        dt_end__gt=start_date
    )

    all_dates = set(
        start_date + datetime.timedelta(days=i)
        for i in range((end_date - start_date).days + 1)
    )

    unavailable_dates = set()
    for lease in overlapping_leases:
        lease_dates = set(
            lease.dt_start + datetime.timedelta(days=i)
            for i in range((lease.dt_end - lease.dt_start).days + 1)
        )
        unavailable_dates.update(lease_dates)

    free_dates = sorted(all_dates - unavailable_dates)

    return free_dates

def parse_or_return(dirty_date):
    if type(dirty_date) == datetime.date:
        return dirty_date
    return parser.parse(dirty_date)