#!/usr/bin/env python
import datetime
from debug_utils import *
from sqlalchemy import func, distinct, select, and_, or_

from database import db_session
from models import *
import config


try:
    try:
        from IPython import embed
        embed()
    except:
        # Older version?
        from IPython.Shell import IPShell
        shell = IPShell(argv=[], user_ns=locals())
        shell.mainloop()
except ImportError:
    print "Install ipython"
