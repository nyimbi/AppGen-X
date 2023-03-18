
import enum
import datetime
from datetime import timedelta, datetime, date

from sqlalchemy.orm import relationship, query, defer, deferred, column_property, mapper
from sqlalchemy.schema import FetchedValue
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy import (Column, Integer, String, ForeignKey,
    Sequence, Float, Text, BigInteger, Date,
    DateTime, Time, Boolean, Index, CheckConstraint,
    UniqueConstraint, ForeignKeyConstraint, Numeric, LargeBinary , Table, func)

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
# import graphene
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



class Userx(Model, AuditMixin): # RefTypeMixin, TransientMixin, PlaceMixin, DocMixin, PersonMixin
    __tablename__ = 'userx'  

    id = Column(Integer, primary_key=True)

    ## Example stuff you can add to a table
    # def __repr__(self):
    #     return self.name
    #
    # def month_year(self):
    #     date = self.birthday or mindate
    #     return datetime.datetime(date.year, date.month, 1) or mindate
    #
    # def year(self):
    #     date = self.birthday or mindate
    #     return datetime.datetime(date.year, 1, 1)
    #
    # @hybrid_property
    # def length(self):
    #     return self.end - self.start
    #
    # @hybrid_method
    # def contains(self, point):
    #     return (self.start <= point) & (point <= self.end)
    #
    #
    # @hybrid_method
    # def intersects(self, other):
    #     return self.contains(other.start) | self.contains(other.end)

class Individual(Model, AuditMixin): # RefTypeMixin, TransientMixin, PlaceMixin, DocMixin, PersonMixin
    __tablename__ = 'individual'  

    id = Column(Integer, primary_key=True)
    userx = Column(Integer, ForeignKey('userx.id'))
    is_individual = Column(Boolean)
    is_institution = Column(Boolean)
    is_company = Column(Boolean)
    is_government = Column(Boolean)
    is_online = Column(Boolean)

    ## Example stuff you can add to a table
    # def __repr__(self):
    #     return self.name
    #
    # def month_year(self):
    #     date = self.birthday or mindate
    #     return datetime.datetime(date.year, date.month, 1) or mindate
    #
    # def year(self):
    #     date = self.birthday or mindate
    #     return datetime.datetime(date.year, 1, 1)
    #
    # @hybrid_property
    # def length(self):
    #     return self.end - self.start
    #
    # @hybrid_method
    # def contains(self, point):
    #     return (self.start <= point) & (point <= self.end)
    #
    #
    # @hybrid_method
    # def intersects(self, other):
    #     return self.contains(other.start) | self.contains(other.end)

class Industry(Model, AuditMixin): # RefTypeMixin, TransientMixin, PlaceMixin, DocMixin, PersonMixin
    __tablename__ = 'industry'  

    id = Column(Integer, primary_key=True)
    industry_code = Column(Text)

    ## Example stuff you can add to a table
    # def __repr__(self):
    #     return self.name
    #
    # def month_year(self):
    #     date = self.birthday or mindate
    #     return datetime.datetime(date.year, date.month, 1) or mindate
    #
    # def year(self):
    #     date = self.birthday or mindate
    #     return datetime.datetime(date.year, 1, 1)
    #
    # @hybrid_property
    # def length(self):
    #     return self.end - self.start
    #
    # @hybrid_method
    # def contains(self, point):
    #     return (self.start <= point) & (point <= self.end)
    #
    #
    # @hybrid_method
    # def intersects(self, other):
    #     return self.contains(other.start) | self.contains(other.end)

class IndustryJob(Model, AuditMixin): # RefTypeMixin, TransientMixin, PlaceMixin, DocMixin, PersonMixin
    __tablename__ = 'industry_job'  

    industry = Column(Integer, ForeignKey('industry.id'), primary_key=True)
    job = Column(Integer, ForeignKey('job.id'), primary_key=True)

    ## Example stuff you can add to a table
    # def __repr__(self):
    #     return self.name
    #
    # def month_year(self):
    #     date = self.birthday or mindate
    #     return datetime.datetime(date.year, date.month, 1) or mindate
    #
    # def year(self):
    #     date = self.birthday or mindate
    #     return datetime.datetime(date.year, 1, 1)
    #
    # @hybrid_property
    # def length(self):
    #     return self.end - self.start
    #
    # @hybrid_method
    # def contains(self, point):
    #     return (self.start <= point) & (point <= self.end)
    #
    #
    # @hybrid_method
    # def intersects(self, other):
    #     return self.contains(other.start) | self.contains(other.end)

class Job(Model, AuditMixin): # RefTypeMixin, TransientMixin, PlaceMixin, DocMixin, PersonMixin
    __tablename__ = 'job'  

    id = Column(Integer, primary_key=True)
    company_profile = Column(Text)
    about_job = Column(Text)
    responsibilities = Column(Text)
    salary = Column(Text)
    equity = Column(Text)
    offers_healthcare = Column(Boolean)
    offers_vision = Column(Boolean)
    offers_401k = Column(Boolean)
    offers_dental = Column(Boolean)
    paid_time_off = Column(Integer)
    vacation_days = Column(Integer)
    location = Column(Text)
    is_remote = Column(Boolean)
    applicant_count = Column(Integer)
    job_filled = Column(Boolean)

    ## Example stuff you can add to a table
    # def __repr__(self):
    #     return self.name
    #
    # def month_year(self):
    #     date = self.birthday or mindate
    #     return datetime.datetime(date.year, date.month, 1) or mindate
    #
    # def year(self):
    #     date = self.birthday or mindate
    #     return datetime.datetime(date.year, 1, 1)
    #
    # @hybrid_property
    # def length(self):
    #     return self.end - self.start
    #
    # @hybrid_method
    # def contains(self, point):
    #     return (self.start <= point) & (point <= self.end)
    #
    #
    # @hybrid_method
    # def intersects(self, other):
    #     return self.contains(other.start) | self.contains(other.end)

class JobSkill(Model, AuditMixin): # RefTypeMixin, TransientMixin, PlaceMixin, DocMixin, PersonMixin
    __tablename__ = 'job_skill'  

    skills = Column(Integer, ForeignKey('skill.id'), primary_key=True)
    jobs = Column(Integer, ForeignKey('job.id'), primary_key=True)

    ## Example stuff you can add to a table
    # def __repr__(self):
    #     return self.name
    #
    # def month_year(self):
    #     date = self.birthday or mindate
    #     return datetime.datetime(date.year, date.month, 1) or mindate
    #
    # def year(self):
    #     date = self.birthday or mindate
    #     return datetime.datetime(date.year, 1, 1)
    #
    # @hybrid_property
    # def length(self):
    #     return self.end - self.start
    #
    # @hybrid_method
    # def contains(self, point):
    #     return (self.start <= point) & (point <= self.end)
    #
    #
    # @hybrid_method
    # def intersects(self, other):
    #     return self.contains(other.start) | self.contains(other.end)

class Skill(Model, AuditMixin): # RefTypeMixin, TransientMixin, PlaceMixin, DocMixin, PersonMixin
    __tablename__ = 'skill'  

    id = Column(Integer, primary_key=True)
    skill_value = Column(Integer)

    ## Example stuff you can add to a table
    # def __repr__(self):
    #     return self.name
    #
    # def month_year(self):
    #     date = self.birthday or mindate
    #     return datetime.datetime(date.year, date.month, 1) or mindate
    #
    # def year(self):
    #     date = self.birthday or mindate
    #     return datetime.datetime(date.year, 1, 1)
    #
    # @hybrid_property
    # def length(self):
    #     return self.end - self.start
    #
    # @hybrid_method
    # def contains(self, point):
    #     return (self.start <= point) & (point <= self.end)
    #
    #
    # @hybrid_method
    # def intersects(self, other):
    #     return self.contains(other.start) | self.contains(other.end)

class Education(Model, AuditMixin): # RefTypeMixin, TransientMixin, PlaceMixin, DocMixin, PersonMixin
    __tablename__ = 'education'  

    id = Column(Integer, primary_key=True)
    individual = Column(Integer, ForeignKey('individual.id'))
    qualification = Column(Text)
    qual_class = Column(Text)
    verified = Column(Boolean)
    verification_code = Column(Text)
    verified_by = Column(Text)
    verification_date = Column(DateTime)
    verification_doc = Column(Text)

    ## Example stuff you can add to a table
    # def __repr__(self):
    #     return self.name
    #
    # def month_year(self):
    #     date = self.birthday or mindate
    #     return datetime.datetime(date.year, date.month, 1) or mindate
    #
    # def year(self):
    #     date = self.birthday or mindate
    #     return datetime.datetime(date.year, 1, 1)
    #
    # @hybrid_property
    # def length(self):
    #     return self.end - self.start
    #
    # @hybrid_method
    # def contains(self, point):
    #     return (self.start <= point) & (point <= self.end)
    #
    #
    # @hybrid_method
    # def intersects(self, other):
    #     return self.contains(other.start) | self.contains(other.end)

class IndividualJob(Model, AuditMixin): # RefTypeMixin, TransientMixin, PlaceMixin, DocMixin, PersonMixin
    __tablename__ = 'individual_job'  

    individual = Column(Integer, ForeignKey('individual.id'), primary_key=True)
    job = Column(Integer, ForeignKey('job.id'), primary_key=True)

    ## Example stuff you can add to a table
    # def __repr__(self):
    #     return self.name
    #
    # def month_year(self):
    #     date = self.birthday or mindate
    #     return datetime.datetime(date.year, date.month, 1) or mindate
    #
    # def year(self):
    #     date = self.birthday or mindate
    #     return datetime.datetime(date.year, 1, 1)
    #
    # @hybrid_property
    # def length(self):
    #     return self.end - self.start
    #
    # @hybrid_method
    # def contains(self, point):
    #     return (self.start <= point) & (point <= self.end)
    #
    #
    # @hybrid_method
    # def intersects(self, other):
    #     return self.contains(other.start) | self.contains(other.end)

class Profilesource(Model, AuditMixin): # RefTypeMixin, TransientMixin, PlaceMixin, DocMixin, PersonMixin
    __tablename__ = 'profilesource'  

    id = Column(Integer, primary_key=True)
    import_script = Column(Text)

    ## Example stuff you can add to a table
    # def __repr__(self):
    #     return self.name
    #
    # def month_year(self):
    #     date = self.birthday or mindate
    #     return datetime.datetime(date.year, date.month, 1) or mindate
    #
    # def year(self):
    #     date = self.birthday or mindate
    #     return datetime.datetime(date.year, 1, 1)
    #
    # @hybrid_property
    # def length(self):
    #     return self.end - self.start
    #
    # @hybrid_method
    # def contains(self, point):
    #     return (self.start <= point) & (point <= self.end)
    #
    #
    # @hybrid_method
    # def intersects(self, other):
    #     return self.contains(other.start) | self.contains(other.end)

class Location(Model, AuditMixin): # RefTypeMixin, TransientMixin, PlaceMixin, DocMixin, PersonMixin
    __tablename__ = 'location'  

    id = Column(Integer, primary_key=True)
    individual = Column(Integer, ForeignKey('individual.id'))

    ## Example stuff you can add to a table
    # def __repr__(self):
    #     return self.name
    #
    # def month_year(self):
    #     date = self.birthday or mindate
    #     return datetime.datetime(date.year, date.month, 1) or mindate
    #
    # def year(self):
    #     date = self.birthday or mindate
    #     return datetime.datetime(date.year, 1, 1)
    #
    # @hybrid_property
    # def length(self):
    #     return self.end - self.start
    #
    # @hybrid_method
    # def contains(self, point):
    #     return (self.start <= point) & (point <= self.end)
    #
    #
    # @hybrid_method
    # def intersects(self, other):
    #     return self.contains(other.start) | self.contains(other.end)

class Portal(Model, AuditMixin): # RefTypeMixin, TransientMixin, PlaceMixin, DocMixin, PersonMixin
    __tablename__ = 'portal'  

    id = Column(Integer, primary_key=True)
    portal_url = Column(Text)
    is_primary = Column(Text)
    portal_state = Column(Text)
    individual = Column(Integer, ForeignKey('individual.id'))
    has_custom_domain = Column(Boolean)
    domain = Column(Text)
    header_text = Column(Text)
    slug = Column(Text)
    automatic_fulfillment_digital_products = Column(Boolean)
    default_digital_max_downloads = Column(Integer)
    default_digital_url_valid_days = Column(Integer)
    default_mail_sender_name = Column(Text)
    default_mail_sender_address = Column(Text)
    fulfillment_auto_approve = Column(Boolean)
    fulfillment_allow_unpaid = Column(Boolean)
    reserve_stock_duration_anonymous_user = Column(Integer)
    reserve_stock_duration_authenticated_user = Column(Integer)
    limit_quantity_per_checkout = Column(Integer)
    gift_card_expiry_type = Column(Text)
    gift_card_expiry_period_type = Column(Text)
    gift_card_expiry_period = Column(Integer)
    charge_taxes_on_shipping = Column(Boolean)
    include_taxes_in_prices = Column(Boolean)
    display_gross_prices = Column(Boolean)
    language = Column(Text)

    ## Example stuff you can add to a table
    # def __repr__(self):
    #     return self.name
    #
    # def month_year(self):
    #     date = self.birthday or mindate
    #     return datetime.datetime(date.year, date.month, 1) or mindate
    #
    # def year(self):
    #     date = self.birthday or mindate
    #     return datetime.datetime(date.year, 1, 1)
    #
    # @hybrid_property
    # def length(self):
    #     return self.end - self.start
    #
    # @hybrid_method
    # def contains(self, point):
    #     return (self.start <= point) & (point <= self.end)
    #
    #
    # @hybrid_method
    # def intersects(self, other):
    #     return self.contains(other.start) | self.contains(other.end)

class Page(Model, AuditMixin): # RefTypeMixin, TransientMixin, PlaceMixin, DocMixin, PersonMixin
    __tablename__ = 'page'  

    id = Column(Integer, primary_key=True)
    portal = Column(Integer, ForeignKey('portal.id'))
    header = Column(Text)
    slug = Column(Text)
    page_type = Column(Text)

    ## Example stuff you can add to a table
    # def __repr__(self):
    #     return self.name
    #
    # def month_year(self):
    #     date = self.birthday or mindate
    #     return datetime.datetime(date.year, date.month, 1) or mindate
    #
    # def year(self):
    #     date = self.birthday or mindate
    #     return datetime.datetime(date.year, 1, 1)
    #
    # @hybrid_property
    # def length(self):
    #     return self.end - self.start
    #
    # @hybrid_method
    # def contains(self, point):
    #     return (self.start <= point) & (point <= self.end)
    #
    #
    # @hybrid_method
    # def intersects(self, other):
    #     return self.contains(other.start) | self.contains(other.end)

class Profile(Model, AuditMixin): # RefTypeMixin, TransientMixin, PlaceMixin, DocMixin, PersonMixin
    __tablename__ = 'profile'  

    id = Column(Integer, primary_key=True)
    individual = Column(Integer, ForeignKey('individual.id'))
    import_address = Column(Text)
    profile_username = Column(Text)
    profile_password = Column(Text)
    has_been_imported = Column(Boolean)
    import_data = Column(JSON)
    import_date = Column(DateTime)
    profilesource = Column(Integer, ForeignKey('profilesource.id'))

    ## Example stuff you can add to a table
    # def __repr__(self):
    #     return self.name
    #
    # def month_year(self):
    #     date = self.birthday or mindate
    #     return datetime.datetime(date.year, date.month, 1) or mindate
    #
    # def year(self):
    #     date = self.birthday or mindate
    #     return datetime.datetime(date.year, 1, 1)
    #
    # @hybrid_property
    # def length(self):
    #     return self.end - self.start
    #
    # @hybrid_method
    # def contains(self, point):
    #     return (self.start <= point) & (point <= self.end)
    #
    #
    # @hybrid_method
    # def intersects(self, other):
    #     return self.contains(other.start) | self.contains(other.end)

class Resume(Model, AuditMixin): # RefTypeMixin, TransientMixin, PlaceMixin, DocMixin, PersonMixin
    __tablename__ = 'resume'  

    id = Column(Integer, primary_key=True)
    individual = Column(Integer, ForeignKey('individual.id'))
    template = Column(Text)
    header = Column(Text)
    color = Column(Text)
    location = Column(Integer, ForeignKey('location.id'))
    summary_text = Column(Text)
    has_been_generated = Column(Boolean)
    preferred = Column(Boolean)

    ## Example stuff you can add to a table
    # def __repr__(self):
    #     return self.name
    #
    # def month_year(self):
    #     date = self.birthday or mindate
    #     return datetime.datetime(date.year, date.month, 1) or mindate
    #
    # def year(self):
    #     date = self.birthday or mindate
    #     return datetime.datetime(date.year, 1, 1)
    #
    # @hybrid_property
    # def length(self):
    #     return self.end - self.start
    #
    # @hybrid_method
    # def contains(self, point):
    #     return (self.start <= point) & (point <= self.end)
    #
    #
    # @hybrid_method
    # def intersects(self, other):
    #     return self.contains(other.start) | self.contains(other.end)

class Swarm(Model, AuditMixin): # RefTypeMixin, TransientMixin, PlaceMixin, DocMixin, PersonMixin
    __tablename__ = 'swarm'  

    id = Column(Integer, primary_key=True)
    portal = Column(Integer, ForeignKey('portal.id'))

    ## Example stuff you can add to a table
    # def __repr__(self):
    #     return self.name
    #
    # def month_year(self):
    #     date = self.birthday or mindate
    #     return datetime.datetime(date.year, date.month, 1) or mindate
    #
    # def year(self):
    #     date = self.birthday or mindate
    #     return datetime.datetime(date.year, 1, 1)
    #
    # @hybrid_property
    # def length(self):
    #     return self.end - self.start
    #
    # @hybrid_method
    # def contains(self, point):
    #     return (self.start <= point) & (point <= self.end)
    #
    #
    # @hybrid_method
    # def intersects(self, other):
    #     return self.contains(other.start) | self.contains(other.end)

class IndividualSwarm(Model, AuditMixin): # RefTypeMixin, TransientMixin, PlaceMixin, DocMixin, PersonMixin
    __tablename__ = 'individual_swarm'  

    individual = Column(Integer, ForeignKey('individual.id'), primary_key=True)
    swarm = Column(Integer, ForeignKey('swarm.id'), primary_key=True)

    ## Example stuff you can add to a table
    # def __repr__(self):
    #     return self.name
    #
    # def month_year(self):
    #     date = self.birthday or mindate
    #     return datetime.datetime(date.year, date.month, 1) or mindate
    #
    # def year(self):
    #     date = self.birthday or mindate
    #     return datetime.datetime(date.year, 1, 1)
    #
    # @hybrid_property
    # def length(self):
    #     return self.end - self.start
    #
    # @hybrid_method
    # def contains(self, point):
    #     return (self.start <= point) & (point <= self.end)
    #
    #
    # @hybrid_method
    # def intersects(self, other):
    #     return self.contains(other.start) | self.contains(other.end)

class UserSkill(Model, AuditMixin): # RefTypeMixin, TransientMixin, PlaceMixin, DocMixin, PersonMixin
    __tablename__ = 'user_skill'  

    skills = Column(Integer, ForeignKey('skill.id'), primary_key=True)
    user_details = Column(Integer, ForeignKey('individual.id'), primary_key=True)

    ## Example stuff you can add to a table
    # def __repr__(self):
    #     return self.name
    #
    # def month_year(self):
    #     date = self.birthday or mindate
    #     return datetime.datetime(date.year, date.month, 1) or mindate
    #
    # def year(self):
    #     date = self.birthday or mindate
    #     return datetime.datetime(date.year, 1, 1)
    #
    # @hybrid_property
    # def length(self):
    #     return self.end - self.start
    #
    # @hybrid_method
    # def contains(self, point):
    #     return (self.start <= point) & (point <= self.end)
    #
    #
    # @hybrid_method
    # def intersects(self, other):
    #     return self.contains(other.start) | self.contains(other.end)

class WorkHistory(Model, AuditMixin): # RefTypeMixin, TransientMixin, PlaceMixin, DocMixin, PersonMixin
    __tablename__ = 'work_history'  

    id = Column(Integer, primary_key=True)
    individual = Column(Integer, ForeignKey('individual.id'))
    resume = Column(Integer, ForeignKey('resume.id'))

    ## Example stuff you can add to a table
    # def __repr__(self):
    #     return self.name
    #
    # def month_year(self):
    #     date = self.birthday or mindate
    #     return datetime.datetime(date.year, date.month, 1) or mindate
    #
    # def year(self):
    #     date = self.birthday or mindate
    #     return datetime.datetime(date.year, 1, 1)
    #
    # @hybrid_property
    # def length(self):
    #     return self.end - self.start
    #
    # @hybrid_method
    # def contains(self, point):
    #     return (self.start <= point) & (point <= self.end)
    #
    #
    # @hybrid_method
    # def intersects(self, other):
    #     return self.contains(other.start) | self.contains(other.end)

# And that's all she said
