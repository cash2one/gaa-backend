import re
import os

from flask import Response, jsonify
from flask.ext.restless import APIManager
from flask.ext.restless.helpers import to_dict
from postprocessors import json_serializer

import config
from helpers import CreateAPIWrapper
from database import db_session
from models import LayerFeature
from geo_utils import (
    polygon_center,
    calc_distance,
    wkb_string_to_geo_array
)


def configure_views(app, limiter):
    apimanager = APIManager(app, session=db_session)

    @app.route('/api/v1/layer_feature/x/<x>/y/<y>/r/<r>/m/<int:m>', methods=['GET'])
    def filter_locations_around_geo_point(x, y, r, m):
        x = float(x)
        y = float(y)
        r = float(r)
        geo_point = "POINT({} {})".format(x, y)
        if m > 10000:
            return jsonify(error="Max results can't be greater than 1000")
        results = []
        for lf in LayerFeature.find_within(geo_point, r).limit(m).all():
            res = to_dict(lf)
            res.pop('_set_geom_polygon')
            res.pop('_set_multi_geom_polygon')
            results.append(res)
        return jsonify(num_results=len(results), objects=json_serializer(results))

    @app.errorhandler(404)
    def page_not_found(e):
        # Just return 200 for any page since angular handles this actually
        return open(os.path.join(config.TEMPLATE_FOLDER,
                                 'index.html')).read(), 200

    v1api = CreateAPIWrapper(apimanager, 1)
    v1api.resource(LayerFeature,
                   exclude_columns_in_get=['_set_geom_polygon',
                                           '_set_multi_geom_polygon'],
                   results_per_page=10000
                   )

    # API documentation
    RE_API_DOCS_BASE_PATH = re.compile(r'"basePath": "(.*)\/api\/')
    API_URL = '"basePath": "http://www.gaa.com/api/'


    @app.route('/api/v1/api-docs', methods=['GET'])
    def api_docs_index():
        return Response(RE_API_DOCS_BASE_PATH.sub(API_URL,
                        open(config.relative_filepath(
                            './docs/api/v1/index.json')).read()),
                        mimetype='application/json')


    @app.route('/api/v1/api-docs/<resource>', methods=['GET'])
    def api_docs(resource):
        return Response(RE_API_DOCS_BASE_PATH.sub(API_URL,
                        open(config.relative_filepath(
                            './docs/api/v1/{}.json'.format(resource))).read()),
                        mimetype='application/json')
