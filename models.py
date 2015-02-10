"""Database models.

"""

import datetime
from dateutil.tz import tzutc

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm.attributes import InstrumentedAttribute

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Integer,
    ForeignKey,
    Boolean,
    UniqueConstraint,
    String,
    Time,
    Float,
    Table,
    select,
    func,
    event,
    case,
    or_,
    and_
)

from sqlalchemy.orm import (
    relationship,
    backref,
    scoped_session,
    sessionmaker,
    column_property,
)

from geoalchemy2 import (
    WKBElement,
    shape,
    Geometry,
    WKTElement
)

from database import Base, db_session

from geo_utils import polygon_center


utcnow = lambda: datetime.datetime.utcnow().replace(tzinfo=tzutc())


class LayerFeature(Base):
    __tablename__ = 'layer_feature'

    id = Column(Integer, primary_key=True)

    geom = Column(Geometry('POLYGON'))
    multi_geom = Column(Geometry('MULTIPOLYGON'))

    # Helper hybrid property allowing us to easily set polygon
    @hybrid_property
    def geom_polygon(self):
        if type(self.geom) in [WKBElement, WKTElement]:
            wkbstring = str(shape.to_shape(self.geom))
            return wkbstring
        else:
            return None

    @geom_polygon.setter
    def _set_geom_polygon(self, polygon):
        if not type(self.geom) == InstrumentedAttribute:
            self.geom = WKTElement(polygon)

    @hybrid_property
    def geom_center(self):
        if type(self.geom) in [WKBElement, WKTElement]:
            return polygon_center(self.geom)
        else:
            return None

    @hybrid_property
    def multi_geom_polygon(self):
        if type(self.multi_geom) in [WKBElement, WKTElement]:
            wkbstring = str(shape.to_shape(self.multi_geom))
            return wkbstring
        else:
            return None

    @multi_geom_polygon.setter
    def _set_multi_geom_polygon(self, polygon):
        if not type(self.multi_geom) == InstrumentedAttribute:
            self.multi_geom = WKTElement(polygon)

    @hybrid_property
    def multi_geom_center(self):
        if type(self.multi_geom) in [WKBElement, WKTElement]:
            return polygon_center(self.multi_geom)
        else:
            return None

    CC_1 = Column(String(200))
    CC_2 = Column(String(200))
    ENGTYPE4 = Column(String(200))
    ENGTYPE_1 = Column(String(200))
    ENGTYPE_2 = Column(String(200))
    ENGTYPE_3 = Column(String(200))
    ENGTYPE_4 = Column(String(200))
    ENGTYPE_5 = Column(String(200))
    HASC_1 = Column(String(50))
    HASC_2 = Column(String(50))
    HASC_3 = Column(String(50))
    ID_0 = Column(String(200))
    ID_1 = Column(String(200))
    ID_2 = Column(String(200))
    ID_3 = Column(String(200))
    ID_4 = Column(String(200))
    ID_5 = Column(String(200))
    ISO = Column(String(200))
    NAME_0 = Column(String(200))
    NAME_1 = Column(String(200))
    NAME_2 = Column(String(200))
    NAME_3 = Column(String(200))
    NAME_4 = Column(String(200))
    NAME_5 = Column(String(200))
    NL_NAME_1 = Column(String(200))
    NL_NAME_2 = Column(String(200))
    NL_NAME_3 = Column(String(200))
    OBJECTID = Column(String(200))
    REMARKS_1 = Column(String(200))
    REMARKS_2 = Column(String(200))
    REMARKS_3 = Column(String(200))
    REMARKS_4 = Column(String(200))
    Shape_Area = Column(String(200))
    Shape_Leng = Column(String(200))
    TYPE4 = Column(String(200))
    TYPE_1 = Column(String(200))
    TYPE_2 = Column(String(200))
    TYPE_3 = Column(String(200))
    TYPE_4 = Column(String(200))
    TYPE_5 = Column(String(200))
    VALIDFR_1 = Column(String(200))
    VALIDFR_2 = Column(String(200))
    VALIDFR_3 = Column(String(200))
    VALIDFR_4 = Column(String(200))
    VALIDTO_1 = Column(String(200))
    VALIDTO_2 = Column(String(200))
    VALIDTO_3 = Column(String(200))
    VALIDTO_4 = Column(String(200))
    VARNAME_1 = Column(String(200))
    VARNAME_2 = Column(String(200))
    VARNAME_3 = Column(String(200))
    VARNAME_4 = Column(String(200))

    @classmethod
    def find_nearby(cls, geom):
        "Returns a locations closest to a geo point"
        return db_session.query(cls).\
            order_by(func.ST_Distance(cls.geom, geom),
                     func.ST_Distance(cls.multi_geom, geom))

    @classmethod
    def find_within(cls, geom, radius_meters):
        "Returns a list of locations with m meters radius of a geo point"
        # http://stackoverflow.com/questions/5217348/how-do-i-convert-kilometres-to-degrees-in-geodjango-geos
        approx_degrees = ((float(radius_meters)/1000) / 40000) * 360
        return db_session.query(cls).filter(
            func.ST_DWithin(cls.geom, geom, approx_degrees)).\
            order_by(func.ST_Distance(cls.geom, geom),
                     func.ST_Distance(cls.multi_geom, geom))


class DBVersion(Base):
    """Store db version for manual migrations.

    Problem is schema is currently reliant on
    `Base.metadata.create_all(config.db_engine)`, which create the full schema
    regardless of migrations.

    Will likely start fresh and create a migration that represents the whole
    database and disable auto-creation of schema.

    This is a temporary measure to ensure that each database is up to date.
    """
    __tablename__ = 'db_version'
    version = Column(Integer, primary_key=True)
