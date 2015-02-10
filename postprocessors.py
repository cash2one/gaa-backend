"""Flask-Restless common postprocessors.

"""

import datetime

from geoalchemy2 import WKBElement, shape

from geo_utils import wkb_string_to_geo_array


def debug_postprocessor(result, **kw):
    import ipdb; ipdb.set_trace()
    return result


def json_serializer(result, **kw):
    """Serializes data to a JSON friendly format (Use as a global
    postprocessor).
    """
    def process(data):
        dt = type(data)
        if dt == dict:
            return {k: process(v) for k, v in data.iteritems()}
        elif dt == list:
            return [process(d) for d in data]
        elif dt == WKBElement:
            wkbstring = str(shape.to_shape(data))
            return wkb_string_to_geo_array(wkbstring)
        elif dt == datetime.time:
            return str(data)
        elif dt == datetime.date:
            return str(data)
        elif dt == datetime.datetime:
            return str(data)
        else:
            return data
    res_type = type(result)
    assert res_type in [list, dict]
    if type(result) == list:
        for i, res in enumerate(result):
            result[i].update(process(res))
    elif type(result) == dict:
        result.update(process(result))
    return result
