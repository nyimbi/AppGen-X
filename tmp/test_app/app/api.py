
from flask_appbuilder import ModelRestApi
from flask_appbuilder.api import BaseApi, expose
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.models.filters import BaseFilter
from sqlalchemy import or_
from sqlalchemy.sql import text

from . import appbuilder, db
from .models import *
class BrandRestApi(ModelRestApi):
    datamodel = SQLAInterface(brand)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'brand_grade', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(BrandRestApi)


class AccountRestApi(ModelRestApi):
    datamodel = SQLAInterface(account)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'account_type', 'general_ledger_account', 'use_as_service_account', 'use_as_billing_account', 'use_as_sales_account', 'use_as_shipping_account', 'asign_territory_flag', 'sla_expiration_date', 'hold_state_reason', 'sla_type', 'bill_delivery_method', 'auto_pay_enabled_flag', 'auto_payment_amount', 'payment_term', 'balance_amount', 'balance_amount_limit', 'thirty_day_balance_amount', 'sixty_day_balance_amount', 'ninety_day_balance_amount', 'default_freight_terms', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(AccountRestApi)


class AppTableRestApi(ModelRestApi):
    datamodel = SQLAInterface(app_table)
    include_columns = ['id', 'name']


appbuilder.add_api(AppTableRestApi)


class AccountContactRestApi(ModelRestApi):
    datamodel = SQLAInterface(account_contact)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'title', 'department_name', 'asistant_name', 'asistant_phone', 'last_activity_date', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(AccountContactRestApi)


class AppColumnRestApi(ModelRestApi):
    datamodel = SQLAInterface(app_column)
    include_columns = ['id', 'name', 'data_type', 'table_id']


appbuilder.add_api(AppColumnRestApi)


class AccountContactRoleRestApi(ModelRestApi):
    datamodel = SQLAInterface(account_contact_role)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'account_contact_role_type', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(AccountContactRoleRestApi)


class AccountPartnerRestApi(ModelRestApi):
    datamodel = SQLAInterface(account_partner)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(AccountPartnerRestApi)


class AttributeSetTranslationRestApi(ModelRestApi):
    datamodel = SQLAInterface(attribute_set_translation)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'translated_name', 'attribute_set', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(AttributeSetTranslationRestApi)


class AttributeTranslationRestApi(ModelRestApi):
    datamodel = SQLAInterface(attribute_translation)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'translated_name', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(AttributeTranslationRestApi)


class AppRelationshipRestApi(ModelRestApi):
    datamodel = SQLAInterface(app_relationship)
    include_columns = ['id', 'name', 'source_table_id', 'source_column_id', 'referred_table_id', 'referred_column_id']


appbuilder.add_api(AppRelationshipRestApi)


class AttributeValueRestApi(ModelRestApi):
    datamodel = SQLAInterface(attribute_value)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'attribute_value', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(AttributeValueRestApi)


class AttributeValueTranslationRestApi(ModelRestApi):
    datamodel = SQLAInterface(attribute_value_translation)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'translated_attribute_value', 'translated_attribute_value_description', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(AttributeValueTranslationRestApi)


class BillingFrequencyRestApi(ModelRestApi):
    datamodel = SQLAInterface(billing_frequency)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'billing_frequency_name', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(BillingFrequencyRestApi)


class BundleProductRestApi(ModelRestApi):
    datamodel = SQLAInterface(bundle_product)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'expected_waste_count', 'quantity_count', 'tare_weight', 'bundled_products_substitutional', 'bundled_products_decided_at_use', 'bundled_products_decides_availability', 'bundled_products_sold_together', 'weight_uo_m', 'quantity_unit_of_measure', 'quantity_schedule_type', 'disposal_type', 'long_description', 'minimum_advertisement_amount', 'is_back_ordered', 'valid_for_period_count', 'is_worker_discount_allowed', 'allow_partial_refund', 'is_weight_entry_required', 'is_quantity_entry_required', 'is_serialized', 'reward_program_points_count', 'revenue_installment_period', 'is_auto_provisionable', 'is_coupon_redemption_allowed', 'is_sellable_independently', 'can_use_revenue_schedule', 'manufacturer_name', 'is_intellectual_property_protected', 'model_year', 'is_customer_discount_allowed', 'product_state', 'brand_grade', 'quantity_installment_count', 'required_deposit_amount', 'revenue_schedule_type', 'is_pre_orderable', 'requires_invididual_unit_pricing', 'standard_warranty_length_month', 'can_use_quantity_schedule', 'is_installable', 'is_rain_check_allowed', 'minimum_advertisement_amount_start_date', 'maximum_order_quantity_count', 'is_multiple_coupons_allowed', 'allow_customer_return', 'model_number', 'msr_pamount', 'external_source_record', 'is_sellable', 'valid_to_date', 'price_charge_type', 'is_partner_discount_allowed', 'revenue_installment_count', 'product_sku', 'quantity_installment_period', 'is_manual_price_entry_required', 'is_sellable_without_price', 'gl_account_code', 'is_returnable', 'display_url', 'version_number', 'lot_identifier', 'valid_from_date', 'stock_ledger_valuation_amount', 'is_dynamic_bundle', 'is_quality_verification_required', 'required_deposit_percentage', 'is_foodstamp_payment_allowed', 'minimum_order_quantity_count', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(BundleProductRestApi)


class CapturePaymentRestApi(ModelRestApi):
    datamodel = SQLAInterface(capture_payment)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'capture_payment_id', 'capture_payment_type', 'handling_fee_amount', 'is_final_capture', 'payment_state', 'authorization_procesing_mode', 'i_paddr', 'comment_text', 'payment_number', 'payment_amount', 'latest_gateway_internal_result', 'customer_email_addr', 'latest_gateway_reference_number', 'latest_gateway_date', 'balance_amount', 'payment_type', 'customer_phone_number', 'latest_payment_gateway_mesage_text', 'payment_effective_date', 'external_created_date', 'payment_cancellation_date', 'mac_addr', 'total_applied_amount', 'net_applied_amount', 'total_unapplied_amount', 'latest_gateway_internal_reference_number', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(CapturePaymentRestApi)


class CompetitorRestApi(ModelRestApi):
    datamodel = SQLAInterface(competitor)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'competitor_strengths', 'competitor_from_date', 'social_media_post_rate', 'competitor_threats', 'current_ratio', 'cash_flow_growth', 'competitor_objectives', 'net_profit_margin', 'competitor_weakneses', 'pres_mentions_rate', 'aset_turnover_ratio', 'competitor_to_date', 'competitor_leverage_opportunities', 'aset_return_ratio', 'pto_enumber', 'ad_keywords', 'ad_reach_rate', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(CompetitorRestApi)


class ContactPointAddrRestApi(ModelRestApi):
    datamodel = SQLAInterface(contact_point_addr)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'is_used_for_shipping', 'state_province_name', 'addr_line3', 'country_name', 'postal_code_text', 'geo_latitude', 'addr_line2', 'addr_line4', 'geo_accuracy', 'geo_longitude', 'addr_line1', 'city_name', 'is_used_for_billing', 'primary_flag', 'profile_last_updated_date', 'profile_occurrence_count', 'for_busines_use', 'for_personal_use', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(ContactPointAddrRestApi)


class ContactPointPhoneRestApi(ModelRestApi):
    datamodel = SQLAInterface(contact_point_phone)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'extension_number', 'phone_country_code', 'country_name', 'area_code', 'is_sm_scapable', 'short_code', 'formatted_international_phone_number', 'primary_phone_type', 'is_fax_capable', 'formatted_e164_phone_number', 'formatted_national_phone_number', 'telephone_number', 'primary_flag', 'profile_occurrence_count', 'for_busines_use', 'for_personal_use', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(ContactPointPhoneRestApi)


class ContactPointTypeRestApi(ModelRestApi):
    datamodel = SQLAInterface(contact_point_type)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'opt_in_priority', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(ContactPointTypeRestApi)


class CouponRestApi(ModelRestApi):
    datamodel = SQLAInterface(coupon)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'primary_scan_code_label', 'is_return_coupon', 'expiration_date', 'secondary_scan_code_label', 'scan_code', 'coupon_code', 'return_coupon_reason', 'discount_amount', 'is_valid', 'coupon_state', 'discount_percentage', 'coupon_count', 'payment_method_state', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(CouponRestApi)


class CreditTenderRestApi(ModelRestApi):
    datamodel = SQLAInterface(credit_tender)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'payment_method_state', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(CreditTenderRestApi)


class CustomerRestApi(ModelRestApi):
    datamodel = SQLAInterface(customer)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'customer_state', 'prospect_rating', 'net_promoter_score', 'customer_satisfaction_score', 'marketing_email_response_rate', 'total_contracted_amount', 'total_profit_contribution_amount', 'customer_number', 'churn_score', 'originating_customer_source', 'total_life_time_value', 'total_bookings_amount', 'last24_months_new_revenue_amount', 'last12_months_new_revenue_amount', 'last12_months_support_call_count', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(CustomerRestApi)


class CustomerStateHistoryRestApi(ModelRestApi):
    datamodel = SQLAInterface(customer_state_history)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'start_date_time', 'party_role_state', 'end_date_time', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(CustomerStateHistoryRestApi)


class DeviceUserSesionRestApi(ModelRestApi):
    datamodel = SQLAInterface(device_user_sesion)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(DeviceUserSesionRestApi)


class GoodsProductRestApi(ModelRestApi):
    datamodel = SQLAInterface(goods_product)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'product_security_requirement', 'season', 'color', 'style', 'is_made_to_order', 'height', 'fabric', 'required_temperature_uo_m', 'shelf_facing_unit_count', 'required_humidity_percentage', 'required_temperature_lowest_number', 'gender', 'max_holding_day_count', 'diameter', 'is_perishable', 'required_cleanup_proces', 'pattern', 'required_temperature_highest_number', 'environment_requirement', 'drained_weight', 'net_weight', 'age', 'gros_weight', 'tare_weight', 'depth', 'width', 'size_uo_m', 'weight_uo_m', 'requires_unit_price_label', 'product_may_expand', 'quantity_schedule_type', 'disposal_type', 'minimum_advertisement_amount', 'is_back_ordered', 'valid_for_period_count', 'is_worker_discount_allowed', 'allow_partial_refund', 'is_weight_entry_required', 'is_quantity_entry_required', 'is_serialized', 'reward_program_points_count', 'revenue_installment_period', 'is_auto_provisionable', 'is_coupon_redemption_allowed', 'is_sellable_independently', 'can_use_revenue_schedule', 'manufacturer_name', 'is_intellectual_property_protected', 'model_year', 'is_customer_discount_allowed', 'product_state', 'brand_grade', 'quantity_installment_count', 'required_deposit_amount', 'revenue_schedule_type', 'is_pre_orderable', 'requires_invididual_unit_pricing', 'standard_warranty_length_month', 'can_use_quantity_schedule', 'is_installable', 'is_rain_check_allowed', 'minimum_advertisement_amount_start_date', 'maximum_order_quantity_count', 'is_multiple_coupons_allowed', 'allow_customer_return', 'model_number', 'msr_pamount', 'external_source_record', 'is_sellable', 'valid_to_date', 'price_charge_type', 'is_partner_discount_allowed', 'revenue_installment_count', 'product_sku', 'quantity_installment_period', 'is_manual_price_entry_required', 'is_sellable_without_price', 'gl_account_code', 'is_returnable', 'display_url', 'version_number', 'lot_identifier', 'valid_from_date', 'stock_ledger_valuation_amount', 'is_dynamic_bundle', 'is_quality_verification_required', 'required_deposit_percentage', 'is_foodstamp_payment_allowed', 'minimum_order_quantity_count', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(GoodsProductRestApi)


class HouseholdRestApi(ModelRestApi):
    datamodel = SQLAInterface(household)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'household_member_count', 'household_formed_date', 'household_disolved_date', 'party_type', 'global_party', 'no_merge_reason', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(HouseholdRestApi)


class IndustryRestApi(ModelRestApi):
    datamodel = SQLAInterface(industry)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'industry_code', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(IndustryRestApi)


class InternalBusinesUnitRestApi(ModelRestApi):
    datamodel = SQLAInterface(internal_busines_unit)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'busines_unit_type', 'party_type', 'global_party', 'no_merge_reason', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(InternalBusinesUnitRestApi)


class JobRestApi(ModelRestApi):
    datamodel = SQLAInterface(job)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'company_profile', 'about_job', 'responsibilities', 'salary', 'equity', 'offers_healthcare', 'offers_vision', 'offers_401k', 'offers_dental', 'paid_time_off', 'vacation_days', 'location', 'is_remote', 'applicant_count', 'job_filled', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(JobRestApi)


class LeadRestApi(ModelRestApi):
    datamodel = SQLAInterface(lead)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'state_province_name', 'lead_state', 'photo_ur_l', 'country_name', 'converted_date', 'company_name', 'street_name', 'lead_score', 'lead_rating', 'geo_code_latitude', 'geo_code_longitude', 'geo_code_accuracy', 'email_bounced_date', 'lead_source', 'last_activity_date', 'annual_revenue', 'email_bounced_reason', 'website', 'is_converted', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(LeadRestApi)


class OrderDeliveryMethodRestApi(ModelRestApi):
    datamodel = SQLAInterface(order_delivery_method)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'external_record', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(OrderDeliveryMethodRestApi)


class PartyRestApi(ModelRestApi):
    datamodel = SQLAInterface(party)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'party_type', 'global_party', 'no_merge_reason', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(PartyRestApi)


class PartyAdditionalNameRestApi(ModelRestApi):
    datamodel = SQLAInterface(party_additional_name)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'additional_name_type', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(PartyAdditionalNameRestApi)


class PartyIdentificationRestApi(ModelRestApi):
    datamodel = SQLAInterface(party_identification)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'expiry_date', 'party_identification_type', 'verified_date', 'isued_by_authority', 'isued_at_location', 'isued_date', 'identification_number', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(PartyIdentificationRestApi)


class PartyRelatedPartyRestApi(ModelRestApi):
    datamodel = SQLAInterface(party_related_party)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'related_from_date', 'related_to_date', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(PartyRelatedPartyRestApi)


class PartyRelationshipTypeRestApi(ModelRestApi):
    datamodel = SQLAInterface(party_relationship_type)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'is_bidirectional', 'party_role', 'related_party_role', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(PartyRelationshipTypeRestApi)


class PartyRoleRestApi(ModelRestApi):
    datamodel = SQLAInterface(party_role)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(PartyRoleRestApi)


class PartyWebAddrRestApi(ModelRestApi):
    datamodel = SQLAInterface(party_web_addr)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'web_site_ur_l', 'primary_flag', 'profile_last_updated_date', 'profile_occurrence_count', 'profile_first_created_date', 'for_busines_use', 'for_personal_use', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(PartyWebAddrRestApi)


class PaymentRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'payment_state', 'authorization_procesing_mode', 'i_paddr', 'comment_text', 'payment_number', 'payment_amount', 'latest_gateway_internal_result', 'customer_email_addr', 'latest_gateway_reference_number', 'latest_gateway_date', 'balance_amount', 'payment_type', 'customer_phone_number', 'latest_payment_gateway_mesage_text', 'payment_effective_date', 'external_created_date', 'payment_cancellation_date', 'mac_addr', 'total_applied_amount', 'net_applied_amount', 'total_unapplied_amount', 'latest_gateway_internal_reference_number', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(PaymentRestApi)


class PaymentAllocationRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_allocation)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'external_created_date', 'payment_allocation_name', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(PaymentAllocationRestApi)


class PaymentApplicationRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_application)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'effective_date', 'payment_application_type', 'comment_text', 'has_been_unapplied', 'applied_amount', 'payment_balance_amount', 'applied_date', 'external_created_date', 'unapplied_date', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(PaymentApplicationRestApi)


class PaymentAuthorizationRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_authorization)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'payment_gateway_reference_number', 'i_paddr', 'total_payment_capture_amount', 'payment_authorization_procesing_mode', 'authorization_amount', 'expiration_date', 'payment_gateway_internal_reference_number', 'gateway_reference_details_text', 'total_authorization_reversal_amount', 'payment_authorization_comment_text', 'external_created_date', 'payment_authorization_number', 'request_date', 'available_balance_amount', 'gateway_result_code_description', 'mac_addr', 'gateway_authorization_code', 'payment_gateway_date', 'payment_authorization_state', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(PaymentAuthorizationRestApi)


class PaymentAuthorizationReversalRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_authorization_reversal)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'payment_gateway_reference_number', 'authorization_reversal_amount', 'customer_authorization_reversal_phone', 'i_paddr', 'payment_authorization_reversal_state', 'payment_authorization_procesing_mode', 'payment_gateway_internal_reference_number', 'payment_authorization_reversal_name', 'external_created_date', 'request_date', 'payment_authorization_reversal_comment_text', 'mac_addr', 'customer_authorization_reversal_email', 'payment_gateway_date', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(PaymentAuthorizationReversalRestApi)


class PaymentCardRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_card)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'payment_card_type', 'card_holder_name', 'bill_to_first_name', 'bill_to_last_name', 'company_name', 'derived_card_type_code', 'expiration_month', 'expiration_year', 'isue_number', 'masked_number', 'number_last_digits', 'credit_card_expired', 'card_token', 'bill_to_street', 'bill_to_street2', 'bill_to_city', 'payment_method_state', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(PaymentCardRestApi)


class PaymentCreditMemoAllocationRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_credit_memo_allocation)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'applied_amount', 'external_created_date', 'payment_allocation_name', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(PaymentCreditMemoAllocationRestApi)


class PaymentCreditMemoApplicationRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_credit_memo_application)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'effective_date', 'payment_application_type', 'comment_text', 'has_been_unapplied', 'applied_amount', 'payment_balance_amount', 'applied_date', 'external_created_date', 'unapplied_date', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(PaymentCreditMemoApplicationRestApi)


class PaymentGatewayRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_gateway)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'payment_gateway_state', 'payment_gateway_comment_text', 'system_credential', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(PaymentGatewayRestApi)


class PaymentGatewayAuthReversalLogRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_gateway_auth_reversal_log)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'payment_gateway_reference_number', 'payment_gateway_mesage_text', 'payment_gateway_authorization_code', 'internal_result_code', 'payment_gateway_av_scode', 'internal_reference_number', 'payment_gateway_interaction_log_name', 'payment_gateway_interaction_state', 'payment_gateway_date', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(PaymentGatewayAuthReversalLogRestApi)


class PaymentGatewayAuthorizationLogRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_gateway_authorization_log)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'payment_gateway_reference_number', 'payment_gateway_mesage_text', 'payment_gateway_authorization_code', 'internal_result_code', 'payment_gateway_av_scode', 'internal_reference_number', 'payment_gateway_interaction_log_name', 'payment_gateway_interaction_state', 'payment_gateway_date', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(PaymentGatewayAuthorizationLogRestApi)


class PaymentGatewayInteractionLogRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_gateway_interaction_log)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'payment_gateway_reference_number', 'payment_gateway_mesage_text', 'payment_gateway_authorization_code', 'internal_result_code', 'payment_gateway_av_scode', 'internal_reference_number', 'payment_gateway_interaction_log_name', 'payment_gateway_interaction_state', 'payment_gateway_date', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(PaymentGatewayInteractionLogRestApi)


class PaymentGatewayInteractionTypeRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_gateway_interaction_type)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(PaymentGatewayInteractionTypeRestApi)


class PaymentGatewayPaymentLogRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_gateway_payment_log)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'payment_gateway_reference_number', 'payment_gateway_mesage_text', 'payment_gateway_authorization_code', 'internal_result_code', 'payment_gateway_av_scode', 'internal_reference_number', 'payment_gateway_interaction_log_name', 'payment_gateway_interaction_state', 'payment_gateway_date', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(PaymentGatewayPaymentLogRestApi)


class PaymentGatewayProviderRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_gateway_provider)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'apex_adapter_clas_name', 'payment_gateway_provider_comment_text', 'payment_gateway_provider_name', 'developer_name', 'namespace_prefix_text', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(PaymentGatewayProviderRestApi)


class PaymentGatewayResultCodeRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_gateway_result_code)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(PaymentGatewayResultCodeRestApi)


class PaymentGroupRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_group)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'total_reversal_amount', 'total_authorization_amount', 'total_payment_amount', 'payment_group_number', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(PaymentGroupRestApi)


class PaymentInvoiceAllocationRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_invoice_allocation)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'payment_invoice_allocation_name', 'applied_amount', 'invoice_balance_amount', 'external_created_date', 'payment_allocation_name', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(PaymentInvoiceAllocationRestApi)


class PaymentInvoiceApplicationRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_invoice_application)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'payment_invoice_application_name', 'invoice_balance_amount', 'payment_invoice_application_type', 'effective_date', 'payment_application_type', 'comment_text', 'has_been_unapplied', 'applied_amount', 'payment_balance_amount', 'applied_date', 'external_created_date', 'unapplied_date', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(PaymentInvoiceApplicationRestApi)


class PaymentMethodRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_method)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'payment_method_state', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(PaymentMethodRestApi)


class PaymentMethodTypeRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_method_type)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'type_description', 'media_type', 'max_per_period_amount', 'type_required_identification', 'use_minimum_age_year', 'max_transaction_amount', 'max_per_period_transaction_count', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(PaymentMethodTypeRestApi)


class PaymentPolicyRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_policy)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'payment_policy_state', 'payment_policy_treatment_selection', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(PaymentPolicyRestApi)


class PaymentTreatmentRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_treatment)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'payment_application_level', 'should_auto_invoice', 'payment_treatment_state', 'payment_treatment_name', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(PaymentTreatmentRestApi)


class PaymentTreatmentMethodRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_treatment_method)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'payment_treatment_method_name', 'payment_treatment_method_code', 'payment_treatment_method_description', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(PaymentTreatmentMethodRestApi)


class PersonLanguageRestApi(ModelRestApi):
    datamodel = SQLAInterface(person_language)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'spoken_proficiency_level', 'written_proficiency_level', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(PersonLanguageRestApi)


class PersonLifeEventRestApi(ModelRestApi):
    datamodel = SQLAInterface(person_life_event)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'person_life_event_date_time', 'person_life_event_type', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(PersonLifeEventRestApi)


class PriceAdjustmentGroupRestApi(ModelRestApi):
    datamodel = SQLAInterface(price_adjustment_group)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'price_adjustment_group_id', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(PriceAdjustmentGroupRestApi)


class PriceAdjustmentMethodRestApi(ModelRestApi):
    datamodel = SQLAInterface(price_adjustment_method)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(PriceAdjustmentMethodRestApi)


class PriceBookEntryRestApi(ModelRestApi):
    datamodel = SQLAInterface(price_book_entry)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'unit_list_price', 'min_required_quantity', 'min_required_order_value', 'max_required_order_value', 'use_standard_price', 'service_period_count', 'is_active', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(PriceBookEntryRestApi)


class ProductAttributeSetRestApi(ModelRestApi):
    datamodel = SQLAInterface(product_attribute_set)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'attribute_set', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(ProductAttributeSetRestApi)


class ProductAttributeValueRestApi(ModelRestApi):
    datamodel = SQLAInterface(product_attribute_value)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'custom_attribute_value', 'attribute_set', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(ProductAttributeValueRestApi)


class ProductCatalogRestApi(ModelRestApi):
    datamodel = SQLAInterface(product_catalog)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(ProductCatalogRestApi)


class ProductCatalogTranslationRestApi(ModelRestApi):
    datamodel = SQLAInterface(product_catalog_translation)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'translated_name', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(ProductCatalogTranslationRestApi)


class ProductCategoryRestApi(ModelRestApi):
    datamodel = SQLAInterface(product_category)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(ProductCategoryRestApi)


class ProductCategoryAttributeSetRestApi(ModelRestApi):
    datamodel = SQLAInterface(product_category_attribute_set)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'attribute_set', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(ProductCategoryAttributeSetRestApi)


class ProductCategoryProductRestApi(ModelRestApi):
    datamodel = SQLAInterface(product_category_product)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(ProductCategoryProductRestApi)


class ProductCategoryTranslationRestApi(ModelRestApi):
    datamodel = SQLAInterface(product_category_translation)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'translated_name', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(ProductCategoryTranslationRestApi)


class ProductCollateralRestApi(ModelRestApi):
    datamodel = SQLAInterface(product_collateral)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'url', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(ProductCollateralRestApi)


class ProductImageRestApi(ModelRestApi):
    datamodel = SQLAInterface(product_image)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'is_default_image', 'image_view_type', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(ProductImageRestApi)


class ProductImageTranslationRestApi(ModelRestApi):
    datamodel = SQLAInterface(product_image_translation)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'translated_name', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(ProductImageTranslationRestApi)


class ProductRelatedProductRestApi(ModelRestApi):
    datamodel = SQLAInterface(product_related_product)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'is_default_option', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(ProductRelatedProductRestApi)


class ProductRelationshipTypeRestApi(ModelRestApi):
    datamodel = SQLAInterface(product_relationship_type)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'parent_product_role', 'child_product_role', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(ProductRelationshipTypeRestApi)


class ProductTranslationRestApi(ModelRestApi):
    datamodel = SQLAInterface(product_translation)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(ProductTranslationRestApi)


class ProductValidityTimePeriodUoMRestApi(ModelRestApi):
    datamodel = SQLAInterface(product_validity_time_period_uo_m)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'plural_name', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(ProductValidityTimePeriodUoMRestApi)


class ProfilesourceRestApi(ModelRestApi):
    datamodel = SQLAInterface(profilesource)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'import_script', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(ProfilesourceRestApi)


class RefundAllocationRestApi(ModelRestApi):
    datamodel = SQLAInterface(refund_allocation)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'effective_date', 'has_been_unapplied', 'refund_allocation_type', 'allocated_amount', 'refund_balance_amount', 'refund_allocation_name', 'applied_date', 'external_created_date', 'unapplied_date', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(RefundAllocationRestApi)


class RefundCreditMemoAllocationRestApi(ModelRestApi):
    datamodel = SQLAInterface(refund_credit_memo_allocation)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'effective_date', 'has_been_unapplied', 'refund_allocation_type', 'allocated_amount', 'refund_balance_amount', 'refund_allocation_name', 'applied_date', 'external_created_date', 'unapplied_date', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(RefundCreditMemoAllocationRestApi)


class RefundPaymentRestApi(ModelRestApi):
    datamodel = SQLAInterface(refund_payment)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'external_created_date', 'payment_state', 'authorization_procesing_mode', 'i_paddr', 'comment_text', 'payment_number', 'payment_amount', 'latest_gateway_internal_result', 'customer_email_addr', 'latest_gateway_reference_number', 'latest_gateway_date', 'balance_amount', 'payment_type', 'customer_phone_number', 'latest_payment_gateway_mesage_text', 'payment_effective_date', 'payment_cancellation_date', 'mac_addr', 'total_applied_amount', 'net_applied_amount', 'total_unapplied_amount', 'latest_gateway_internal_reference_number', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(RefundPaymentRestApi)


class RefundPaymentAllocationRestApi(ModelRestApi):
    datamodel = SQLAInterface(refund_payment_allocation)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'refund_allocation_comments_date', 'payment_balance_amount', 'refund_allocation_comment_text', 'credit_memo_balance_amount', 'refund_payment_allocation_name', 'effective_date', 'has_been_unapplied', 'refund_allocation_type', 'allocated_amount', 'refund_balance_amount', 'refund_allocation_name', 'applied_date', 'external_created_date', 'unapplied_date', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(RefundPaymentAllocationRestApi)


class RenewalTermRestApi(ModelRestApi):
    datamodel = SQLAInterface(renewal_term)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(RenewalTermRestApi)


class SalesChannelRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_channel)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'external_record', 'sales_channel_number', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(SalesChannelRestApi)


class SalesChannelTypeRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_channel_type)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(SalesChannelTypeRestApi)


class SalesOrderRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'total_pending_billing_amount', 'checkout_date', 'price_calculation_state_mesage_text', 'confirmation_recipient_email_text', 'order_end_date', 'is_tax_exempt', 'total_product_tax_amount', 'is_alerted', 'is_anonymous', 'is_closed', 'activated_date', 'requested_start_date', 'company_authorized_date', 'order_insurance_amount', 'total_delivery_amount', 'customer_authorized_date', 'total_cancelled_billing_amount', 'total_adjusted_delivery_tax_amount', 'total_adjustment_amount', 'renewal_uplift_rate', 'total_product_amount', 'total_adjustment_tax_amount', 'is_gift_order', 'promise_fulfillment_date', 'filed_date', 'i_so_culture', 'purchase_order_number', 'total_delivery_fee_amount', 'total_delivery_tax_amount', 'total_tax_amount', 'order_number', 'can_bill_now', 'promise_date', 'paid_date', 'packed_date', 'fulfilled_date', 'total_booking_amount', 'adjusted_product_tax_amount', 'is_historical_only', 'grand_total_amount', 'is_contracted', 'adjusted_total_product_amount', 'order_discount', 'order_start_date', 'cancel_date_type', 'is_reduction_order', 'sales_order_system_state', 'is_suspended', 'purchase_order_date', 'billing_day_of_the_month', 'cancel_date', 'tax_rate', 'developer_state_code', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(SalesOrderRestApi)


class SalesOrderChangeLogRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_change_log)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(SalesOrderChangeLogRestApi)


class SalesOrderChangeTypeRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_change_type)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'sales_order_change_type_name', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(SalesOrderChangeTypeRestApi)


class SalesOrderConfirmationStateRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_confirmation_state)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(SalesOrderConfirmationStateRestApi)


class SalesOrderDeliveryGroupRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_delivery_group)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'promised_date', 'is_gift', 'gift_mesage_text', 'desired_delivery_date', 'delivery_instructions_text', 'total_unit_price_amount', 'total_delivery_charge_amount', 'total_delivery_adjustment_amount', 'total_delivery_tax_amount', 'total_delivery_charge_tax_amount', 'total_delivery_adjustment_tax_amount', 'total_tax_amount', 'total_product_tax_amount', 'total_price_amount', 'grand_total_delivery_amount', 'sales_order_delivery_group_number', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(SalesOrderDeliveryGroupRestApi)


class SalesOrderDeliveryStateRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_delivery_state)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(SalesOrderDeliveryStateRestApi)


class SalesOrderPaymentSummaryRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_payment_summary)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'authorization_reversal_amount', 'authorization_amount', 'unapplied_amount', 'payment_amount', 'applied_amount', 'available_to_apply_balance_amount', 'captured_amount', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(SalesOrderPaymentSummaryRestApi)


class SalesOrderPriceAdjustmentRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_price_adjustment)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'total_adjustment_tax_amount', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(SalesOrderPriceAdjustmentRestApi)


class SalesOrderPriceAdjustmentTypeRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_price_adjustment_type)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(SalesOrderPriceAdjustmentTypeRestApi)


class SalesOrderProductRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_product)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'total_recurring_price_amount', 'total_line_adjustment_amount', 'total_price_amount', 'provisioning_date', 'fulfilled_quantity', 'total_line_amount', 'promised_date', 'recurring_price_amount', 'end_date', 'gift_order_mesage_text', 'quantity_ordered_uo_m', 'total_product_tax_amount', 'line_adjustment_sub_total_amount', 'comment_text', 'order_product_number', 'ordered_quantity', 'unit_price_amount', 'requested_start_date', 'subscription_renewal_month_quantity', 'order_manual_adjustment_sub_total_amount', 'allocated_quantity', 'allocation_partition_name', 'is_gift', 'unit_tax_amount', 'delivery_tax_amount', 'is_bonus_product', 'sales_order_product_adjusted_tax_amount', 'total_adjustment_amount', 'shipping_tax_amount', 'total_list_price_amount', 'total_adjustment_tax_amount', 'order_adjustment_sub_total_amount', 'subscription_term_quantity', 'total_distributed_adjustment_tax_amount', 'total_distributed_tax_amount', 'total_tax_amount', 'adjusted_delivery_tax_amount', 'list_price_amount', 'segment_index', 'shipping_cost_amount', 'is_bundle_root', 'discount_amount', 'cancelled_quantity', 'list_price_quantity_uo_m', 'total_distributed_adjustment_amount', 'segment_index_number', 'total_unit_price_amount', 'available_quantity', 'requested_end_date', 'allocation_group_name', 'gift_recipient_telephone_number', 'is_automatically_renewed', 'discount_percent', 'total_manual_adjustment_amount', 'handling_cost_amount', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(SalesOrderProductRestApi)


class SalesOrderProductGroupRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_product_group)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(SalesOrderProductGroupRestApi)


class SalesOrderProductGroupTypeRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_product_group_type)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(SalesOrderProductGroupTypeRestApi)


class SalesOrderProductNoteRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_product_note)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'note_text', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(SalesOrderProductNoteRestApi)


class SalesOrderProductReasonRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_product_reason)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(SalesOrderProductReasonRestApi)


class SalesOrderProductReasonCategoryRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_product_reason_category)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(SalesOrderProductReasonCategoryRestApi)


class SalesOrderProductStateRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_product_state)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(SalesOrderProductStateRestApi)


class SalesOrderProductTaxRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_product_tax)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'tax_effective_date', 'tax_amount', 'sales_order_tax_amount', 'tax_addr_city_name', 'tax_error_mesage_text', 'tax_addr_street1_text', 'tax_rate_percent', 'tax_addr_street2_text', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(SalesOrderProductTaxRestApi)


class SalesOrderSegmentRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_segment)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(SalesOrderSegmentRestApi)


class SalesOrderStateRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_state)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(SalesOrderStateRestApi)


class SalesOrderTaxRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_tax)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'sales_order_tax_amount', 'tax_addr_city_name', 'tax_error_mesage_text', 'tax_addr_street1_text', 'tax_rate_percent', 'tax_addr_street2_text', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(SalesOrderTaxRestApi)


class SalesOrderTypeRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_type)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(SalesOrderTypeRestApi)


class SellerRestApi(ModelRestApi):
    datamodel = SQLAInterface(seller)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'community_participation_count', 'demonstrations_given_count', 'event_participation_count', 'customer_satisfaction_score', 'training_certification_count', 'opportunity_involvement_count', 'marketing_development_amount', 'seller_type', 'documentation_download_count', 'trial_participation_count', 'credit_rating', 'satisfaction_score', 'sales_amount', 'opportunity_win_rate', 'product_return_rate', 'lead_generation_count', 'inventory_value_amount', 'major_post_sale_support_needed', 'training_participation_count', 'new_customer_acquisition_count', 'succes_story_count', 'system_login_count', 'joint_busines_plan_exist', 'average_converted_lead_amount', 'estimated_partner_gros_margin', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(SellerRestApi)


class ServiceProductRestApi(ModelRestApi):
    datamodel = SQLAInterface(service_product)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'rental_term_violation_penalty_amount', 'evergreen_contract_estimated_month_count', 'evergreen_contract_estimated_charge_amount', 'service_period_uo_m', 'service_period_count', 'rental_cleanup_fee_amount', 'service_type', 'quantity_schedule_type', 'disposal_type', 'long_description', 'minimum_advertisement_amount', 'is_back_ordered', 'valid_for_period_count', 'is_worker_discount_allowed', 'allow_partial_refund', 'is_weight_entry_required', 'is_quantity_entry_required', 'is_serialized', 'reward_program_points_count', 'revenue_installment_period', 'is_auto_provisionable', 'is_coupon_redemption_allowed', 'is_sellable_independently', 'can_use_revenue_schedule', 'manufacturer_name', 'is_intellectual_property_protected', 'model_year', 'is_customer_discount_allowed', 'product_state', 'brand_grade', 'quantity_installment_count', 'required_deposit_amount', 'revenue_schedule_type', 'is_pre_orderable', 'requires_invididual_unit_pricing', 'standard_warranty_length_month', 'can_use_quantity_schedule', 'is_installable', 'is_rain_check_allowed', 'minimum_advertisement_amount_start_date', 'maximum_order_quantity_count', 'is_multiple_coupons_allowed', 'allow_customer_return', 'model_number', 'm_sr_pamount', 'external_source_record', 'is_sellable', 'valid_to_date', 'price_charge_type', 'is_partner_discount_allowed', 'revenue_installment_count', 'product_sk_u', 'quantity_installment_period', 'is_manual_price_entry_required', 'is_sellable_without_price', 'gl_account_code', 'is_returnable', 'display_url', 'version_number', 'lot_identifier', 'valid_from_date', 'stock_ledger_valuation_amount', 'is_dynamic_bundle', 'is_quality_verification_required', 'required_deposit_percentage', 'is_foodstamp_payment_allowed', 'minimum_order_quantity_count', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(ServiceProductRestApi)


class ShipmentRestApi(ModelRestApi):
    datamodel = SQLAInterface(shipment)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'gift_mesage_text', 'shipment_number', 'is_gift', 'actual_delivery_date_time', 'special_instructions_text', 'carrier_tracking_number', 'estimated_delivery_date_time', 'scheduled_delivery_date_time', 'shipment_date', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(ShipmentRestApi)


class ShipmentDocumentRestApi(ModelRestApi):
    datamodel = SQLAInterface(shipment_document)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(ShipmentDocumentRestApi)


class ShipmentPackageRestApi(ModelRestApi):
    datamodel = SQLAInterface(shipment_package)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'shipment_product_count', 'shipment_product_description', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(ShipmentPackageRestApi)


class ShipmentProductRestApi(ModelRestApi):
    datamodel = SQLAInterface(shipment_product)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'shipment_product_count', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(ShipmentProductRestApi)


class ShipmentProductPriceAdjustmentRestApi(ModelRestApi):
    datamodel = SQLAInterface(shipment_product_price_adjustment)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'adjustment_amount', 'shipment_product_price_adjustment_amount', 'adjustment_tax_amount', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(ShipmentProductPriceAdjustmentRestApi)


class ShipmentProductPriceAdjustmentTaxRestApi(ModelRestApi):
    datamodel = SQLAInterface(shipment_product_price_adjustment_tax)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(ShipmentProductPriceAdjustmentTaxRestApi)


class ShipmentStateRestApi(ModelRestApi):
    datamodel = SQLAInterface(shipment_state)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(ShipmentStateRestApi)


class ShippingMethodRestApi(ModelRestApi):
    datamodel = SQLAInterface(shipping_method)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(ShippingMethodRestApi)


class SkillRestApi(ModelRestApi):
    datamodel = SQLAInterface(skill)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'skill_value', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(SkillRestApi)


class SupplierRestApi(ModelRestApi):
    datamodel = SQLAInterface(supplier)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'satisfaction_ethics_rank', 'contract_invoice_accuracy_rate', 'satisfaction_weight_percent', 'contract_on_time_delivery_rate', 'competitive_warranty_rank', 'competitive_marketing_rank', 'contract_delivery_correctnes_rate', 'competitive_weight_score', 'contract_sl_aisue_rate', 'competitive_weight_percent', 'supplier_score', 'competitive_product_price_rank', 'contract_weight_percent', 'supplier_spend', 'satisfaction_technical_support_rank', 'contract_weight_score', 'satisfaction_customer_service_rank', 'satisfaction_weight_score', 'contract_sourcing_cycle_days', 'supplier_type', 'is_carrier', 'contract_product_return_rate', 'competitive_cost_avoidance_rank', 'contract_product_quality_rate', 'contract_budget_cost_rate', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(SupplierRestApi)


class UncategorizedPartyRestApi(ModelRestApi):
    datamodel = SQLAInterface(uncategorized_party)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'creation_reason', 'uncategorized_party_label', 'original_source_record', 'original_source_system', 'party_type', 'global_party', 'no_merge_reason', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(UncategorizedPartyRestApi)


class UserxRestApi(ModelRestApi):
    datamodel = SQLAInterface(userx)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(UserxRestApi)


class AccountAutoPaymentMethodJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(account_auto_payment_method_join)
    include_columns = ['account_id', 'payment_method_id']


appbuilder.add_api(AccountAutoPaymentMethodJoinRestApi)


class AccountBillFrequencyJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(account_bill_frequency_join)
    include_columns = ['account_id', 'billing_frequency_id']


appbuilder.add_api(AccountBillFrequencyJoinRestApi)


class AccountContactAccountJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(account_contact_account_join)
    include_columns = ['account_contact_id', 'account_id']


appbuilder.add_api(AccountContactAccountJoinRestApi)


class AccountContactIndirectRelationAccountContactJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(account_contact_indirect_relation_account_contact_join)
    include_columns = ['account_contact_id_left', 'account_contact_id_right']


appbuilder.add_api(AccountContactIndirectRelationAccountContactJoinRestApi)


class AccountContactReportsToAccountContactJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(account_contact_reports_to_account_contact_join)
    include_columns = ['account_contact_id_left', 'account_contact_id_right']


appbuilder.add_api(AccountContactReportsToAccountContactJoinRestApi)


class AccountContactRoleAccountContactJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(account_contact_role_account_contact_join)
    include_columns = ['account_contact_role_id', 'account_contact_id']


appbuilder.add_api(AccountContactRoleAccountContactJoinRestApi)


class AccountOrderDeliveryMethodJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(account_order_delivery_method_join)
    include_columns = ['account_id', 'order_delivery_method_id']


appbuilder.add_api(AccountOrderDeliveryMethodJoinRestApi)


class AccountParentAccountJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(account_parent_account_join)
    include_columns = ['account_id_left', 'account_id_right']


appbuilder.add_api(AccountParentAccountJoinRestApi)


class AccountPartnerAccountJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(account_partner_account_join)
    include_columns = ['account_partner_id', 'account_id']


appbuilder.add_api(AccountPartnerAccountJoinRestApi)


class AccountPartnerPartnerAccountJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(account_partner_partner_account_join)
    include_columns = ['account_partner_id', 'account_id']


appbuilder.add_api(AccountPartnerPartnerAccountJoinRestApi)


class AccountPartyJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(account_party_join)
    include_columns = ['account_id', 'party_id']


appbuilder.add_api(AccountPartyJoinRestApi)


class AccountPartyRoleJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(account_party_role_join)
    include_columns = ['account_id', 'party_role_id']


appbuilder.add_api(AccountPartyRoleJoinRestApi)


class AccountPrimarySalesContactPointJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(account_primary_sales_contact_point_join)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'account_id', 'contact_point_id', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(AccountPrimarySalesContactPointJoinRestApi)


class AccountShippingContactJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(account_shipping_contact_join)
    include_columns = ['account_id', 'account_contact_id']


appbuilder.add_api(AccountShippingContactJoinRestApi)


class AccountShippingEmailJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(account_shipping_email_join)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'account_id', 'contact_point_email_id', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(AccountShippingEmailJoinRestApi)


class AccountShippingPhoneidJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(account_shipping_phoneid_join)
    include_columns = ['account_id', 'contact_point_phone_id']


appbuilder.add_api(AccountShippingPhoneidJoinRestApi)


class AttributeValueTranslationAttributeValueJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(attribute_value_translation_attribute_value_join)
    include_columns = ['attribute_value_translation_id', 'attribute_value_id']


appbuilder.add_api(AttributeValueTranslationAttributeValueJoinRestApi)


class BundleProductBrandJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(bundle_product_brand_join)
    include_columns = ['bundle_product_id', 'brand_id']


appbuilder.add_api(BundleProductBrandJoinRestApi)


class BundleProductPrimaryProductCategoryJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(bundle_product_primary_product_category_join)
    include_columns = ['bundle_product_id', 'product_category_id']


appbuilder.add_api(BundleProductPrimaryProductCategoryJoinRestApi)


class BundleProductPrimarySalesChannelJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(bundle_product_primary_sales_channel_join)
    include_columns = ['bundle_product_id', 'sales_channel_id']


appbuilder.add_api(BundleProductPrimarySalesChannelJoinRestApi)


class BundleProductValidForPeriodUoMJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(bundle_product_valid_for_period_uo_m_join)
    include_columns = ['bundle_product_id', 'product_validity_time_period_uo_m_id']


appbuilder.add_api(BundleProductValidForPeriodUoMJoinRestApi)


class CapturePaymentAccountJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(capture_payment_account_join)
    include_columns = ['capture_payment_capture_payment_id', 'account_id']


appbuilder.add_api(CapturePaymentAccountJoinRestApi)


class CapturePaymentInternalBusinesUnitJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(capture_payment_internal_busines_unit_join)
    include_columns = ['capture_payment_capture_payment_id', 'internal_busines_unit_id']


appbuilder.add_api(CapturePaymentInternalBusinesUnitJoinRestApi)


class CapturePaymentLatestGatewayResultCodeJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(capture_payment_latest_gateway_result_code_join)
    include_columns = ['capture_payment_capture_payment_id', 'payment_gateway_result_code_id']


appbuilder.add_api(CapturePaymentLatestGatewayResultCodeJoinRestApi)


class CapturePaymentPaymentAuthorizationJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(capture_payment_payment_authorization_join)
    include_columns = ['capture_payment_capture_payment_id', 'payment_authorization_id']


appbuilder.add_api(CapturePaymentPaymentAuthorizationJoinRestApi)


class CapturePaymentPaymentGatewayJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(capture_payment_payment_gateway_join)
    include_columns = ['capture_payment_capture_payment_id', 'payment_gateway_id']


appbuilder.add_api(CapturePaymentPaymentGatewayJoinRestApi)


class CapturePaymentPaymentGroupJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(capture_payment_payment_group_join)
    include_columns = ['capture_payment_capture_payment_id', 'payment_group_id']


appbuilder.add_api(CapturePaymentPaymentGroupJoinRestApi)


class CapturePaymentPaymentMethodJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(capture_payment_payment_method_join)
    include_columns = ['capture_payment_capture_payment_id', 'payment_method_id']


appbuilder.add_api(CapturePaymentPaymentMethodJoinRestApi)


class CapturePaymentPaymentTreatmentJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(capture_payment_payment_treatment_join)
    include_columns = ['capture_payment_capture_payment_id', 'payment_treatment_id']


appbuilder.add_api(CapturePaymentPaymentTreatmentJoinRestApi)


class CapturePaymentSalesOrderPaymentSummaryJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(capture_payment_sales_order_payment_summary_join)
    include_columns = ['capture_payment_capture_payment_id', 'sales_order_payment_summary_id']


appbuilder.add_api(CapturePaymentSalesOrderPaymentSummaryJoinRestApi)


class CompetitorPartyJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(competitor_party_join)
    include_columns = ['competitor_id', 'party_id']


appbuilder.add_api(CompetitorPartyJoinRestApi)


class CouponManufacturerJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(coupon_manufacturer_join)
    include_columns = ['coupon_id', 'party_id']


appbuilder.add_api(CouponManufacturerJoinRestApi)


class CouponPaymentMethodTypeJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(coupon_payment_method_type_join)
    include_columns = ['coupon_id', 'payment_method_type_id']


appbuilder.add_api(CouponPaymentMethodTypeJoinRestApi)


class CreditTenderAccountJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(credit_tender_account_join)
    include_columns = ['credit_tender_id', 'account_id']


appbuilder.add_api(CreditTenderAccountJoinRestApi)


class CreditTenderPaymentMethodTypeJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(credit_tender_payment_method_type_join)
    include_columns = ['credit_tender_id', 'payment_method_type_id']


appbuilder.add_api(CreditTenderPaymentMethodTypeJoinRestApi)


class CustomerPartyJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(customer_party_join)
    include_columns = ['customer_id', 'party_id']


appbuilder.add_api(CustomerPartyJoinRestApi)


class CustomerStateHistoryPartyRoleJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(customer_state_history_party_role_join)
    include_columns = ['customer_state_history_id', 'party_role_id']


appbuilder.add_api(CustomerStateHistoryPartyRoleJoinRestApi)


class GoodsProductBrandJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(goods_product_brand_join)
    include_columns = ['goods_product_id', 'brand_id']


appbuilder.add_api(GoodsProductBrandJoinRestApi)


class GoodsProductPrimaryProductCategoryJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(goods_product_primary_product_category_join)
    include_columns = ['goods_product_id', 'product_category_id']


appbuilder.add_api(GoodsProductPrimaryProductCategoryJoinRestApi)


class GoodsProductPrimarySalesChannelJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(goods_product_primary_sales_channel_join)
    include_columns = ['goods_product_id', 'sales_channel_id']


appbuilder.add_api(GoodsProductPrimarySalesChannelJoinRestApi)


class GoodsProductValidForPeriodUoMJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(goods_product_valid_for_period_uo_m_join)
    include_columns = ['goods_product_id', 'product_validity_time_period_uo_m_id']


appbuilder.add_api(GoodsProductValidForPeriodUoMJoinRestApi)


class HouseholdPrimaryAccountJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(household_primary_account_join)
    include_columns = ['household_id', 'account_id']


appbuilder.add_api(HouseholdPrimaryAccountJoinRestApi)


class IndividualRestApi(ModelRestApi):
    datamodel = SQLAInterface(individual)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'is_institution', 'is_company', 'is_online', 'userx_id', 'photo_url', 'do_extract_my_data_update_date', 'should_forget', 'web_site_url', 'ordering_name', 'over_age_number', 'send_individual_data', 'mothers_maiden_name', 'residence_country_name', 'party_type', 'global_party', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(IndividualRestApi)


class IndustryJobRestApi(ModelRestApi):
    datamodel = SQLAInterface(industry_job)
    include_columns = ['industry', 'job']


appbuilder.add_api(IndustryJobRestApi)


class InternalBusinesUnitParentInternalBusinesUnitJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(internal_busines_unit_parent_internal_busines_unit_join)
    include_columns = ['internal_busines_unit_id_left', 'internal_busines_unit_id_right']


appbuilder.add_api(InternalBusinesUnitParentInternalBusinesUnitJoinRestApi)


class InternalBusinesUnitPrimaryAccountJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(internal_busines_unit_primary_account_join)
    include_columns = ['internal_busines_unit_id', 'account_id']


appbuilder.add_api(InternalBusinesUnitPrimaryAccountJoinRestApi)


class JobSkillRestApi(ModelRestApi):
    datamodel = SQLAInterface(job_skill)
    include_columns = ['skills', 'jobs']


appbuilder.add_api(JobSkillRestApi)


class LeadConvertedToAccountContactJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(lead_converted_to_account_contact_join)
    include_columns = ['lead_id', 'account_contact_id']


appbuilder.add_api(LeadConvertedToAccountContactJoinRestApi)


class LeadConvertedToAccountJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(lead_converted_to_account_join)
    include_columns = ['lead_id', 'account_id']


appbuilder.add_api(LeadConvertedToAccountJoinRestApi)


class LeadFaxContactPhoneJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(lead_fax_contact_phone_join)
    include_columns = ['lead_id', 'contact_point_phone_id']


appbuilder.add_api(LeadFaxContactPhoneJoinRestApi)


class LeadMobileContactPhoneJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(lead_mobile_contact_phone_join)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'lead_id', 'contact_point_phone_id', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(LeadMobileContactPhoneJoinRestApi)


class LeadPartnerAccountJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(lead_partner_account_join)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'lead_id', 'account_id', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(LeadPartnerAccountJoinRestApi)


class LeadPartyRoleJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(lead_party_role_join)
    include_columns = ['lead_id', 'party_role_id']


appbuilder.add_api(LeadPartyRoleJoinRestApi)


class PartyAdditionalNamePartyJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(party_additional_name_party_join)
    include_columns = ['party_additional_name_id', 'party_id']


appbuilder.add_api(PartyAdditionalNamePartyJoinRestApi)


class PartyIdentificationPartyJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(party_identification_party_join)
    include_columns = ['party_identification_id', 'party_id']


appbuilder.add_api(PartyIdentificationPartyJoinRestApi)


class PartyIdentificationPartyRoleJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(party_identification_party_role_join)
    include_columns = ['party_identification_id', 'party_role_id']


appbuilder.add_api(PartyIdentificationPartyRoleJoinRestApi)


class PartyPrimaryAccountJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(party_primary_account_join)
    include_columns = ['party_id', 'account_id']


appbuilder.add_api(PartyPrimaryAccountJoinRestApi)


class PartyRelatedPartyPartyJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(party_related_party_party_join)
    include_columns = ['party_related_party_id', 'party_id']


appbuilder.add_api(PartyRelatedPartyPartyJoinRestApi)


class PartyRelatedPartyPartyRelationshipTypeJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(party_related_party_party_relationship_type_join)
    include_columns = ['party_related_party_id', 'party_relationship_type_id']


appbuilder.add_api(PartyRelatedPartyPartyRelationshipTypeJoinRestApi)


class PartyRelatedPartyRelatedPartyJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(party_related_party_related_party_join)
    include_columns = ['party_related_party_id', 'party_id']


appbuilder.add_api(PartyRelatedPartyRelatedPartyJoinRestApi)


class PartyRolePartyJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(party_role_party_join)
    include_columns = ['party_role_id', 'party_id']


appbuilder.add_api(PartyRolePartyJoinRestApi)


class PartyWebAddrPartyJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(party_web_addr_party_join)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'party_web_addr_id', 'party_id', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(PartyWebAddrPartyJoinRestApi)


class PartyWebAddrPartyRoleJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(party_web_addr_party_role_join)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'party_web_addr_id', 'party_role_id', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(PartyWebAddrPartyRoleJoinRestApi)


class PayGatAutLogPayGatIntTypJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(pay_gat_aut_log_pay_gat_int_typ_join)
    include_columns = ['payment_gateway_authorization_log_id', 'payment_gateway_interaction_type_id']


appbuilder.add_api(PayGatAutLogPayGatIntTypJoinRestApi)


class PayGatAutRevLogPayAutRevJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(pay_gat_aut_rev_log_pay_aut_rev_join)
    include_columns = ['payment_gateway_auth_reversal_log_id', 'payment_authorization_reversal_id']


appbuilder.add_api(PayGatAutRevLogPayAutRevJoinRestApi)


class PayGatAutRevLogPayGatIntTypJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(pay_gat_aut_rev_log_pay_gat_int_typ_join)
    include_columns = ['payment_gateway_auth_reversal_log_id', 'payment_gateway_interaction_type_id']


appbuilder.add_api(PayGatAutRevLogPayGatIntTypJoinRestApi)


class PayGatIntLogPayGatIntTypJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(pay_gat_int_log_pay_gat_int_typ_join)
    include_columns = ['payment_gateway_interaction_log_id', 'payment_gateway_interaction_type_id']


appbuilder.add_api(PayGatIntLogPayGatIntTypJoinRestApi)


class PayGatPayLogPayGatIntTypJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(pay_gat_pay_log_pay_gat_int_typ_join)
    include_columns = ['payment_gateway_payment_log_id', 'payment_gateway_interaction_type_id']


appbuilder.add_api(PayGatPayLogPayGatIntTypJoinRestApi)


class PaymentAccountJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_account_join)
    include_columns = ['payment_id', 'account_id']


appbuilder.add_api(PaymentAccountJoinRestApi)


class PaymentAllocationRelatedPaymentAllocationJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_allocation_related_payment_allocation_join)
    include_columns = ['payment_allocation_id_left', 'payment_allocation_id_right']


appbuilder.add_api(PaymentAllocationRelatedPaymentAllocationJoinRestApi)


class PaymentApplicationPaymentJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_application_payment_join)
    include_columns = ['payment_application_id', 'payment_id']


appbuilder.add_api(PaymentApplicationPaymentJoinRestApi)


class PaymentAuthorizationPaymentGatewayJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_authorization_payment_gateway_join)
    include_columns = ['payment_authorization_id', 'payment_gateway_id']


appbuilder.add_api(PaymentAuthorizationPaymentGatewayJoinRestApi)


class PaymentAuthorizationPaymentGatewayResultJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_authorization_payment_gateway_result_join)
    include_columns = ['payment_authorization_id', 'payment_gateway_result_code_id']


appbuilder.add_api(PaymentAuthorizationPaymentGatewayResultJoinRestApi)


class PaymentAuthorizationPaymentGroupJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_authorization_payment_group_join)
    include_columns = ['payment_authorization_id', 'payment_group_id']


appbuilder.add_api(PaymentAuthorizationPaymentGroupJoinRestApi)


class PaymentAuthorizationPaymentMethodJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_authorization_payment_method_join)
    include_columns = ['payment_authorization_id', 'payment_method_id']


appbuilder.add_api(PaymentAuthorizationPaymentMethodJoinRestApi)


class PaymentAuthorizationReversalCapturePaymentJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_authorization_reversal_capture_payment_join)
    include_columns = ['payment_authorization_reversal_id', 'capture_payment_capture_payment_id']


appbuilder.add_api(PaymentAuthorizationReversalCapturePaymentJoinRestApi)


class PaymentAuthorizationReversalPaymentAuthorizationJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_authorization_reversal_payment_authorization_join)
    include_columns = ['payment_authorization_reversal_id', 'payment_authorization_id']


appbuilder.add_api(PaymentAuthorizationReversalPaymentAuthorizationJoinRestApi)


class PaymentAuthorizationReversalPaymentGatewayResultJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_authorization_reversal_payment_gateway_result_join)
    include_columns = ['payment_authorization_reversal_id', 'payment_gateway_result_code_id']


appbuilder.add_api(PaymentAuthorizationReversalPaymentGatewayResultJoinRestApi)


class PaymentAuthorizationSalesOrderPaymentSummaryJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_authorization_sales_order_payment_summary_join)
    include_columns = ['payment_authorization_id', 'sales_order_payment_summary_id']


appbuilder.add_api(PaymentAuthorizationSalesOrderPaymentSummaryJoinRestApi)


class PaymentCardPaymentMethodTypeJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_card_payment_method_type_join)
    include_columns = ['payment_card_id', 'payment_method_type_id']


appbuilder.add_api(PaymentCardPaymentMethodTypeJoinRestApi)


class PaymentCreditMemoAllocationRelatedPaymentAllocationJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_credit_memo_allocation_related_payment_allocation_join)
    include_columns = ['payment_credit_memo_allocation_id', 'payment_allocation_id']


appbuilder.add_api(PaymentCreditMemoAllocationRelatedPaymentAllocationJoinRestApi)


class PaymentCreditMemoApplicationPaymentJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_credit_memo_application_payment_join)
    include_columns = ['payment_credit_memo_application_id', 'payment_id']


appbuilder.add_api(PaymentCreditMemoApplicationPaymentJoinRestApi)


class PaymentGatewayAuthReversalLogPaymentGatewayResultJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_gateway_auth_reversal_log_payment_gateway_result_join)
    include_columns = ['payment_gateway_auth_reversal_log_id', 'payment_gateway_result_code_id']


appbuilder.add_api(PaymentGatewayAuthReversalLogPaymentGatewayResultJoinRestApi)


class PaymentGatewayAuthorizationLogPaymentAuthorizationJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_gateway_authorization_log_payment_authorization_join)
    include_columns = ['payment_gateway_authorization_log_id', 'payment_authorization_id']


appbuilder.add_api(PaymentGatewayAuthorizationLogPaymentAuthorizationJoinRestApi)


class PaymentGatewayAuthorizationLogPaymentGatewayResultJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_gateway_authorization_log_payment_gateway_result_join)
    include_columns = ['payment_gateway_authorization_log_id', 'payment_gateway_result_code_id']


appbuilder.add_api(PaymentGatewayAuthorizationLogPaymentGatewayResultJoinRestApi)


class PaymentGatewayInteractionLogPaymentGatewayResultJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_gateway_interaction_log_payment_gateway_result_join)
    include_columns = ['payment_gateway_interaction_log_id', 'payment_gateway_result_code_id']


appbuilder.add_api(PaymentGatewayInteractionLogPaymentGatewayResultJoinRestApi)


class PaymentGatewayPaymentGatewayProviderJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_gateway_payment_gateway_provider_join)
    include_columns = ['payment_gateway_id', 'payment_gateway_provider_id']


appbuilder.add_api(PaymentGatewayPaymentGatewayProviderJoinRestApi)


class PaymentGatewayPaymentLogPaymentGatewayResultJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_gateway_payment_log_payment_gateway_result_join)
    include_columns = ['payment_gateway_payment_log_id', 'payment_gateway_result_code_id']


appbuilder.add_api(PaymentGatewayPaymentLogPaymentGatewayResultJoinRestApi)


class PaymentGatewayPaymentLogPaymentJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_gateway_payment_log_payment_join)
    include_columns = ['payment_gateway_payment_log_id', 'payment_id']


appbuilder.add_api(PaymentGatewayPaymentLogPaymentJoinRestApi)


class PaymentInternalBusinesUnitJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_internal_busines_unit_join)
    include_columns = ['payment_id', 'internal_busines_unit_id']


appbuilder.add_api(PaymentInternalBusinesUnitJoinRestApi)


class PaymentInvoiceAllocationPaymentInvoiceApplicationJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_invoice_allocation_payment_invoice_application_join)
    include_columns = ['payment_invoice_allocation_id', 'payment_invoice_application_id']


appbuilder.add_api(PaymentInvoiceAllocationPaymentInvoiceApplicationJoinRestApi)


class PaymentInvoiceAllocationRelatedPaymentAllocationJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_invoice_allocation_related_payment_allocation_join)
    include_columns = ['payment_invoice_allocation_id', 'payment_allocation_id']


appbuilder.add_api(PaymentInvoiceAllocationRelatedPaymentAllocationJoinRestApi)


class PaymentInvoiceApplicationPaymentJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_invoice_application_payment_join)
    include_columns = ['payment_invoice_application_id', 'payment_id']


appbuilder.add_api(PaymentInvoiceApplicationPaymentJoinRestApi)


class PaymentLatestGatewayResultCodeJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_latest_gateway_result_code_join)
    include_columns = ['payment_id', 'payment_gateway_result_code_id']


appbuilder.add_api(PaymentLatestGatewayResultCodeJoinRestApi)


class PaymentMethodPaymentMethodTypeJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_method_payment_method_type_join)
    include_columns = ['payment_method_id', 'payment_method_type_id']


appbuilder.add_api(PaymentMethodPaymentMethodTypeJoinRestApi)


class PaymentPaymentGatewayJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_payment_gateway_join)
    include_columns = ['payment_id', 'payment_gateway_id']


appbuilder.add_api(PaymentPaymentGatewayJoinRestApi)


class PaymentPaymentGroupJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_payment_group_join)
    include_columns = ['payment_id', 'payment_group_id']


appbuilder.add_api(PaymentPaymentGroupJoinRestApi)


class PaymentPaymentMethodJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_payment_method_join)
    include_columns = ['payment_id', 'payment_method_id']


appbuilder.add_api(PaymentPaymentMethodJoinRestApi)


class PaymentPaymentTreatmentJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_payment_treatment_join)
    include_columns = ['payment_id', 'payment_treatment_id']


appbuilder.add_api(PaymentPaymentTreatmentJoinRestApi)


class PaymentSalesOrderPaymentSummaryJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_sales_order_payment_summary_join)
    include_columns = ['payment_id', 'sales_order_payment_summary_id']


appbuilder.add_api(PaymentSalesOrderPaymentSummaryJoinRestApi)


class PaymentTreatmentPaymentPolicyJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_treatment_payment_policy_join)
    include_columns = ['payment_treatment_id', 'payment_policy_id']


appbuilder.add_api(PaymentTreatmentPaymentPolicyJoinRestApi)


class PaymentTreatmentPaymentTreatmentMethodJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(payment_treatment_payment_treatment_method_join)
    include_columns = ['payment_treatment_id', 'payment_treatment_method_id']


appbuilder.add_api(PaymentTreatmentPaymentTreatmentMethodJoinRestApi)


class ProductRestApi(ModelRestApi):
    datamodel = SQLAInterface(product)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'product_category_id', 'rating', 'default_variant', 'charge_taxes', 'tax_clas', 'manufacturer_name', 'model_year', 'model_number', 'quantity_schedule_type', 'disposal_type', 'minimum_advertisement_amount', 'is_back_ordered', 'valid_for_period_count', 'is_worker_discount_allowed', 'allow_partial_refund', 'is_weight_entry_required', 'is_quantity_entry_required', 'is_serialized', 'reward_program_points_count', 'revenue_installment_period', 'is_auto_provisionable', 'is_coupon_redemption_allowed', 'is_sellable_independently', 'can_use_revenue_schedule', 'is_intellectual_property_protected', 'is_customer_discount_allowed', 'product_state', 'brand_grade', 'quantity_installment_count', 'required_deposit_amount', 'revenue_schedule_type', 'is_pre_orderable', 'requires_invididual_unit_pricing', 'standard_warranty_length_month', 'can_use_quantity_schedule', 'is_installable', 'is_rain_check_allowed', 'minimum_advertisement_amount_start_date', 'maximum_order_quantity_count', 'is_multiple_coupons_allowed', 'allow_customer_return', 'm_sr_pamount', 'external_source_record', 'is_sellable', 'valid_to_date', 'price_charge_type', 'is_partner_discount_allowed', 'revenue_installment_count', 'product_sku', 'quantity_installment_period', 'is_manual_price_entry_required', 'is_sellable_without_price', 'gl_account_code', 'is_returnable', 'display_url', 'version_number', 'lot_identifier', 'valid_from_date', 'stock_ledger_valuation_amount', 'is_dynamic_bundle', 'is_quality_verification_required', 'required_deposit_percentage', 'is_foodstamp_payment_allowed', 'minimum_order_quantity_count', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(ProductRestApi)


class ProductAttributeValueAttributeValueJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(product_attribute_value_attribute_value_join)
    include_columns = ['product_attribute_value_id', 'attribute_value_id']


appbuilder.add_api(ProductAttributeValueAttributeValueJoinRestApi)


class ProductCatalogTranslationProductCatalogJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(product_catalog_translation_product_catalog_join)
    include_columns = ['product_catalog_translation_id', 'product_catalog_id']


appbuilder.add_api(ProductCatalogTranslationProductCatalogJoinRestApi)


class ProductCategoryAttributeSetProductCategoryJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(product_category_attribute_set_product_category_join)
    include_columns = ['product_category_attribute_set_id', 'product_category_id']


appbuilder.add_api(ProductCategoryAttributeSetProductCategoryJoinRestApi)


class ProductCategoryParentCategoryJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(product_category_parent_category_join)
    include_columns = ['product_category_id_left', 'product_category_id_right']


appbuilder.add_api(ProductCategoryParentCategoryJoinRestApi)


class ProductCategoryProductCatalogJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(product_category_product_catalog_join)
    include_columns = ['product_category_id', 'product_catalog_id']


appbuilder.add_api(ProductCategoryProductCatalogJoinRestApi)


class ProductCategoryProductProductCategoryJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(product_category_product_product_category_join)
    include_columns = ['product_category_product_id', 'product_category_id']


appbuilder.add_api(ProductCategoryProductProductCategoryJoinRestApi)


class ProductCategoryTranslationProductCategoryJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(product_category_translation_product_category_join)
    include_columns = ['product_category_translation_id', 'product_category_id']


appbuilder.add_api(ProductCategoryTranslationProductCategoryJoinRestApi)


class ProductImageTranslationProductImageJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(product_image_translation_product_image_join)
    include_columns = ['product_image_translation_id', 'product_image_id']


appbuilder.add_api(ProductImageTranslationProductImageJoinRestApi)


class ProductRelatedProductProductRelationshipTypeJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(product_related_product_product_relationship_type_join)
    include_columns = ['product_related_product_id', 'product_relationship_type_id']


appbuilder.add_api(ProductRelatedProductProductRelationshipTypeJoinRestApi)


class ProductRelatedProductSalesOrderProduct1JoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(product_related_product_sales_order_product1_join)
    include_columns = ['product_related_product_id', 'sales_order_product_id']


appbuilder.add_api(ProductRelatedProductSalesOrderProduct1JoinRestApi)


class ProductRelatedProductSalesOrderProduct2JoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(product_related_product_sales_order_product2_join)
    include_columns = ['product_related_product_id', 'sales_order_product_id']


appbuilder.add_api(ProductRelatedProductSalesOrderProduct2JoinRestApi)


class RefundAllocationRefundPaymentJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(refund_allocation_refund_payment_join)
    include_columns = ['refund_allocation_id', 'refund_payment_id']


appbuilder.add_api(RefundAllocationRefundPaymentJoinRestApi)


class RefundAllocationRelatedRefundAllocationJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(refund_allocation_related_refund_allocation_join)
    include_columns = ['refund_allocation_id_left', 'refund_allocation_id_right']


appbuilder.add_api(RefundAllocationRelatedRefundAllocationJoinRestApi)


class RefundCreditMemoAllocationRefundPaymentJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(refund_credit_memo_allocation_refund_payment_join)
    include_columns = ['refund_credit_memo_allocation_id', 'refund_payment_id']


appbuilder.add_api(RefundCreditMemoAllocationRefundPaymentJoinRestApi)


class RefundCreditMemoAllocationRelatedRefundAllocationJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(refund_credit_memo_allocation_related_refund_allocation_join)
    include_columns = ['refund_credit_memo_allocation_id', 'refund_allocation_id']


appbuilder.add_api(RefundCreditMemoAllocationRelatedRefundAllocationJoinRestApi)


class RefundPaymentAccountJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(refund_payment_account_join)
    include_columns = ['refund_payment_id', 'account_id']


appbuilder.add_api(RefundPaymentAccountJoinRestApi)


class RefundPaymentAllocationCapturePaymentJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(refund_payment_allocation_capture_payment_join)
    include_columns = ['refund_payment_allocation_id', 'capture_payment_capture_payment_id']


appbuilder.add_api(RefundPaymentAllocationCapturePaymentJoinRestApi)


class RefundPaymentAllocationRefundPaymentJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(refund_payment_allocation_refund_payment_join)
    include_columns = ['refund_payment_allocation_id', 'refund_payment_id']


appbuilder.add_api(RefundPaymentAllocationRefundPaymentJoinRestApi)


class RefundPaymentAllocationRelatedRefundAllocationJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(refund_payment_allocation_related_refund_allocation_join)
    include_columns = ['refund_payment_allocation_id', 'refund_allocation_id']


appbuilder.add_api(RefundPaymentAllocationRelatedRefundAllocationJoinRestApi)


class RefundPaymentInternalBusinesUnitJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(refund_payment_internal_busines_unit_join)
    include_columns = ['refund_payment_id', 'internal_busines_unit_id']


appbuilder.add_api(RefundPaymentInternalBusinesUnitJoinRestApi)


class RefundPaymentLatestGatewayResultCodeJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(refund_payment_latest_gateway_result_code_join)
    include_columns = ['refund_payment_id', 'payment_gateway_result_code_id']


appbuilder.add_api(RefundPaymentLatestGatewayResultCodeJoinRestApi)


class RefundPaymentPaymentGatewayJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(refund_payment_payment_gateway_join)
    include_columns = ['refund_payment_id', 'payment_gateway_id']


appbuilder.add_api(RefundPaymentPaymentGatewayJoinRestApi)


class RefundPaymentPaymentGroupJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(refund_payment_payment_group_join)
    include_columns = ['refund_payment_id', 'payment_group_id']


appbuilder.add_api(RefundPaymentPaymentGroupJoinRestApi)


class RefundPaymentPaymentMethodJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(refund_payment_payment_method_join)
    include_columns = ['refund_payment_id', 'payment_method_id']


appbuilder.add_api(RefundPaymentPaymentMethodJoinRestApi)


class RefundPaymentPaymentTreatmentJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(refund_payment_payment_treatment_join)
    include_columns = ['refund_payment_id', 'payment_treatment_id']


appbuilder.add_api(RefundPaymentPaymentTreatmentJoinRestApi)


class RefundPaymentSalesOrderPaymentSummaryJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(refund_payment_sales_order_payment_summary_join)
    include_columns = ['refund_payment_id', 'sales_order_payment_summary_id']


appbuilder.add_api(RefundPaymentSalesOrderPaymentSummaryJoinRestApi)


class SalOrdProReaSalOrdProReaCatJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sal_ord_pro_rea_sal_ord_pro_rea_cat_join)
    include_columns = ['sales_order_product_reason_id', 'sales_order_product_reason_category_id']


appbuilder.add_api(SalOrdProReaSalOrdProReaCatJoinRestApi)


class SalesChannelSalesChannelTypeJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_channel_sales_channel_type_join)
    include_columns = ['sales_channel_id', 'sales_channel_type_id']


appbuilder.add_api(SalesChannelSalesChannelTypeJoinRestApi)


class SalesOrderBillToAccountJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_bill_to_account_join)
    include_columns = ['sales_order_id', 'account_id']


appbuilder.add_api(SalesOrderBillToAccountJoinRestApi)


class SalesOrderBillToAddrJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_bill_to_addr_join)
    include_columns = ['sales_order_id', 'contact_point_addr_id']


appbuilder.add_api(SalesOrderBillToAddrJoinRestApi)


class SalesOrderBillToContactJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_bill_to_contact_join)
    include_columns = ['sales_order_id', 'account_contact_id']


appbuilder.add_api(SalesOrderBillToContactJoinRestApi)


class SalesOrderBillToEmailJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_bill_to_email_join)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'sales_order_id', 'contact_point_email_id', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(SalesOrderBillToEmailJoinRestApi)


class SalesOrderBillToPhoneNumberJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_bill_to_phone_number_join)
    include_columns = ['sales_order_id', 'contact_point_phone_id']


appbuilder.add_api(SalesOrderBillToPhoneNumberJoinRestApi)


class SalesOrderChangeLogChangeSalesOrderJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_change_log_change_sales_order_join)
    include_columns = ['sales_order_change_log_id', 'sales_order_id']


appbuilder.add_api(SalesOrderChangeLogChangeSalesOrderJoinRestApi)


class SalesOrderChangeLogChangeSalesOrderProductJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_change_log_change_sales_order_product_join)
    include_columns = ['sales_order_change_log_id', 'sales_order_product_id']


appbuilder.add_api(SalesOrderChangeLogChangeSalesOrderProductJoinRestApi)


class SalesOrderChangeLogRelatedSalesOrderJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_change_log_related_sales_order_join)
    include_columns = ['sales_order_change_log_id', 'sales_order_id']


appbuilder.add_api(SalesOrderChangeLogRelatedSalesOrderJoinRestApi)


class SalesOrderChangeLogRelatedSalesOrderProductJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_change_log_related_sales_order_product_join)
    include_columns = ['sales_order_change_log_id', 'sales_order_product_id']


appbuilder.add_api(SalesOrderChangeLogRelatedSalesOrderProductJoinRestApi)


class SalesOrderDeliveryGroupAccountContactJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_delivery_group_account_contact_join)
    include_columns = ['sales_order_delivery_group_id', 'account_contact_id']


appbuilder.add_api(SalesOrderDeliveryGroupAccountContactJoinRestApi)


class SalesOrderDeliveryGroupContactPointAddrJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_delivery_group_contact_point_addr_join)
    include_columns = ['sales_order_delivery_group_id', 'contact_point_addr_id']


appbuilder.add_api(SalesOrderDeliveryGroupContactPointAddrJoinRestApi)


class SalesOrderDeliveryGroupOrderDeliveryMethodJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_delivery_group_order_delivery_method_join)
    include_columns = ['sales_order_delivery_group_id', 'order_delivery_method_id']


appbuilder.add_api(SalesOrderDeliveryGroupOrderDeliveryMethodJoinRestApi)


class SalesOrderDeliveryGroupOriginalDeliveryGroupJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_delivery_group_original_delivery_group_join)
    include_columns = ['sales_order_delivery_group_id_left', 'sales_order_delivery_group_id_right']


appbuilder.add_api(SalesOrderDeliveryGroupOriginalDeliveryGroupJoinRestApi)


class SalesOrderDeliveryGroupSalesOrderDeliveryStateJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_delivery_group_sales_order_delivery_state_join)
    include_columns = ['sales_order_delivery_group_id', 'sales_order_delivery_state_id']


appbuilder.add_api(SalesOrderDeliveryGroupSalesOrderDeliveryStateJoinRestApi)


class SalesOrderDeliveryGroupSalesOrderJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_delivery_group_sales_order_join)
    include_columns = ['sales_order_delivery_group_id', 'sales_order_id']


appbuilder.add_api(SalesOrderDeliveryGroupSalesOrderJoinRestApi)


class SalesOrderInternalBusinesUnitJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_internal_busines_unit_join)
    include_columns = ['sales_order_id', 'internal_busines_unit_id']


appbuilder.add_api(SalesOrderInternalBusinesUnitJoinRestApi)


class SalesOrderOriginalOrderJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_original_order_join)
    include_columns = ['sales_order_id_left', 'sales_order_id_right']


appbuilder.add_api(SalesOrderOriginalOrderJoinRestApi)


class SalesOrderPaymentMethodJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_payment_method_join)
    include_columns = ['sales_order_id', 'payment_method_id']


appbuilder.add_api(SalesOrderPaymentMethodJoinRestApi)


class SalesOrderPaymentSummaryPaymentMethodJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_payment_summary_payment_method_join)
    include_columns = ['sales_order_payment_summary_id', 'payment_method_id']


appbuilder.add_api(SalesOrderPaymentSummaryPaymentMethodJoinRestApi)


class SalesOrderPaymentSummarySalesOrderJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_payment_summary_sales_order_join)
    include_columns = ['sales_order_payment_summary_id', 'sales_order_id']


appbuilder.add_api(SalesOrderPaymentSummarySalesOrderJoinRestApi)


class SalesOrderPriceAdjustmentSalesOrderJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_price_adjustment_sales_order_join)
    include_columns = ['sales_order_price_adjustment_id', 'sales_order_id']


appbuilder.add_api(SalesOrderPriceAdjustmentSalesOrderJoinRestApi)


class SalesOrderProductGroupSalesOrderProductGroupTypeJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_product_group_sales_order_product_group_type_join)
    include_columns = ['sales_order_product_group_id', 'sales_order_product_group_type_id']


appbuilder.add_api(SalesOrderProductGroupSalesOrderProductGroupTypeJoinRestApi)


class SalesOrderProductListPriceTermUoMJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_product_list_price_term_uo_m_join)
    include_columns = ['sales_order_product_id', 'product_validity_time_period_uo_m_id']


appbuilder.add_api(SalesOrderProductListPriceTermUoMJoinRestApi)


class SalesOrderProductOriginalOrderProductJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_product_original_order_product_join)
    include_columns = ['sales_order_product_id_left', 'sales_order_product_id_right']


appbuilder.add_api(SalesOrderProductOriginalOrderProductJoinRestApi)


class SalesOrderProductPriceBookEntryJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_product_price_book_entry_join)
    include_columns = ['sales_order_product_id', 'price_book_entry_id']


appbuilder.add_api(SalesOrderProductPriceBookEntryJoinRestApi)


class SalesOrderProductSalesOrderDeliveryGroupJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_product_sales_order_delivery_group_join)
    include_columns = ['sales_order_product_id', 'sales_order_delivery_group_id']


appbuilder.add_api(SalesOrderProductSalesOrderDeliveryGroupJoinRestApi)


class SalesOrderProductSalesOrderJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_product_sales_order_join)
    include_columns = ['sales_order_product_id', 'sales_order_id']


appbuilder.add_api(SalesOrderProductSalesOrderJoinRestApi)


class SalesOrderProductSalesOrderProductReasonJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_product_sales_order_product_reason_join)
    include_columns = ['sales_order_product_id', 'sales_order_product_reason_id']


appbuilder.add_api(SalesOrderProductSalesOrderProductReasonJoinRestApi)


class SalesOrderProductSalesOrderProductStateJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_product_sales_order_product_state_join)
    include_columns = ['sales_order_product_id', 'sales_order_product_state_id']


appbuilder.add_api(SalesOrderProductSalesOrderProductStateJoinRestApi)


class SalesOrderProductSellerAccountJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_product_seller_account_join)
    include_columns = ['sales_order_product_id', 'account_id']


appbuilder.add_api(SalesOrderProductSellerAccountJoinRestApi)


class SalesOrderProductShippingAddrJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_product_shipping_addr_join)
    include_columns = ['sales_order_product_id', 'contact_point_addr_id']


appbuilder.add_api(SalesOrderProductShippingAddrJoinRestApi)


class SalesOrderProductShippingEmailJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_product_shipping_email_join)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'sales_order_product_id', 'contact_point_email_id', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(SalesOrderProductShippingEmailJoinRestApi)


class SalesOrderProductShippingPhoneJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_product_shipping_phone_join)
    include_columns = ['sales_order_product_id', 'contact_point_phone_id']


appbuilder.add_api(SalesOrderProductShippingPhoneJoinRestApi)


class SalesOrderProductSubscriptionTermUnitJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_product_subscription_term_unit_join)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'sales_order_product_id', 'product_validity_time_period_uo_m_id', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(SalesOrderProductSubscriptionTermUnitJoinRestApi)


class SalesOrderProductTaxOriginalSalesOrderProductTaxJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_product_tax_original_sales_order_product_tax_join)
    include_columns = ['sales_order_product_tax_id_left', 'sales_order_product_tax_id_right']


appbuilder.add_api(SalesOrderProductTaxOriginalSalesOrderProductTaxJoinRestApi)


class SalesOrderProductTaxSalesOrderProductJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_product_tax_sales_order_product_join)
    include_columns = ['sales_order_product_tax_id', 'sales_order_product_id']


appbuilder.add_api(SalesOrderProductTaxSalesOrderProductJoinRestApi)


class SalesOrderRenewalTermJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_renewal_term_join)
    include_columns = ['sales_order_id', 'renewal_term_id']


appbuilder.add_api(SalesOrderRenewalTermJoinRestApi)


class SalesOrderSalesChannelJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_sales_channel_join)
    include_columns = ['sales_order_id', 'sales_channel_id']


appbuilder.add_api(SalesOrderSalesChannelJoinRestApi)


class SalesOrderSalesOrderConfirmationStateJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_sales_order_confirmation_state_join)
    include_columns = ['sales_order_id', 'sales_order_confirmation_state_id']


appbuilder.add_api(SalesOrderSalesOrderConfirmationStateJoinRestApi)


class SalesOrderSalesOrderStateJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_sales_order_state_join)
    include_columns = ['sales_order_id', 'sales_order_state_id']


appbuilder.add_api(SalesOrderSalesOrderStateJoinRestApi)


class SalesOrderSalesOrderTypeJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_sales_order_type_join)
    include_columns = ['sales_order_id', 'sales_order_type_id']


appbuilder.add_api(SalesOrderSalesOrderTypeJoinRestApi)


class SalesOrderSellerJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_seller_join)
    include_columns = ['sales_order_id', 'seller_id']


appbuilder.add_api(SalesOrderSellerJoinRestApi)


class SalesOrderShipToAddrJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_ship_to_addr_join)
    include_columns = ['sales_order_id', 'contact_point_addr_id']


appbuilder.add_api(SalesOrderShipToAddrJoinRestApi)


class SalesOrderShipToContactJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_ship_to_contact_join)
    include_columns = ['sales_order_id', 'account_contact_id']


appbuilder.add_api(SalesOrderShipToContactJoinRestApi)


class SalesOrderShipToEmailJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_ship_to_email_join)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'sales_order_id', 'contact_point_email_id', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(SalesOrderShipToEmailJoinRestApi)


class SalesOrderSoldToCustomerJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_sold_to_customer_join)
    include_columns = ['sales_order_id', 'customer_id']


appbuilder.add_api(SalesOrderSoldToCustomerJoinRestApi)


class SalesOrderUserDeviceSesionJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_user_device_sesion_join)
    include_columns = ['sales_order_id', 'device_user_sesion_id']


appbuilder.add_api(SalesOrderUserDeviceSesionJoinRestApi)


class SellerPartyJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(seller_party_join)
    include_columns = ['seller_id', 'party_id']


appbuilder.add_api(SellerPartyJoinRestApi)


class ServiceProductBrandJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(service_product_brand_join)
    include_columns = ['service_product_id', 'brand_id']


appbuilder.add_api(ServiceProductBrandJoinRestApi)


class ServiceProductPrimaryProductCategoryJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(service_product_primary_product_category_join)
    include_columns = ['service_product_id', 'product_category_id']


appbuilder.add_api(ServiceProductPrimaryProductCategoryJoinRestApi)


class ServiceProductPrimarySalesChannelJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(service_product_primary_sales_channel_join)
    include_columns = ['service_product_id', 'sales_channel_id']


appbuilder.add_api(ServiceProductPrimarySalesChannelJoinRestApi)


class ServiceProductServiceProviderAccountJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(service_product_service_provider_account_join)
    include_columns = ['service_product_id', 'account_id']


appbuilder.add_api(ServiceProductServiceProviderAccountJoinRestApi)


class ServiceProductValidForPeriodUoMJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(service_product_valid_for_period_uo_m_join)
    include_columns = ['service_product_id', 'product_validity_time_period_uo_m_id']


appbuilder.add_api(ServiceProductValidForPeriodUoMJoinRestApi)


class ShiProPriAdjTaxShiProPriAdjJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(shi_pro_pri_adj_tax_shi_pro_pri_adj_join)
    include_columns = ['shipment_product_price_adjustment_tax_id', 'shipment_product_price_adjustment_id']


appbuilder.add_api(ShiProPriAdjTaxShiProPriAdjJoinRestApi)


class ShipmentDocumentShipmentJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(shipment_document_shipment_join)
    include_columns = ['shipment_document_id', 'shipment_id']


appbuilder.add_api(ShipmentDocumentShipmentJoinRestApi)


class ShipmentPackageShipmentJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(shipment_package_shipment_join)
    include_columns = ['shipment_package_id', 'shipment_id']


appbuilder.add_api(ShipmentPackageShipmentJoinRestApi)


class ShipmentProductPriceAdjustmentShipmentProductJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(shipment_product_price_adjustment_shipment_product_join)
    include_columns = ['shipment_product_price_adjustment_id', 'shipment_product_id']


appbuilder.add_api(ShipmentProductPriceAdjustmentShipmentProductJoinRestApi)


class ShipmentProductSalesOrderProductJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(shipment_product_sales_order_product_join)
    include_columns = ['shipment_product_id', 'sales_order_product_id']


appbuilder.add_api(ShipmentProductSalesOrderProductJoinRestApi)


class ShipmentProductShipmentJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(shipment_product_shipment_join)
    include_columns = ['shipment_product_id', 'shipment_id']


appbuilder.add_api(ShipmentProductShipmentJoinRestApi)


class ShipmentProductShipmentPackageJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(shipment_product_shipment_package_join)
    include_columns = ['shipment_product_id', 'shipment_package_id']


appbuilder.add_api(ShipmentProductShipmentPackageJoinRestApi)


class ShipmentSalesOrderDeliveryGroupJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(shipment_sales_order_delivery_group_join)
    include_columns = ['shipment_id', 'sales_order_delivery_group_id']


appbuilder.add_api(ShipmentSalesOrderDeliveryGroupJoinRestApi)


class ShipmentSalesOrderJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(shipment_sales_order_join)
    include_columns = ['shipment_id', 'sales_order_id']


appbuilder.add_api(ShipmentSalesOrderJoinRestApi)


class ShipmentShipToAddrJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(shipment_ship_to_addr_join)
    include_columns = ['shipment_id', 'contact_point_addr_id']


appbuilder.add_api(ShipmentShipToAddrJoinRestApi)


class ShipmentShipmentStateJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(shipment_shipment_state_join)
    include_columns = ['shipment_id', 'shipment_state_id']


appbuilder.add_api(ShipmentShipmentStateJoinRestApi)


class SupplierPartyJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(supplier_party_join)
    include_columns = ['supplier_id', 'party_id']


appbuilder.add_api(SupplierPartyJoinRestApi)


class UncategorizedPartyPrimaryAccountJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(uncategorized_party_primary_account_join)
    include_columns = ['account_id', 'uncategorized_party_id']


appbuilder.add_api(UncategorizedPartyPrimaryAccountJoinRestApi)


class AccountContactIndividualJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(account_contact_individual_join)
    include_columns = ['account_contact_id', 'individual_id']


appbuilder.add_api(AccountContactIndividualJoinRestApi)


class BundleProductMasterProductJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(bundle_product_master_product_join)
    include_columns = ['bundle_product_id', 'product_id']


appbuilder.add_api(BundleProductMasterProductJoinRestApi)


class EducationRestApi(ModelRestApi):
    datamodel = SQLAInterface(education)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'individual_id', 'qualification', 'qual_clas', 'verified', 'verification_code', 'verified_by', 'verification_date', 'verification_doc', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(EducationRestApi)


class GoodsProductMasterProductJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(goods_product_master_product_join)
    include_columns = ['goods_product_id', 'product_id']


appbuilder.add_api(GoodsProductMasterProductJoinRestApi)


class IndividualPrimaryAccountJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(individual_primary_account_join)
    include_columns = ['individual_id', 'account_id']


appbuilder.add_api(IndividualPrimaryAccountJoinRestApi)


class IndividualPrimaryHouseholdJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(individual_primary_household_join)
    include_columns = ['individual_id', 'household_id']


appbuilder.add_api(IndividualPrimaryHouseholdJoinRestApi)


class JobIndividualRestApi(ModelRestApi):
    datamodel = SQLAInterface(job_individual)
    include_columns = ['job', 'individual']


appbuilder.add_api(JobIndividualRestApi)


class LocationRestApi(ModelRestApi):
    datamodel = SQLAInterface(location)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'individual_id', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(LocationRestApi)


class OrderDeliveryMethodProductJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(order_delivery_method_product_join)
    include_columns = ['order_delivery_method_id', 'product_id']


appbuilder.add_api(OrderDeliveryMethodProductJoinRestApi)


class PersonLanguageIndividualJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(person_language_individual_join)
    include_columns = ['individual_id', 'person_language_id']


appbuilder.add_api(PersonLanguageIndividualJoinRestApi)


class PersonLifeEventIndividualJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(person_life_event_individual_join)
    include_columns = ['person_life_event_id', 'individual_id']


appbuilder.add_api(PersonLifeEventIndividualJoinRestApi)


class PortalRestApi(ModelRestApi):
    datamodel = SQLAInterface(portal)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'portal_url', 'is_primary', 'portal_state', 'individual_id', 'has_custom_domain', 'domain', 'header_text', 'slug', 'automatic_fulfillment_digital_products', 'default_digital_max_downloads', 'default_digital_url_valid_days', 'default_mail_sender_name', 'default_mail_sender_addr', 'fulfillment_auto_approve', 'fulfillment_allow_unpaid', 'reserve_stock_duration_anonymous_user', 'reserve_stock_duration_authenticated_user', 'limit_quantity_per_checkout', 'gift_card_expiry_type', 'gift_card_expiry_period_type', 'gift_card_expiry_period', 'charge_taxes_on_shipping', 'include_taxes_in_prices', 'display_gros_prices', 'language', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(PortalRestApi)


class PriceBookEntryProductJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(price_book_entry_product_join)
    include_columns = ['price_book_entry_id', 'product_id']


appbuilder.add_api(PriceBookEntryProductJoinRestApi)


class ProductAttributeSetProductJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(product_attribute_set_product_join)
    include_columns = ['product_attribute_set_id', 'product_id']


appbuilder.add_api(ProductAttributeSetProductJoinRestApi)


class ProductAttributeValueProductJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(product_attribute_value_product_join)
    include_columns = ['product_attribute_value_id', 'product_id']


appbuilder.add_api(ProductAttributeValueProductJoinRestApi)


class ProductBrandJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(product_brand_join)
    include_columns = ['product_id', 'brand_id']


appbuilder.add_api(ProductBrandJoinRestApi)


class ProductCategoryProductProductJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(product_category_product_product_join)
    include_columns = ['product_category_product_id', 'product_id']


appbuilder.add_api(ProductCategoryProductProductJoinRestApi)


class ProductCollateralProductJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(product_collateral_product_join)
    include_columns = ['product_collateral_id', 'product_id']


appbuilder.add_api(ProductCollateralProductJoinRestApi)


class ProductImageProductJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(product_image_product_join)
    include_columns = ['product_image_id', 'product_id']


appbuilder.add_api(ProductImageProductJoinRestApi)


class ProductMasterProductJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(product_master_product_join)
    include_columns = ['product_id_left', 'product_id_right']


appbuilder.add_api(ProductMasterProductJoinRestApi)


class ProductPrimaryProductCategoryJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(product_primary_product_category_join)
    include_columns = ['product_id', 'product_category_id']


appbuilder.add_api(ProductPrimaryProductCategoryJoinRestApi)


class ProductPrimarySalesChannelJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(product_primary_sales_channel_join)
    include_columns = ['product_id', 'sales_channel_id']


appbuilder.add_api(ProductPrimarySalesChannelJoinRestApi)


class ProductRelatedProductChildProductJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(product_related_product_child_product_join)
    include_columns = ['product_related_product_id', 'product_id']


appbuilder.add_api(ProductRelatedProductChildProductJoinRestApi)


class ProductRelatedProductParentProductJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(product_related_product_parent_product_join)
    include_columns = ['product_related_product_id', 'product_id']


appbuilder.add_api(ProductRelatedProductParentProductJoinRestApi)


class ProductTranslationProductJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(product_translation_product_join)
    include_columns = ['product_translation_id', 'product_id']


appbuilder.add_api(ProductTranslationProductJoinRestApi)


class ProductValidForPeriodUoMJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(product_valid_for_period_uo_m_join)
    include_columns = ['product_id', 'product_validity_time_period_uo_m_id']


appbuilder.add_api(ProductValidForPeriodUoMJoinRestApi)


class ProfileRestApi(ModelRestApi):
    datamodel = SQLAInterface(profile)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'individual_id', 'import_addr', 'profile_username', 'profile_pasword', 'has_been_imported', 'import_data', 'import_date', 'profilesource_id', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(ProfileRestApi)


class SalesOrderProductProductJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(sales_order_product_product_join)
    include_columns = ['sales_order_product_id', 'product_id']


appbuilder.add_api(SalesOrderProductProductJoinRestApi)


class ServiceProductMasterProductJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(service_product_master_product_join)
    include_columns = ['service_product_id', 'product_id']


appbuilder.add_api(ServiceProductMasterProductJoinRestApi)


class ShipmentProductProductJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(shipment_product_product_join)
    include_columns = ['shipment_product_id', 'product_id']


appbuilder.add_api(ShipmentProductProductJoinRestApi)


class ShippingMethodProductJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(shipping_method_product_join)
    include_columns = ['shipping_method_id', 'product_id']


appbuilder.add_api(ShippingMethodProductJoinRestApi)


class UserSkillRestApi(ModelRestApi):
    datamodel = SQLAInterface(user_skill)
    include_columns = ['skills', 'user_details']


appbuilder.add_api(UserSkillRestApi)


class EducationIndividualJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(education_individual_join)
    include_columns = ['individual_id', 'education_id']


appbuilder.add_api(EducationIndividualJoinRestApi)


class PageRestApi(ModelRestApi):
    datamodel = SQLAInterface(page)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'portal_id', 'header', 'slug', 'page_type', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(PageRestApi)


class ResumeRestApi(ModelRestApi):
    datamodel = SQLAInterface(resume)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'individual_id', 'template', 'header', 'color', 'location_id', 'summary_text', 'has_been_generated', 'preferred', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(ResumeRestApi)


class SwarmRestApi(ModelRestApi):
    datamodel = SQLAInterface(swarm)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'portal_id', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(SwarmRestApi)


class SwarmIndividualRestApi(ModelRestApi):
    datamodel = SQLAInterface(swarm_individual)
    include_columns = ['swarm', 'individual']


appbuilder.add_api(SwarmIndividualRestApi)


class WorkHistoryRestApi(ModelRestApi):
    datamodel = SQLAInterface(work_history)
    include_columns = ['created_on', 'changed_on', 'name', 'code', 'description', 'id', 'employment_state', 'position_text', 'employer_addr_line3', 'occupation_text', 'employer_name', 'employer_addr_line4', 'employer_addr_line1', 'annual_income', 'employer_city_name', 'employer_addr_line2', 'employer_postal_code_text', 'employer_phone_number', 'resume_id', 'individual_id', 'created_by_fk', 'changed_by_fk']


appbuilder.add_api(WorkHistoryRestApi)


class WorkHistoryIndividualJoinRestApi(ModelRestApi):
    datamodel = SQLAInterface(work_history_individual_join)
    include_columns = ['individual_id', 'work_history_id']


appbuilder.add_api(WorkHistoryIndividualJoinRestApi)

