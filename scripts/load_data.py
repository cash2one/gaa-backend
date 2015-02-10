import os
import json
#os.environ['ECHO'] = '1'

import osgeo.ogr

from models import *
from database import db_session

import config

from debug import *

from pprint import pprint


def main():
    db_session.query(LayerFeature).delete()
    db_session.commit()

    shape_data = osgeo.ogr.Open(config.relative_filepath('./resources/gadm_v2_shp/gadm2.shp'))
    layer = shape_data.GetLayer()

    for index in xrange(layer.GetFeatureCount()):
        feature = layer.GetFeature(index)
        geometry = feature.GetGeometryRef()
        try:
            lf = LayerFeature(**feature.items())
        except Exception, e:
            print e
            pprint(feature.items())
        geo = geometry.ExportToWkt()
        if "MULTI" in geo:
            lf.multi_geom_polygon = geo
        else:
            lf.geom_polygon = geo
        db_session.add(lf)
        print 'Loading: {} {} {} {} {} {}'.format(lf.ENGTYPE_4,
                                                  lf.NAME_0,
                                                  lf.NAME_1,
                                                  lf.NAME_2,
                                                  lf.NAME_3,
                                                  lf.NAME_4,
                                                  lf.NAME_5)
        try:
            db_session.commit()
        except Exception, e:
            print e
            pprint(geometry)
            import ipdb; ipdb.set_trace()

    print "DONE!"


if __name__ == '__main__':
    main()
