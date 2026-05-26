
from flask_appbuilder import ModelRestApi
from flask_appbuilder.api import BaseApi, expose
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.models.filters import BaseFilter
from sqlalchemy import or_
from sqlalchemy.sql import text

from . import appbuilder, db
from .models import *
class UserxRestApi(ModelRestApi):
    datamodel = SQLAInterface(Userx)
    include_columns = ['id']


appbuilder.add_api(UserxRestApi)


class IndividualRestApi(ModelRestApi):
    datamodel = SQLAInterface(Individual)
    include_columns = ['id', 'userx', 'is_individual', 'is_institution', 'is_company', 'is_government', 'is_online']


appbuilder.add_api(IndividualRestApi)


class IndustryRestApi(ModelRestApi):
    datamodel = SQLAInterface(Industry)
    include_columns = ['id', 'industry_code']


appbuilder.add_api(IndustryRestApi)


class IndustryJobRestApi(ModelRestApi):
    datamodel = SQLAInterface(IndustryJob)
    include_columns = ['industry', 'job']


appbuilder.add_api(IndustryJobRestApi)


class JobRestApi(ModelRestApi):
    datamodel = SQLAInterface(Job)
    include_columns = ['id', 'company_profile', 'about_job', 'responsibilities', 'salary', 'equity', 'offers_healthcare', 'offers_vision', 'offers_401k', 'offers_dental', 'paid_time_off', 'vacation_days', 'location', 'is_remote', 'applicant_count', 'job_filled']


appbuilder.add_api(JobRestApi)


class JobSkillRestApi(ModelRestApi):
    datamodel = SQLAInterface(JobSkill)
    include_columns = ['skills', 'jobs']


appbuilder.add_api(JobSkillRestApi)


class SkillRestApi(ModelRestApi):
    datamodel = SQLAInterface(Skill)
    include_columns = ['id', 'skill_value']


appbuilder.add_api(SkillRestApi)


class EducationRestApi(ModelRestApi):
    datamodel = SQLAInterface(Education)
    include_columns = ['id', 'individual', 'qualification', 'qual_class', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc']


appbuilder.add_api(EducationRestApi)


class IndividualJobRestApi(ModelRestApi):
    datamodel = SQLAInterface(IndividualJob)
    include_columns = ['individual', 'job']


appbuilder.add_api(IndividualJobRestApi)


class ProfilesourceRestApi(ModelRestApi):
    datamodel = SQLAInterface(Profilesource)
    include_columns = ['id', 'import_script']


appbuilder.add_api(ProfilesourceRestApi)


class LocationRestApi(ModelRestApi):
    datamodel = SQLAInterface(Location)
    include_columns = ['id', 'individual']


appbuilder.add_api(LocationRestApi)


class PortalRestApi(ModelRestApi):
    datamodel = SQLAInterface(Portal)
    include_columns = ['id', 'portal_url', 'is_primary', 'portal_state', 'individual', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_address', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gross_prices', 'language']


appbuilder.add_api(PortalRestApi)


class PageRestApi(ModelRestApi):
    datamodel = SQLAInterface(Page)
    include_columns = ['id', 'portal', 'header', 'slug', 'page_type']


appbuilder.add_api(PageRestApi)


class ProfileRestApi(ModelRestApi):
    datamodel = SQLAInterface(Profile)
    include_columns = ['id', 'individual', 'import_address', 'profile_username', 'profile_password', 'has_been_imported', 'import_data', 'import_date', 'profilesource']


appbuilder.add_api(ProfileRestApi)


class ResumeRestApi(ModelRestApi):
    datamodel = SQLAInterface(Resume)
    include_columns = ['id', 'individual', 'template', 'header', 'color', 'location', 'summary_text', 'has_been_generated', 'preferred']


appbuilder.add_api(ResumeRestApi)


class SwarmRestApi(ModelRestApi):
    datamodel = SQLAInterface(Swarm)
    include_columns = ['id', 'portal']


appbuilder.add_api(SwarmRestApi)


class IndividualSwarmRestApi(ModelRestApi):
    datamodel = SQLAInterface(IndividualSwarm)
    include_columns = ['individual', 'swarm']


appbuilder.add_api(IndividualSwarmRestApi)


class UserSkillRestApi(ModelRestApi):
    datamodel = SQLAInterface(UserSkill)
    include_columns = ['skills', 'user_details']


appbuilder.add_api(UserSkillRestApi)


class WorkHistoryRestApi(ModelRestApi):
    datamodel = SQLAInterface(WorkHistory)
    include_columns = ['id', 'individual', 'resume']


appbuilder.add_api(WorkHistoryRestApi)
