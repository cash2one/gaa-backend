"""Geoalchemy geo helpers.

"""

import re

from geopy.distance import great_circle
from geoalchemy2 import shape
from sqlalchemy import func

from database import db_session


RE_DECIMALS = re.compile('(\+|-)?([0-9]+(\.[0-9]+))')


def wkb_string_to_geo_array(wkbstring):
    """Takes a wkb string and converts it to a geo array."""
    values = []
    data = RE_DECIMALS.findall(wkbstring)
    for i, (first, second)in enumerate(zip(data[0::2], data[1::2])):
        val = (''.join(first[:2]), ''.join(second[:2]))
        #if i == 1:
        #    lastvalue = val
        values.append(val)
    #values.append(val)
    return values


def polygon_center(geom):
    """Takes a series of points making up a polygon and calculates the center.

    Example:
    >> pp polygon_center(taxi.location.geom)
    u'POINT(-1.2283227844206 36.812308483854)'
    """
    center = func.ST_Centroid(geom)
    return str(shape.to_shape(db_session.scalar(center)))


def calc_distance(latlong1, latlong2):
    """Calculate the great circle distance between two points on the earth
    (specified in decimal degrees)
    """
    return great_circle(map(float, latlong1), map(float, latlong2)).kilometers
