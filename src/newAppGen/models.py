
import enum
import datetime
from datetime import timedelta, datetime, date

from sqlalchemy.orm import relationship, query, defer, deferred, column_property, mapper
from sqlalchemy.schema import FetchedValue
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy import (Column, Integer, String, ForeignKey,
    Sequence, Float, Text, BigInteger, Date,
    DateTime, Time, Boolean, Index, CheckConstraint,
    UniqueConstraint,ForeignKeyConstraint, Numeric, LargeBinary , Table, func)

# IMPORT Postgresql Specific Types
from sqlalchemy.dialects.postgresql import *
from sqlalchemy.dialects.postgresql import (
    ARRAY, BIGINT, BIT, BOOLEAN, BYTEA, CHAR, CIDR, DATE,
    DOUBLE_PRECISION, ENUM, FLOAT, HSTORE, INET, INTEGER,
    INTERVAL, JSON, JSONB, MACADDR, NUMERIC, OID, REAL, SMALLINT, TEXT,
    TIME, TIMESTAMP, UUID, VARCHAR, INT4RANGE, INT8RANGE, NUMRANGE,
    DATERANGE, TSRANGE, TSTZRANGE, TSVECTOR, aggregate_order_by )

from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin, FileColumn, ImageColumn, UserExtensionMixin
from flask_appbuilder.filemanager import ImageManager

from flask_appbuilder.models.decorators import renders
from sqlalchemy_utils import aggregated, force_auto_coercion, observes
from sqlalchemy_utils.types import TSVectorType   #Searchability look at DocMixin
from sqlalchemy.ext.associationproxy import association_proxy

from flask_appbuilder.security.sqla.models import User

# To create GraphSQL API
import graphene
# from graphene_sqlalchemy import SQLAlchemyObjectType

# Versioning Mixin
# from sqlalchemy_continuum import make_versioned
#Add __versioned__ = {}




# from sqlalchemy_searchable import make_searchable
# from flask_graphql import GraphQLView

# ActiveRecord Model Features
# from sqlalchemy_mixins import AllFeaturesMixin, ActiveRecordMixin


from .mixins import *

# Here is how to extend the User model
#class UserExtended(Model, UserExtensionMixin):
#    contact_group_id = Column(Integer, ForeignKey('contact_group.id'), nullable=True)
#    contact_group = relationship('ContactGroup')

# UTILITY CLASSES
# import arrow,


# Initialize sqlalchemy_utils
#force_auto_coercion()
# Keep versions of all data
# make_versioned()
# make_searchable()



class Industry(Model, AuditMixin): # RefTypeMixin, TransientMixin, DocMixin
     __tablename__ = "industry"
    id = Column(SERIAL, primary_key=True)
    industry_code = Column(TEXT, nullable=False)
    job_id = Column(Integer, ForeignKey(job.id))
    fk_job_id = relationship(job, backref='industry', lazy='dynamic')
    task_id = Column(Integer, ForeignKey(task.id))
    fk_task_id = relationship(task, backref='industry', lazy='dynamic')

class Job(Model, AuditMixin): # RefTypeMixin, TransientMixin, DocMixin
     __tablename__ = "job"
    id = Column(SERIAL, primary_key=True)
    name = Column(varchar(30))
    company_profile = Column(TEXT, nullable=False)
    about_job = Column(TEXT, nullable=False)
    responsibilities = Column(TEXT, nullable=False)
    salary = Column(TEXT, nullable=False)
    equity = Column(TEXT, nullable=False)
    task_id = Column(Integer, ForeignKey(task.id))
    fk_task_id = relationship(task, backref='job', lazy='dynamic')

class Task(Model, AuditMixin): # RefTypeMixin, TransientMixin, DocMixin
     __tablename__ = "task"
    id = Column(SERIAL, primary_key=True)
    task_name = Column(varchar(50))

# And that's all she said


