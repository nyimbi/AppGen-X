from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Float, Text, Date, Numeric, Interval, Enum
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from flask_appbuilder import Model

Base = Model

class CompanyType(Model):
    __tablename__ = 'company_type'
    id = Column(Integer, nullable=False)


class Company(Model):
    __tablename__ = 'company'
    id = Column(Integer, nullable=False)
    country = Column(Integer, ForeignKey('country.id'), nullable=False)
    company_type = Column(Integer, ForeignKey('company_type.id'), nullable=False)
    companytype_assoc = association_proxy('country', 'CompanyType')


class Country(Model):
    __tablename__ = 'country'
    id = Column(Integer, nullable=False)
    mapx = Column(Text, nullable=False)
    comments = Column(Text, nullable=False)
    region = Column(Integer, ForeignKey('region.id'), nullable=False)


class Region(Model):
    __tablename__ = 'region'
    id = Column(Integer, nullable=False)


class AudaInitiative(Model):
    __tablename__ = 'auda_initiative'
    id = Column(Integer, nullable=False)
    comment = Column(Text, nullable=False)


class AudaInitiativeCountry(Model):
    __tablename__ = 'auda_initiative_country'
    auda_initiative = Column(Integer, ForeignKey('auda_initiative.id'), nullable=False)
    country = Column(Integer, ForeignKey('country.id'), nullable=False)
    country_assoc = association_proxy('auda_initiative', 'Country')


class AudaPartner(Model):
    __tablename__ = 'auda_partner'
    id = Column(Integer, nullable=False)


class AudaPartnerCountry(Model):
    __tablename__ = 'auda_partner_country'
    auda_partner = Column(Integer, ForeignKey('auda_partner.id'), nullable=False)
    country = Column(Integer, ForeignKey('country.id'), nullable=False)
    country_assoc = association_proxy('auda_partner', 'Country')


class Law(Model):
    __tablename__ = 'law'
    id = Column(Integer, nullable=False)
    country = Column(Integer, ForeignKey('country.id'), nullable=False)
    date_of_enactment = Column(Text, nullable=False)
    text = Column(Text, nullable=False)


class ResourceType(Model):
    __tablename__ = 'resource_type'
    id = Column(Integer, nullable=False)


class Resource(Model):
    __tablename__ = 'resource'
    id = Column(Integer, nullable=False)
    resource_type = Column(Integer, ForeignKey('resource_type.id'), nullable=False)


class CountryResource(Model):
    __tablename__ = 'country_resource'
    country = Column(Integer, ForeignKey('country.id'), nullable=False)
    resource = Column(Integer, ForeignKey('resource.id'), nullable=False)
    resource_assoc = association_proxy('country', 'Resource')


class Startup(Model):
    __tablename__ = 'startup'
    id = Column(Integer, nullable=False)
    country = Column(Integer, ForeignKey('country.id'), nullable=False)


class Tender(Model):
    __tablename__ = 'tender'
    id = Column(Integer, nullable=False)
    country = Column(Integer, ForeignKey('country.id'), nullable=False)
    prerequisites = Column(Text, nullable=False)
    tenderdocument = Column(Text, nullable=False)
    tender_url = Column(Text, nullable=False)
