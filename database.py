"""Provides all methods and classes related to configuring the database and any
special types or helpers used by the database.

"""

import os

from sqlalchemy import event
from sqlalchemy import exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import Pool
import sqlalchemy

from debug import *

import config


@event.listens_for(Pool, "checkout")
def ping_connection(dbapi_connection, connection_record, connection_proxy):
    """http://docs.sqlalchemy.org/en/latest/core/pooling.html

    Disconnect Handling - Pessimistic

    At the expense of some extra SQL emitted for each connection checked out
    from the pool, a ping operation established by a checkout event handler
    can detect an invalid connection before it is used

    The Pool object specifically catches DisconnectionError and attempts to
    create a new DBAPI connection, up to three times, before giving up and then
    raising InvalidRequestError, failing the connection. This recipe will
    ensure that a new Connection will succeed even if connections in the pool
    have gone stale
    """
    cursor = dbapi_connection.cursor()
    try:
        cursor.execute("SELECT 1")
    except:
        # optional - dispose the whole pool
        # instead of invalidating one at a time
        # connection_proxy._pool.dispose()

        # raise DisconnectionError - pool will try
        # connecting again up to three times before raising.
        raise exc.DisconnectionError()
    cursor.close()


def configure_db(db_config):
    username = os.environ.get('USERNAME') or db_config.get('username')
    password = os.environ.get('PASS') or db_config.get('password')
    host = os.environ.get('CONTAINER_IP') or db_config.get('host')
    port = os.environ.get('PORT') or db_config.get('port')
    database = os.environ.get('DATABASE') or db_config.get('database')
    engine = sqlalchemy.engine.url.URL(
        db_config.get('engine'),
        username=username,
        password=password,
        host=host,
        port=port,
        database=database,
        query=db_config.get('query', {})
    )
    opts = {}
    for opt in ['encoding', 'convert_unicode', 'echo', 'pool_recycle',
                'pool_size', 'connect_args', 'paramstyle']:
        # Allow opts to be passed in command line,
        # e.g. ECHO=1 python -m scripts.csv2db... to see db queries
        # executed
        if db_config.get(opt) or opt.upper() in os.environ:
            opts[opt] = db_config.get(opt) or bool(os.environ.get(opt.upper()))

    return sqlalchemy.create_engine(engine, **opts)


engine = configure_db(config.db_config)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base(engine)
Base.query = db_session.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models
    Base.metadata.create_all(bind=engine)
    #from migrations import migrate
    #migrate.up()
