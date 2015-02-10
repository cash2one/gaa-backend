"""Basic debug utilities.

"""

import time
import datetime
import json
import collections

try:
    import sqlparse
except:
    pass

from sqlalchemy.sql import compiler
from psycopg2.extensions import adapt as sqlescape


def compile_query(query):
    """Compiles sqlalchemy query, can be used for debugging.

    Use inconjunction with pretty_print_query for best results.

    Modified from
    http://stackoverflow.com/questions/4617291/how-do-i-get-a-raw-compiled-sql-query-from-a-sqlalchemy-expression
    """
    dialect = query.session.bind.dialect
    statement = query.statement
    comp = compiler.SQLCompiler(dialect, statement)
    comp.compile()
    enc = dialect.encoding
    params = {}
    for k, v in comp.params.iteritems():
        if isinstance(v, unicode):
            v = v.encode(enc)
        params[k] = sqlescape(v).getquoted()
    sql = comp.string.encode(enc).replace('%s', '{}')
    return sql.format(*params.values()).decode(enc)


class functime(object):
    def __init__(self, log):
        self.log = log

    def __call__(self, f):
        def wrapped_f(*args, **kwds):
            start = time.time()
            value = f(*args, **kwds)
            end = time.time()
            self.log.debug('%s TOOK %s ms' % (f.__name__, end-start))
            return value
        return wrapped_f


def pptree(d):
    """Converts default dict to dict.

    defaultdict collections don't pretty print properly.

    Use this function to convert default dict to dict to ease debugging using
    the pretty print function.
    """
    t = type(d)
    if t == collections.defaultdict:
        return {k: pptree(v) for k, v in d.iteritems()}
    elif t == dict:
        return {k: v for k, v in d.iteritems()}
    else:
        return d


def pretty_print_query(q):
    """Pretty print query as sql

    E.g.
    >>> pretty_print_query(session.query(Article))
    SELECT article.bibo_doi AS article_bibo_doi,
        article."bibo_pageStart" AS "article_bibo_pageStart",
        ...
        article.section_label AS article_section_label
    FROM article

    """
    if sqlparse:
        print sqlparse.format(str(q), reindent=True, keyword_case='upper')
    else:
        print 'install sqlparse'


def to_json(insts):
    """Jsonify the sql alchemy query result.
    Modified from http://stackoverflow.com/questions/7102754/jsonify-a-sqlalchemy-result-set-in-flask

    >>> from models import db_session, Country
    >>> import json
    >>> from debug_utils import to_json
    >>> json.loads(to_json(db_session.query(Country).first()))
    [{u'id': 1,
    u'code': u'KE',
    u'name': u'Kenya',
    }]
    """
    def fix_datetime(d):
        return str(d)

    # Convert to list
    try:
        insts = list(insts)
    except:
        insts = [insts]

    recs = []
    for inst in insts:
        cls = inst.__class__
        convert = {
            datetime.datetime: fix_datetime
        }
        # add your coversions for things like datetime's
        # and what-not that aren't serializable.
        rec = dict()
        for col in cls.__table__.columns:
            val = getattr(inst, col.name)
            python_type = col.type.python_type
            if python_type in convert.keys() and val is not None:
                try:
                    rec[col.name] = convert[python_type](val)
                except:
                    rec[col.name] = "Error:  Failed to covert using ", str(convert[python_type])
            elif val is None:
                pass
            else:
                rec[col.name] = val
        recs.append(rec)
    return json.dumps(recs, sort_keys=True, indent=4)

