#!/usr/bin/env python
# coding: utf8
"""Flask app views.

"""

from gevent import monkey
monkey.patch_all()

import re
import os
import sys

# Fix needed for flask to allow import models
sys.path.insert(0, os.path.dirname(os.path.split(__file__)[0]))

from werkzeug.contrib.fixers import ProxyFix
import flask
from flask.ext.cache import Cache
from flask_limiter import Limiter

import config
from database import db_session
from models import utcnow


# Flask app
class BetterFlask(flask.Flask):
    def log_exception(self, exc_info):
        message = """
Time:           {time}
Request:        {request}
Request JSON:   {json}
Request FORM:   {form}
Request ARGS:   {args}
Request FILES:  {files}
Session:        {session}
IP:             {ip}
Agent:          {agent_platform} | {agent_browser} {agent_browser_version}
Raw Agent:      {agent}
            """.format(time=utcnow(),
                       request=flask.request,
                       json=flask.request.json,
                       form=flask.request.form,
                       args=flask.request.args,
                       files=flask.request.files,
                       ip=flask.request.remote_addr,
                       agent_platform=flask.request.user_agent.platform,
                       agent_browser=flask.request.user_agent.browser,
                       agent_browser_version=flask.request.user_agent.version,
                       agent=flask.request.user_agent.string,
                       session=flask.session
                       )
        self.logger.error(message, exc_info=exc_info)

app = BetterFlask(__name__,
                  template_folder=config.TEMPLATE_FOLDER,
                  static_folder=config.STATIC_FOLDER,
                  static_url_path=config.STATIC_URL_PATH)
app.config.update(
    CACHE_TYPE='filesystem',
    CACHE_DEFAULT_TIMEOUT=config.CACHE_TIMEOUT,
    CACHE_KEY_PREFIX='app_',
    SECRET_KEY=config.app_secret,
    DEBUG=config.environment == 'development',
    CACHE_DIR='/tmp/gaa/app_cache/',
    SENTRY_DSN=config.configuration['sentry_dsn'],
)

# The name and port number of the server. Required for subdomain support (e.g.:
# 'myapp.com:5000')
# http://flask.pocoo.org/docs/config/#builtin-configuration-values
app.config.server_name = config.virtual_host

# Rewrite a few headers in order for the application to work
# via nginx
app.wsgi_app = ProxyFix(app.wsgi_app)

cache = Cache(app)

limiter = Limiter(app)

# Cache results from these API routes
APPLY_CACHE_CONTROL_TO_ROUTES = (
    # Match: /api/v1/country/37
    # Match: /api/v1/country/373
    # Match: /api/v1/country/3711/
    # /api/v1/country/37?
    # Match: /api/v1/country/37?q=asdf
    # /api/v1/country
    # /api/v1/country/1/2/
    # /api/v1/city/37
    re.compile(r'^\/api\/v1\/country\/?(\d*)(\/?)(\??q=\S*)?$'),
    re.compile(r'^\/api\/v1\/city\/?(\d*)(\/?)(\??q=\S*)?$'),
    # Note: Disabled for now
    #re.compile(r'^\/api\/v1\/taxi_type\/?(\d*)(\/?)(\??q=\S*)?$'),
    # /api/v1/country/37?q=asdf
    # /api/v1/country/cities/37?q=asdf
    # Match: /api/v1/country/1/cities/37?q=asdf
    # Match: /api/v1/country/1/cities/
    # Match: /api/v1/country/1/cities/1
    re.compile(r'^\/api\/v1\/country\/(\d*)\/cities\/?(\d*)(\/?)(\??q=\S*)?$'),
)


@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()


@app.after_request
def after(response):
    # Allow cross domain
    response.headers.add('Access-Control-Allow-Origin', '{}'.format(
        flask.request.headers.get('Origin') or
        flask.request.headers.get('Host') or
        "*"))
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Methods',
                         'POST, GET, PUT, PATCH, DELETE, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type, X-Requested-With')
    response.headers.add('Access-Control-Max-Age', '1728000')

    # Set cache-control from some GET API requests
    # which only need READ access
    if flask.request.method == 'GET':
        for r in APPLY_CACHE_CONTROL_TO_ROUTES:
            if r.match(flask.request.path):
                # Cache 10 minutes
                response.headers.add('Cache-Control', 'public, max-age=600')
                break
    return response


from views import (
    apiv1
)


apiv1.configure_views(app, limiter)


if __name__ == '__main__':
    import argparse
    import werkzeug
    import werkzeug.serving
    PORT = 8080
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-p', type=int, default=PORT)
    args = parser.parse_args()
    @werkzeug.serving.run_with_reloader
    def run_server():
        from gevent.wsgi import WSGIServer
        # Note: See SERVER_NAME above, http://flask.pocoo.org/docs/config/
        app.server_name = None
        http_server = WSGIServer(('', args.port), app)
        http_server.serve_forever()
    run_server()
