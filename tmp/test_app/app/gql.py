class Brandgraphql(graphene.ObjectType):
    brand = graphene.List(BrandObject)

class Accountgraphql(graphene.ObjectType):
    account = graphene.List(AccountObject)

class Apptablegraphql(graphene.ObjectType):
    app_table = graphene.List(AppTableObject)

class Accountcontactgraphql(graphene.ObjectType):
    account_contact = graphene.List(AccountContactObject)

class Appcolumngraphql(graphene.ObjectType):
    app_column = graphene.List(AppColumnObject)

class Accountcontactrolegraphql(graphene.ObjectType):
    account_contact_role = graphene.List(AccountContactRoleObject)

class Accountpartnergraphql(graphene.ObjectType):
    account_partner = graphene.List(AccountPartnerObject)

class Attributesettranslationgraphql(graphene.ObjectType):
    attribute_set_translation = graphene.List(AttributeSetTranslationObject)

class Attributetranslationgraphql(graphene.ObjectType):
    attribute_translation = graphene.List(AttributeTranslationObject)

class Apprelationshipgraphql(graphene.ObjectType):
    app_relationship = graphene.List(AppRelationshipObject)

class Attributevaluegraphql(graphene.ObjectType):
    attribute_value = graphene.List(AttributeValueObject)

class Attributevaluetranslationgraphql(graphene.ObjectType):
    attribute_value_translation = graphene.List(AttributeValueTranslationObject)

class Billingfrequencygraphql(graphene.ObjectType):
    billing_frequency = graphene.List(BillingFrequencyObject)

class Bundleproductgraphql(graphene.ObjectType):
    bundle_product = graphene.List(BundleProductObject)

class Capturepaymentgraphql(graphene.ObjectType):
    capture_payment = graphene.List(CapturePaymentObject)

class Competitorgraphql(graphene.ObjectType):
    competitor = graphene.List(CompetitorObject)

class Contactpointaddrgraphql(graphene.ObjectType):
    contact_point_addr = graphene.List(ContactPointAddrObject)

class Contactpointphonegraphql(graphene.ObjectType):
    contact_point_phone = graphene.List(ContactPointPhoneObject)

class Contactpointtypegraphql(graphene.ObjectType):
    contact_point_type = graphene.List(ContactPointTypeObject)

class Coupongraphql(graphene.ObjectType):
    coupon = graphene.List(CouponObject)

class Credittendergraphql(graphene.ObjectType):
    credit_tender = graphene.List(CreditTenderObject)

class Customergraphql(graphene.ObjectType):
    customer = graphene.List(CustomerObject)

class Customerstatehistorygraphql(graphene.ObjectType):
    customer_state_history = graphene.List(CustomerStateHistoryObject)

class Deviceusersesiongraphql(graphene.ObjectType):
    device_user_sesion = graphene.List(DeviceUserSesionObject)

class Goodsproductgraphql(graphene.ObjectType):
    goods_product = graphene.List(GoodsProductObject)

class Householdgraphql(graphene.ObjectType):
    household = graphene.List(HouseholdObject)

class Industrygraphql(graphene.ObjectType):
    industry = graphene.List(IndustryObject)

class Internalbusinesunitgraphql(graphene.ObjectType):
    internal_busines_unit = graphene.List(InternalBusinesUnitObject)

class Jobgraphql(graphene.ObjectType):
    job = graphene.List(JobObject)

class Leadgraphql(graphene.ObjectType):
    lead = graphene.List(LeadObject)

class Orderdeliverymethodgraphql(graphene.ObjectType):
    order_delivery_method = graphene.List(OrderDeliveryMethodObject)

class Partygraphql(graphene.ObjectType):
    party = graphene.List(PartyObject)

class Partyadditionalnamegraphql(graphene.ObjectType):
    party_additional_name = graphene.List(PartyAdditionalNameObject)

class Partyidentificationgraphql(graphene.ObjectType):
    party_identification = graphene.List(PartyIdentificationObject)

class Partyrelatedpartygraphql(graphene.ObjectType):
    party_related_party = graphene.List(PartyRelatedPartyObject)

class Partyrelationshiptypegraphql(graphene.ObjectType):
    party_relationship_type = graphene.List(PartyRelationshipTypeObject)

class Partyrolegraphql(graphene.ObjectType):
    party_role = graphene.List(PartyRoleObject)

class Partywebaddrgraphql(graphene.ObjectType):
    party_web_addr = graphene.List(PartyWebAddrObject)

class Paymentgraphql(graphene.ObjectType):
    payment = graphene.List(PaymentObject)

class Paymentallocationgraphql(graphene.ObjectType):
    payment_allocation = graphene.List(PaymentAllocationObject)

class Paymentapplicationgraphql(graphene.ObjectType):
    payment_application = graphene.List(PaymentApplicationObject)

class Paymentauthorizationgraphql(graphene.ObjectType):
    payment_authorization = graphene.List(PaymentAuthorizationObject)

class Paymentauthorizationreversalgraphql(graphene.ObjectType):
    payment_authorization_reversal = graphene.List(PaymentAuthorizationReversalObject)

class Paymentcardgraphql(graphene.ObjectType):
    payment_card = graphene.List(PaymentCardObject)

class Paymentcreditmemoallocationgraphql(graphene.ObjectType):
    payment_credit_memo_allocation = graphene.List(PaymentCreditMemoAllocationObject)

class Paymentcreditmemoapplicationgraphql(graphene.ObjectType):
    payment_credit_memo_application = graphene.List(PaymentCreditMemoApplicationObject)

class Paymentgatewaygraphql(graphene.ObjectType):
    payment_gateway = graphene.List(PaymentGatewayObject)

class Paymentgatewayauthreversalloggraphql(graphene.ObjectType):
    payment_gateway_auth_reversal_log = graphene.List(PaymentGatewayAuthReversalLogObject)

class Paymentgatewayauthorizationloggraphql(graphene.ObjectType):
    payment_gateway_authorization_log = graphene.List(PaymentGatewayAuthorizationLogObject)

class Paymentgatewayinteractionloggraphql(graphene.ObjectType):
    payment_gateway_interaction_log = graphene.List(PaymentGatewayInteractionLogObject)

class Paymentgatewayinteractiontypegraphql(graphene.ObjectType):
    payment_gateway_interaction_type = graphene.List(PaymentGatewayInteractionTypeObject)

class Paymentgatewaypaymentloggraphql(graphene.ObjectType):
    payment_gateway_payment_log = graphene.List(PaymentGatewayPaymentLogObject)

class Paymentgatewayprovidergraphql(graphene.ObjectType):
    payment_gateway_provider = graphene.List(PaymentGatewayProviderObject)

class Paymentgatewayresultcodegraphql(graphene.ObjectType):
    payment_gateway_result_code = graphene.List(PaymentGatewayResultCodeObject)

class Paymentgroupgraphql(graphene.ObjectType):
    payment_group = graphene.List(PaymentGroupObject)

class Paymentinvoiceallocationgraphql(graphene.ObjectType):
    payment_invoice_allocation = graphene.List(PaymentInvoiceAllocationObject)

class Paymentinvoiceapplicationgraphql(graphene.ObjectType):
    payment_invoice_application = graphene.List(PaymentInvoiceApplicationObject)

class Paymentmethodgraphql(graphene.ObjectType):
    payment_method = graphene.List(PaymentMethodObject)

class Paymentmethodtypegraphql(graphene.ObjectType):
    payment_method_type = graphene.List(PaymentMethodTypeObject)

class Paymentpolicygraphql(graphene.ObjectType):
    payment_policy = graphene.List(PaymentPolicyObject)

class Paymenttreatmentgraphql(graphene.ObjectType):
    payment_treatment = graphene.List(PaymentTreatmentObject)

class Paymenttreatmentmethodgraphql(graphene.ObjectType):
    payment_treatment_method = graphene.List(PaymentTreatmentMethodObject)

class Personlanguagegraphql(graphene.ObjectType):
    person_language = graphene.List(PersonLanguageObject)

class Personlifeeventgraphql(graphene.ObjectType):
    person_life_event = graphene.List(PersonLifeEventObject)

class Priceadjustmentgroupgraphql(graphene.ObjectType):
    price_adjustment_group = graphene.List(PriceAdjustmentGroupObject)

class Priceadjustmentmethodgraphql(graphene.ObjectType):
    price_adjustment_method = graphene.List(PriceAdjustmentMethodObject)

class Pricebookentrygraphql(graphene.ObjectType):
    price_book_entry = graphene.List(PriceBookEntryObject)

class Productattributesetgraphql(graphene.ObjectType):
    product_attribute_set = graphene.List(ProductAttributeSetObject)

class Productattributevaluegraphql(graphene.ObjectType):
    product_attribute_value = graphene.List(ProductAttributeValueObject)

class Productcataloggraphql(graphene.ObjectType):
    product_catalog = graphene.List(ProductCatalogObject)

class Productcatalogtranslationgraphql(graphene.ObjectType):
    product_catalog_translation = graphene.List(ProductCatalogTranslationObject)

class Productcategorygraphql(graphene.ObjectType):
    product_category = graphene.List(ProductCategoryObject)

class Productcategoryattributesetgraphql(graphene.ObjectType):
    product_category_attribute_set = graphene.List(ProductCategoryAttributeSetObject)

class Productcategoryproductgraphql(graphene.ObjectType):
    product_category_product = graphene.List(ProductCategoryProductObject)

class Productcategorytranslationgraphql(graphene.ObjectType):
    product_category_translation = graphene.List(ProductCategoryTranslationObject)

class Productcollateralgraphql(graphene.ObjectType):
    product_collateral = graphene.List(ProductCollateralObject)

class Productimagegraphql(graphene.ObjectType):
    product_image = graphene.List(ProductImageObject)

class Productimagetranslationgraphql(graphene.ObjectType):
    product_image_translation = graphene.List(ProductImageTranslationObject)

class Productrelatedproductgraphql(graphene.ObjectType):
    product_related_product = graphene.List(ProductRelatedProductObject)

class Productrelationshiptypegraphql(graphene.ObjectType):
    product_relationship_type = graphene.List(ProductRelationshipTypeObject)

class Producttranslationgraphql(graphene.ObjectType):
    product_translation = graphene.List(ProductTranslationObject)

class Productvaliditytimeperioduomgraphql(graphene.ObjectType):
    product_validity_time_period_uo_m = graphene.List(ProductValidityTimePeriodUoMObject)

class Profilesourcegraphql(graphene.ObjectType):
    profilesource = graphene.List(ProfilesourceObject)

class Refundallocationgraphql(graphene.ObjectType):
    refund_allocation = graphene.List(RefundAllocationObject)

class Refundcreditmemoallocationgraphql(graphene.ObjectType):
    refund_credit_memo_allocation = graphene.List(RefundCreditMemoAllocationObject)

class Refundpaymentgraphql(graphene.ObjectType):
    refund_payment = graphene.List(RefundPaymentObject)

class Refundpaymentallocationgraphql(graphene.ObjectType):
    refund_payment_allocation = graphene.List(RefundPaymentAllocationObject)

class Renewaltermgraphql(graphene.ObjectType):
    renewal_term = graphene.List(RenewalTermObject)

class Saleschannelgraphql(graphene.ObjectType):
    sales_channel = graphene.List(SalesChannelObject)

class Saleschanneltypegraphql(graphene.ObjectType):
    sales_channel_type = graphene.List(SalesChannelTypeObject)

class Salesordergraphql(graphene.ObjectType):
    sales_order = graphene.List(SalesOrderObject)

class Salesorderchangeloggraphql(graphene.ObjectType):
    sales_order_change_log = graphene.List(SalesOrderChangeLogObject)

class Salesorderchangetypegraphql(graphene.ObjectType):
    sales_order_change_type = graphene.List(SalesOrderChangeTypeObject)

class Salesorderconfirmationstategraphql(graphene.ObjectType):
    sales_order_confirmation_state = graphene.List(SalesOrderConfirmationStateObject)

class Salesorderdeliverygroupgraphql(graphene.ObjectType):
    sales_order_delivery_group = graphene.List(SalesOrderDeliveryGroupObject)

class Salesorderdeliverystategraphql(graphene.ObjectType):
    sales_order_delivery_state = graphene.List(SalesOrderDeliveryStateObject)

class Salesorderpaymentsummarygraphql(graphene.ObjectType):
    sales_order_payment_summary = graphene.List(SalesOrderPaymentSummaryObject)

class Salesorderpriceadjustmentgraphql(graphene.ObjectType):
    sales_order_price_adjustment = graphene.List(SalesOrderPriceAdjustmentObject)

class Salesorderpriceadjustmenttypegraphql(graphene.ObjectType):
    sales_order_price_adjustment_type = graphene.List(SalesOrderPriceAdjustmentTypeObject)

class Salesorderproductgraphql(graphene.ObjectType):
    sales_order_product = graphene.List(SalesOrderProductObject)

class Salesorderproductgroupgraphql(graphene.ObjectType):
    sales_order_product_group = graphene.List(SalesOrderProductGroupObject)

class Salesorderproductgrouptypegraphql(graphene.ObjectType):
    sales_order_product_group_type = graphene.List(SalesOrderProductGroupTypeObject)

class Salesorderproductnotegraphql(graphene.ObjectType):
    sales_order_product_note = graphene.List(SalesOrderProductNoteObject)

class Salesorderproductreasongraphql(graphene.ObjectType):
    sales_order_product_reason = graphene.List(SalesOrderProductReasonObject)

class Salesorderproductreasoncategorygraphql(graphene.ObjectType):
    sales_order_product_reason_category = graphene.List(SalesOrderProductReasonCategoryObject)

class Salesorderproductstategraphql(graphene.ObjectType):
    sales_order_product_state = graphene.List(SalesOrderProductStateObject)

class Salesorderproducttaxgraphql(graphene.ObjectType):
    sales_order_product_tax = graphene.List(SalesOrderProductTaxObject)

class Salesordersegmentgraphql(graphene.ObjectType):
    sales_order_segment = graphene.List(SalesOrderSegmentObject)

class Salesorderstategraphql(graphene.ObjectType):
    sales_order_state = graphene.List(SalesOrderStateObject)

class Salesordertaxgraphql(graphene.ObjectType):
    sales_order_tax = graphene.List(SalesOrderTaxObject)

class Salesordertypegraphql(graphene.ObjectType):
    sales_order_type = graphene.List(SalesOrderTypeObject)

class Sellergraphql(graphene.ObjectType):
    seller = graphene.List(SellerObject)

class Serviceproductgraphql(graphene.ObjectType):
    service_product = graphene.List(ServiceProductObject)

class Shipmentgraphql(graphene.ObjectType):
    shipment = graphene.List(ShipmentObject)

class Shipmentdocumentgraphql(graphene.ObjectType):
    shipment_document = graphene.List(ShipmentDocumentObject)

class Shipmentpackagegraphql(graphene.ObjectType):
    shipment_package = graphene.List(ShipmentPackageObject)

class Shipmentproductgraphql(graphene.ObjectType):
    shipment_product = graphene.List(ShipmentProductObject)

class Shipmentproductpriceadjustmentgraphql(graphene.ObjectType):
    shipment_product_price_adjustment = graphene.List(ShipmentProductPriceAdjustmentObject)

class Shipmentproductpriceadjustmenttaxgraphql(graphene.ObjectType):
    shipment_product_price_adjustment_tax = graphene.List(ShipmentProductPriceAdjustmentTaxObject)

class Shipmentstategraphql(graphene.ObjectType):
    shipment_state = graphene.List(ShipmentStateObject)

class Shippingmethodgraphql(graphene.ObjectType):
    shipping_method = graphene.List(ShippingMethodObject)

class Skillgraphql(graphene.ObjectType):
    skill = graphene.List(SkillObject)

class Suppliergraphql(graphene.ObjectType):
    supplier = graphene.List(SupplierObject)

class Uncategorizedpartygraphql(graphene.ObjectType):
    uncategorized_party = graphene.List(UncategorizedPartyObject)

class Userxgraphql(graphene.ObjectType):
    userx = graphene.List(UserxObject)

class Accountautopaymentmethodjoingraphql(graphene.ObjectType):
    account_auto_payment_method_join = graphene.List(AccountAutoPaymentMethodJoinObject)

class Accountbillfrequencyjoingraphql(graphene.ObjectType):
    account_bill_frequency_join = graphene.List(AccountBillFrequencyJoinObject)

class Accountcontactaccountjoingraphql(graphene.ObjectType):
    account_contact_account_join = graphene.List(AccountContactAccountJoinObject)

class Accountcontactindirectrelationaccountcontactjoingraphql(graphene.ObjectType):
    account_contact_indirect_relation_account_contact_join = graphene.List(AccountContactIndirectRelationAccountContactJoinObject)

class Accountcontactreportstoaccountcontactjoingraphql(graphene.ObjectType):
    account_contact_reports_to_account_contact_join = graphene.List(AccountContactReportsToAccountContactJoinObject)

class Accountcontactroleaccountcontactjoingraphql(graphene.ObjectType):
    account_contact_role_account_contact_join = graphene.List(AccountContactRoleAccountContactJoinObject)

class Accountorderdeliverymethodjoingraphql(graphene.ObjectType):
    account_order_delivery_method_join = graphene.List(AccountOrderDeliveryMethodJoinObject)

class Accountparentaccountjoingraphql(graphene.ObjectType):
    account_parent_account_join = graphene.List(AccountParentAccountJoinObject)

class Accountpartneraccountjoingraphql(graphene.ObjectType):
    account_partner_account_join = graphene.List(AccountPartnerAccountJoinObject)

class Accountpartnerpartneraccountjoingraphql(graphene.ObjectType):
    account_partner_partner_account_join = graphene.List(AccountPartnerPartnerAccountJoinObject)

class Accountpartyjoingraphql(graphene.ObjectType):
    account_party_join = graphene.List(AccountPartyJoinObject)

class Accountpartyrolejoingraphql(graphene.ObjectType):
    account_party_role_join = graphene.List(AccountPartyRoleJoinObject)

class Accountprimarysalescontactpointjoingraphql(graphene.ObjectType):
    account_primary_sales_contact_point_join = graphene.List(AccountPrimarySalesContactPointJoinObject)

class Accountshippingcontactjoingraphql(graphene.ObjectType):
    account_shipping_contact_join = graphene.List(AccountShippingContactJoinObject)

class Accountshippingemailjoingraphql(graphene.ObjectType):
    account_shipping_email_join = graphene.List(AccountShippingEmailJoinObject)

class Accountshippingphoneidjoingraphql(graphene.ObjectType):
    account_shipping_phoneid_join = graphene.List(AccountShippingPhoneidJoinObject)

class Attributevaluetranslationattributevaluejoingraphql(graphene.ObjectType):
    attribute_value_translation_attribute_value_join = graphene.List(AttributeValueTranslationAttributeValueJoinObject)

class Bundleproductbrandjoingraphql(graphene.ObjectType):
    bundle_product_brand_join = graphene.List(BundleProductBrandJoinObject)

class Bundleproductprimaryproductcategoryjoingraphql(graphene.ObjectType):
    bundle_product_primary_product_category_join = graphene.List(BundleProductPrimaryProductCategoryJoinObject)

class Bundleproductprimarysaleschanneljoingraphql(graphene.ObjectType):
    bundle_product_primary_sales_channel_join = graphene.List(BundleProductPrimarySalesChannelJoinObject)

class Bundleproductvalidforperioduomjoingraphql(graphene.ObjectType):
    bundle_product_valid_for_period_uo_m_join = graphene.List(BundleProductValidForPeriodUoMJoinObject)

class Capturepaymentaccountjoingraphql(graphene.ObjectType):
    capture_payment_account_join = graphene.List(CapturePaymentAccountJoinObject)

class Capturepaymentinternalbusinesunitjoingraphql(graphene.ObjectType):
    capture_payment_internal_busines_unit_join = graphene.List(CapturePaymentInternalBusinesUnitJoinObject)

class Capturepaymentlatestgatewayresultcodejoingraphql(graphene.ObjectType):
    capture_payment_latest_gateway_result_code_join = graphene.List(CapturePaymentLatestGatewayResultCodeJoinObject)

class Capturepaymentpaymentauthorizationjoingraphql(graphene.ObjectType):
    capture_payment_payment_authorization_join = graphene.List(CapturePaymentPaymentAuthorizationJoinObject)

class Capturepaymentpaymentgatewayjoingraphql(graphene.ObjectType):
    capture_payment_payment_gateway_join = graphene.List(CapturePaymentPaymentGatewayJoinObject)

class Capturepaymentpaymentgroupjoingraphql(graphene.ObjectType):
    capture_payment_payment_group_join = graphene.List(CapturePaymentPaymentGroupJoinObject)

class Capturepaymentpaymentmethodjoingraphql(graphene.ObjectType):
    capture_payment_payment_method_join = graphene.List(CapturePaymentPaymentMethodJoinObject)

class Capturepaymentpaymenttreatmentjoingraphql(graphene.ObjectType):
    capture_payment_payment_treatment_join = graphene.List(CapturePaymentPaymentTreatmentJoinObject)

class Capturepaymentsalesorderpaymentsummaryjoingraphql(graphene.ObjectType):
    capture_payment_sales_order_payment_summary_join = graphene.List(CapturePaymentSalesOrderPaymentSummaryJoinObject)

class Competitorpartyjoingraphql(graphene.ObjectType):
    competitor_party_join = graphene.List(CompetitorPartyJoinObject)

class Couponmanufacturerjoingraphql(graphene.ObjectType):
    coupon_manufacturer_join = graphene.List(CouponManufacturerJoinObject)

class Couponpaymentmethodtypejoingraphql(graphene.ObjectType):
    coupon_payment_method_type_join = graphene.List(CouponPaymentMethodTypeJoinObject)

class Credittenderaccountjoingraphql(graphene.ObjectType):
    credit_tender_account_join = graphene.List(CreditTenderAccountJoinObject)

class Credittenderpaymentmethodtypejoingraphql(graphene.ObjectType):
    credit_tender_payment_method_type_join = graphene.List(CreditTenderPaymentMethodTypeJoinObject)

class Customerpartyjoingraphql(graphene.ObjectType):
    customer_party_join = graphene.List(CustomerPartyJoinObject)

class Customerstatehistorypartyrolejoingraphql(graphene.ObjectType):
    customer_state_history_party_role_join = graphene.List(CustomerStateHistoryPartyRoleJoinObject)

class Goodsproductbrandjoingraphql(graphene.ObjectType):
    goods_product_brand_join = graphene.List(GoodsProductBrandJoinObject)

class Goodsproductprimaryproductcategoryjoingraphql(graphene.ObjectType):
    goods_product_primary_product_category_join = graphene.List(GoodsProductPrimaryProductCategoryJoinObject)

class Goodsproductprimarysaleschanneljoingraphql(graphene.ObjectType):
    goods_product_primary_sales_channel_join = graphene.List(GoodsProductPrimarySalesChannelJoinObject)

class Goodsproductvalidforperioduomjoingraphql(graphene.ObjectType):
    goods_product_valid_for_period_uo_m_join = graphene.List(GoodsProductValidForPeriodUoMJoinObject)

class Householdprimaryaccountjoingraphql(graphene.ObjectType):
    household_primary_account_join = graphene.List(HouseholdPrimaryAccountJoinObject)

class Individualgraphql(graphene.ObjectType):
    individual = graphene.List(IndividualObject)

class Industryjobgraphql(graphene.ObjectType):
    industry_job = graphene.List(IndustryJobObject)

class Internalbusinesunitparentinternalbusinesunitjoingraphql(graphene.ObjectType):
    internal_busines_unit_parent_internal_busines_unit_join = graphene.List(InternalBusinesUnitParentInternalBusinesUnitJoinObject)

class Internalbusinesunitprimaryaccountjoingraphql(graphene.ObjectType):
    internal_busines_unit_primary_account_join = graphene.List(InternalBusinesUnitPrimaryAccountJoinObject)

class Jobskillgraphql(graphene.ObjectType):
    job_skill = graphene.List(JobSkillObject)

class Leadconvertedtoaccountcontactjoingraphql(graphene.ObjectType):
    lead_converted_to_account_contact_join = graphene.List(LeadConvertedToAccountContactJoinObject)

class Leadconvertedtoaccountjoingraphql(graphene.ObjectType):
    lead_converted_to_account_join = graphene.List(LeadConvertedToAccountJoinObject)

class Leadfaxcontactphonejoingraphql(graphene.ObjectType):
    lead_fax_contact_phone_join = graphene.List(LeadFaxContactPhoneJoinObject)

class Leadmobilecontactphonejoingraphql(graphene.ObjectType):
    lead_mobile_contact_phone_join = graphene.List(LeadMobileContactPhoneJoinObject)

class Leadpartneraccountjoingraphql(graphene.ObjectType):
    lead_partner_account_join = graphene.List(LeadPartnerAccountJoinObject)

class Leadpartyrolejoingraphql(graphene.ObjectType):
    lead_party_role_join = graphene.List(LeadPartyRoleJoinObject)

class Partyadditionalnamepartyjoingraphql(graphene.ObjectType):
    party_additional_name_party_join = graphene.List(PartyAdditionalNamePartyJoinObject)

class Partyidentificationpartyjoingraphql(graphene.ObjectType):
    party_identification_party_join = graphene.List(PartyIdentificationPartyJoinObject)

class Partyidentificationpartyrolejoingraphql(graphene.ObjectType):
    party_identification_party_role_join = graphene.List(PartyIdentificationPartyRoleJoinObject)

class Partyprimaryaccountjoingraphql(graphene.ObjectType):
    party_primary_account_join = graphene.List(PartyPrimaryAccountJoinObject)

class Partyrelatedpartypartyjoingraphql(graphene.ObjectType):
    party_related_party_party_join = graphene.List(PartyRelatedPartyPartyJoinObject)

class Partyrelatedpartypartyrelationshiptypejoingraphql(graphene.ObjectType):
    party_related_party_party_relationship_type_join = graphene.List(PartyRelatedPartyPartyRelationshipTypeJoinObject)

class Partyrelatedpartyrelatedpartyjoingraphql(graphene.ObjectType):
    party_related_party_related_party_join = graphene.List(PartyRelatedPartyRelatedPartyJoinObject)

class Partyrolepartyjoingraphql(graphene.ObjectType):
    party_role_party_join = graphene.List(PartyRolePartyJoinObject)

class Partywebaddrpartyjoingraphql(graphene.ObjectType):
    party_web_addr_party_join = graphene.List(PartyWebAddrPartyJoinObject)

class Partywebaddrpartyrolejoingraphql(graphene.ObjectType):
    party_web_addr_party_role_join = graphene.List(PartyWebAddrPartyRoleJoinObject)

class Paygatautlogpaygatinttypjoingraphql(graphene.ObjectType):
    pay_gat_aut_log_pay_gat_int_typ_join = graphene.List(PayGatAutLogPayGatIntTypJoinObject)

class Paygatautrevlogpayautrevjoingraphql(graphene.ObjectType):
    pay_gat_aut_rev_log_pay_aut_rev_join = graphene.List(PayGatAutRevLogPayAutRevJoinObject)

class Paygatautrevlogpaygatinttypjoingraphql(graphene.ObjectType):
    pay_gat_aut_rev_log_pay_gat_int_typ_join = graphene.List(PayGatAutRevLogPayGatIntTypJoinObject)

class Paygatintlogpaygatinttypjoingraphql(graphene.ObjectType):
    pay_gat_int_log_pay_gat_int_typ_join = graphene.List(PayGatIntLogPayGatIntTypJoinObject)

class Paygatpaylogpaygatinttypjoingraphql(graphene.ObjectType):
    pay_gat_pay_log_pay_gat_int_typ_join = graphene.List(PayGatPayLogPayGatIntTypJoinObject)

class Paymentaccountjoingraphql(graphene.ObjectType):
    payment_account_join = graphene.List(PaymentAccountJoinObject)

class Paymentallocationrelatedpaymentallocationjoingraphql(graphene.ObjectType):
    payment_allocation_related_payment_allocation_join = graphene.List(PaymentAllocationRelatedPaymentAllocationJoinObject)

class Paymentapplicationpaymentjoingraphql(graphene.ObjectType):
    payment_application_payment_join = graphene.List(PaymentApplicationPaymentJoinObject)

class Paymentauthorizationpaymentgatewayjoingraphql(graphene.ObjectType):
    payment_authorization_payment_gateway_join = graphene.List(PaymentAuthorizationPaymentGatewayJoinObject)

class Paymentauthorizationpaymentgatewayresultjoingraphql(graphene.ObjectType):
    payment_authorization_payment_gateway_result_join = graphene.List(PaymentAuthorizationPaymentGatewayResultJoinObject)

class Paymentauthorizationpaymentgroupjoingraphql(graphene.ObjectType):
    payment_authorization_payment_group_join = graphene.List(PaymentAuthorizationPaymentGroupJoinObject)

class Paymentauthorizationpaymentmethodjoingraphql(graphene.ObjectType):
    payment_authorization_payment_method_join = graphene.List(PaymentAuthorizationPaymentMethodJoinObject)

class Paymentauthorizationreversalcapturepaymentjoingraphql(graphene.ObjectType):
    payment_authorization_reversal_capture_payment_join = graphene.List(PaymentAuthorizationReversalCapturePaymentJoinObject)

class Paymentauthorizationreversalpaymentauthorizationjoingraphql(graphene.ObjectType):
    payment_authorization_reversal_payment_authorization_join = graphene.List(PaymentAuthorizationReversalPaymentAuthorizationJoinObject)

class Paymentauthorizationreversalpaymentgatewayresultjoingraphql(graphene.ObjectType):
    payment_authorization_reversal_payment_gateway_result_join = graphene.List(PaymentAuthorizationReversalPaymentGatewayResultJoinObject)

class Paymentauthorizationsalesorderpaymentsummaryjoingraphql(graphene.ObjectType):
    payment_authorization_sales_order_payment_summary_join = graphene.List(PaymentAuthorizationSalesOrderPaymentSummaryJoinObject)

class Paymentcardpaymentmethodtypejoingraphql(graphene.ObjectType):
    payment_card_payment_method_type_join = graphene.List(PaymentCardPaymentMethodTypeJoinObject)

class Paymentcreditmemoallocationrelatedpaymentallocationjoingraphql(graphene.ObjectType):
    payment_credit_memo_allocation_related_payment_allocation_join = graphene.List(PaymentCreditMemoAllocationRelatedPaymentAllocationJoinObject)

class Paymentcreditmemoapplicationpaymentjoingraphql(graphene.ObjectType):
    payment_credit_memo_application_payment_join = graphene.List(PaymentCreditMemoApplicationPaymentJoinObject)

class Paymentgatewayauthreversallogpaymentgatewayresultjoingraphql(graphene.ObjectType):
    payment_gateway_auth_reversal_log_payment_gateway_result_join = graphene.List(PaymentGatewayAuthReversalLogPaymentGatewayResultJoinObject)

class Paymentgatewayauthorizationlogpaymentauthorizationjoingraphql(graphene.ObjectType):
    payment_gateway_authorization_log_payment_authorization_join = graphene.List(PaymentGatewayAuthorizationLogPaymentAuthorizationJoinObject)

class Paymentgatewayauthorizationlogpaymentgatewayresultjoingraphql(graphene.ObjectType):
    payment_gateway_authorization_log_payment_gateway_result_join = graphene.List(PaymentGatewayAuthorizationLogPaymentGatewayResultJoinObject)

class Paymentgatewayinteractionlogpaymentgatewayresultjoingraphql(graphene.ObjectType):
    payment_gateway_interaction_log_payment_gateway_result_join = graphene.List(PaymentGatewayInteractionLogPaymentGatewayResultJoinObject)

class Paymentgatewaypaymentgatewayproviderjoingraphql(graphene.ObjectType):
    payment_gateway_payment_gateway_provider_join = graphene.List(PaymentGatewayPaymentGatewayProviderJoinObject)

class Paymentgatewaypaymentlogpaymentgatewayresultjoingraphql(graphene.ObjectType):
    payment_gateway_payment_log_payment_gateway_result_join = graphene.List(PaymentGatewayPaymentLogPaymentGatewayResultJoinObject)

class Paymentgatewaypaymentlogpaymentjoingraphql(graphene.ObjectType):
    payment_gateway_payment_log_payment_join = graphene.List(PaymentGatewayPaymentLogPaymentJoinObject)

class Paymentinternalbusinesunitjoingraphql(graphene.ObjectType):
    payment_internal_busines_unit_join = graphene.List(PaymentInternalBusinesUnitJoinObject)

class Paymentinvoiceallocationpaymentinvoiceapplicationjoingraphql(graphene.ObjectType):
    payment_invoice_allocation_payment_invoice_application_join = graphene.List(PaymentInvoiceAllocationPaymentInvoiceApplicationJoinObject)

class Paymentinvoiceallocationrelatedpaymentallocationjoingraphql(graphene.ObjectType):
    payment_invoice_allocation_related_payment_allocation_join = graphene.List(PaymentInvoiceAllocationRelatedPaymentAllocationJoinObject)

class Paymentinvoiceapplicationpaymentjoingraphql(graphene.ObjectType):
    payment_invoice_application_payment_join = graphene.List(PaymentInvoiceApplicationPaymentJoinObject)

class Paymentlatestgatewayresultcodejoingraphql(graphene.ObjectType):
    payment_latest_gateway_result_code_join = graphene.List(PaymentLatestGatewayResultCodeJoinObject)

class Paymentmethodpaymentmethodtypejoingraphql(graphene.ObjectType):
    payment_method_payment_method_type_join = graphene.List(PaymentMethodPaymentMethodTypeJoinObject)

class Paymentpaymentgatewayjoingraphql(graphene.ObjectType):
    payment_payment_gateway_join = graphene.List(PaymentPaymentGatewayJoinObject)

class Paymentpaymentgroupjoingraphql(graphene.ObjectType):
    payment_payment_group_join = graphene.List(PaymentPaymentGroupJoinObject)

class Paymentpaymentmethodjoingraphql(graphene.ObjectType):
    payment_payment_method_join = graphene.List(PaymentPaymentMethodJoinObject)

class Paymentpaymenttreatmentjoingraphql(graphene.ObjectType):
    payment_payment_treatment_join = graphene.List(PaymentPaymentTreatmentJoinObject)

class Paymentsalesorderpaymentsummaryjoingraphql(graphene.ObjectType):
    payment_sales_order_payment_summary_join = graphene.List(PaymentSalesOrderPaymentSummaryJoinObject)

class Paymenttreatmentpaymentpolicyjoingraphql(graphene.ObjectType):
    payment_treatment_payment_policy_join = graphene.List(PaymentTreatmentPaymentPolicyJoinObject)

class Paymenttreatmentpaymenttreatmentmethodjoingraphql(graphene.ObjectType):
    payment_treatment_payment_treatment_method_join = graphene.List(PaymentTreatmentPaymentTreatmentMethodJoinObject)

class Productgraphql(graphene.ObjectType):
    product = graphene.List(ProductObject)

class Productattributevalueattributevaluejoingraphql(graphene.ObjectType):
    product_attribute_value_attribute_value_join = graphene.List(ProductAttributeValueAttributeValueJoinObject)

class Productcatalogtranslationproductcatalogjoingraphql(graphene.ObjectType):
    product_catalog_translation_product_catalog_join = graphene.List(ProductCatalogTranslationProductCatalogJoinObject)

class Productcategoryattributesetproductcategoryjoingraphql(graphene.ObjectType):
    product_category_attribute_set_product_category_join = graphene.List(ProductCategoryAttributeSetProductCategoryJoinObject)

class Productcategoryparentcategoryjoingraphql(graphene.ObjectType):
    product_category_parent_category_join = graphene.List(ProductCategoryParentCategoryJoinObject)

class Productcategoryproductcatalogjoingraphql(graphene.ObjectType):
    product_category_product_catalog_join = graphene.List(ProductCategoryProductCatalogJoinObject)

class Productcategoryproductproductcategoryjoingraphql(graphene.ObjectType):
    product_category_product_product_category_join = graphene.List(ProductCategoryProductProductCategoryJoinObject)

class Productcategorytranslationproductcategoryjoingraphql(graphene.ObjectType):
    product_category_translation_product_category_join = graphene.List(ProductCategoryTranslationProductCategoryJoinObject)

class Productimagetranslationproductimagejoingraphql(graphene.ObjectType):
    product_image_translation_product_image_join = graphene.List(ProductImageTranslationProductImageJoinObject)

class Productrelatedproductproductrelationshiptypejoingraphql(graphene.ObjectType):
    product_related_product_product_relationship_type_join = graphene.List(ProductRelatedProductProductRelationshipTypeJoinObject)

class Productrelatedproductsalesorderproduct1joingraphql(graphene.ObjectType):
    product_related_product_sales_order_product1_join = graphene.List(ProductRelatedProductSalesOrderProduct1JoinObject)

class Productrelatedproductsalesorderproduct2joingraphql(graphene.ObjectType):
    product_related_product_sales_order_product2_join = graphene.List(ProductRelatedProductSalesOrderProduct2JoinObject)

class Refundallocationrefundpaymentjoingraphql(graphene.ObjectType):
    refund_allocation_refund_payment_join = graphene.List(RefundAllocationRefundPaymentJoinObject)

class Refundallocationrelatedrefundallocationjoingraphql(graphene.ObjectType):
    refund_allocation_related_refund_allocation_join = graphene.List(RefundAllocationRelatedRefundAllocationJoinObject)

class Refundcreditmemoallocationrefundpaymentjoingraphql(graphene.ObjectType):
    refund_credit_memo_allocation_refund_payment_join = graphene.List(RefundCreditMemoAllocationRefundPaymentJoinObject)

class Refundcreditmemoallocationrelatedrefundallocationjoingraphql(graphene.ObjectType):
    refund_credit_memo_allocation_related_refund_allocation_join = graphene.List(RefundCreditMemoAllocationRelatedRefundAllocationJoinObject)

class Refundpaymentaccountjoingraphql(graphene.ObjectType):
    refund_payment_account_join = graphene.List(RefundPaymentAccountJoinObject)

class Refundpaymentallocationcapturepaymentjoingraphql(graphene.ObjectType):
    refund_payment_allocation_capture_payment_join = graphene.List(RefundPaymentAllocationCapturePaymentJoinObject)

class Refundpaymentallocationrefundpaymentjoingraphql(graphene.ObjectType):
    refund_payment_allocation_refund_payment_join = graphene.List(RefundPaymentAllocationRefundPaymentJoinObject)

class Refundpaymentallocationrelatedrefundallocationjoingraphql(graphene.ObjectType):
    refund_payment_allocation_related_refund_allocation_join = graphene.List(RefundPaymentAllocationRelatedRefundAllocationJoinObject)

class Refundpaymentinternalbusinesunitjoingraphql(graphene.ObjectType):
    refund_payment_internal_busines_unit_join = graphene.List(RefundPaymentInternalBusinesUnitJoinObject)

class Refundpaymentlatestgatewayresultcodejoingraphql(graphene.ObjectType):
    refund_payment_latest_gateway_result_code_join = graphene.List(RefundPaymentLatestGatewayResultCodeJoinObject)

class Refundpaymentpaymentgatewayjoingraphql(graphene.ObjectType):
    refund_payment_payment_gateway_join = graphene.List(RefundPaymentPaymentGatewayJoinObject)

class Refundpaymentpaymentgroupjoingraphql(graphene.ObjectType):
    refund_payment_payment_group_join = graphene.List(RefundPaymentPaymentGroupJoinObject)

class Refundpaymentpaymentmethodjoingraphql(graphene.ObjectType):
    refund_payment_payment_method_join = graphene.List(RefundPaymentPaymentMethodJoinObject)

class Refundpaymentpaymenttreatmentjoingraphql(graphene.ObjectType):
    refund_payment_payment_treatment_join = graphene.List(RefundPaymentPaymentTreatmentJoinObject)

class Refundpaymentsalesorderpaymentsummaryjoingraphql(graphene.ObjectType):
    refund_payment_sales_order_payment_summary_join = graphene.List(RefundPaymentSalesOrderPaymentSummaryJoinObject)

class Salordproreasalordproreacatjoingraphql(graphene.ObjectType):
    sal_ord_pro_rea_sal_ord_pro_rea_cat_join = graphene.List(SalOrdProReaSalOrdProReaCatJoinObject)

class Saleschannelsaleschanneltypejoingraphql(graphene.ObjectType):
    sales_channel_sales_channel_type_join = graphene.List(SalesChannelSalesChannelTypeJoinObject)

class Salesorderbilltoaccountjoingraphql(graphene.ObjectType):
    sales_order_bill_to_account_join = graphene.List(SalesOrderBillToAccountJoinObject)

class Salesorderbilltoaddrjoingraphql(graphene.ObjectType):
    sales_order_bill_to_addr_join = graphene.List(SalesOrderBillToAddrJoinObject)

class Salesorderbilltocontactjoingraphql(graphene.ObjectType):
    sales_order_bill_to_contact_join = graphene.List(SalesOrderBillToContactJoinObject)

class Salesorderbilltoemailjoingraphql(graphene.ObjectType):
    sales_order_bill_to_email_join = graphene.List(SalesOrderBillToEmailJoinObject)

class Salesorderbilltophonenumberjoingraphql(graphene.ObjectType):
    sales_order_bill_to_phone_number_join = graphene.List(SalesOrderBillToPhoneNumberJoinObject)

class Salesorderchangelogchangesalesorderjoingraphql(graphene.ObjectType):
    sales_order_change_log_change_sales_order_join = graphene.List(SalesOrderChangeLogChangeSalesOrderJoinObject)

class Salesorderchangelogchangesalesorderproductjoingraphql(graphene.ObjectType):
    sales_order_change_log_change_sales_order_product_join = graphene.List(SalesOrderChangeLogChangeSalesOrderProductJoinObject)

class Salesorderchangelogrelatedsalesorderjoingraphql(graphene.ObjectType):
    sales_order_change_log_related_sales_order_join = graphene.List(SalesOrderChangeLogRelatedSalesOrderJoinObject)

class Salesorderchangelogrelatedsalesorderproductjoingraphql(graphene.ObjectType):
    sales_order_change_log_related_sales_order_product_join = graphene.List(SalesOrderChangeLogRelatedSalesOrderProductJoinObject)

class Salesorderdeliverygroupaccountcontactjoingraphql(graphene.ObjectType):
    sales_order_delivery_group_account_contact_join = graphene.List(SalesOrderDeliveryGroupAccountContactJoinObject)

class Salesorderdeliverygroupcontactpointaddrjoingraphql(graphene.ObjectType):
    sales_order_delivery_group_contact_point_addr_join = graphene.List(SalesOrderDeliveryGroupContactPointAddrJoinObject)

class Salesorderdeliverygrouporderdeliverymethodjoingraphql(graphene.ObjectType):
    sales_order_delivery_group_order_delivery_method_join = graphene.List(SalesOrderDeliveryGroupOrderDeliveryMethodJoinObject)

class Salesorderdeliverygrouporiginaldeliverygroupjoingraphql(graphene.ObjectType):
    sales_order_delivery_group_original_delivery_group_join = graphene.List(SalesOrderDeliveryGroupOriginalDeliveryGroupJoinObject)

class Salesorderdeliverygroupsalesorderdeliverystatejoingraphql(graphene.ObjectType):
    sales_order_delivery_group_sales_order_delivery_state_join = graphene.List(SalesOrderDeliveryGroupSalesOrderDeliveryStateJoinObject)

class Salesorderdeliverygroupsalesorderjoingraphql(graphene.ObjectType):
    sales_order_delivery_group_sales_order_join = graphene.List(SalesOrderDeliveryGroupSalesOrderJoinObject)

class Salesorderinternalbusinesunitjoingraphql(graphene.ObjectType):
    sales_order_internal_busines_unit_join = graphene.List(SalesOrderInternalBusinesUnitJoinObject)

class Salesorderoriginalorderjoingraphql(graphene.ObjectType):
    sales_order_original_order_join = graphene.List(SalesOrderOriginalOrderJoinObject)

class Salesorderpaymentmethodjoingraphql(graphene.ObjectType):
    sales_order_payment_method_join = graphene.List(SalesOrderPaymentMethodJoinObject)

class Salesorderpaymentsummarypaymentmethodjoingraphql(graphene.ObjectType):
    sales_order_payment_summary_payment_method_join = graphene.List(SalesOrderPaymentSummaryPaymentMethodJoinObject)

class Salesorderpaymentsummarysalesorderjoingraphql(graphene.ObjectType):
    sales_order_payment_summary_sales_order_join = graphene.List(SalesOrderPaymentSummarySalesOrderJoinObject)

class Salesorderpriceadjustmentsalesorderjoingraphql(graphene.ObjectType):
    sales_order_price_adjustment_sales_order_join = graphene.List(SalesOrderPriceAdjustmentSalesOrderJoinObject)

class Salesorderproductgroupsalesorderproductgrouptypejoingraphql(graphene.ObjectType):
    sales_order_product_group_sales_order_product_group_type_join = graphene.List(SalesOrderProductGroupSalesOrderProductGroupTypeJoinObject)

class Salesorderproductlistpricetermuomjoingraphql(graphene.ObjectType):
    sales_order_product_list_price_term_uo_m_join = graphene.List(SalesOrderProductListPriceTermUoMJoinObject)

class Salesorderproductoriginalorderproductjoingraphql(graphene.ObjectType):
    sales_order_product_original_order_product_join = graphene.List(SalesOrderProductOriginalOrderProductJoinObject)

class Salesorderproductpricebookentryjoingraphql(graphene.ObjectType):
    sales_order_product_price_book_entry_join = graphene.List(SalesOrderProductPriceBookEntryJoinObject)

class Salesorderproductsalesorderdeliverygroupjoingraphql(graphene.ObjectType):
    sales_order_product_sales_order_delivery_group_join = graphene.List(SalesOrderProductSalesOrderDeliveryGroupJoinObject)

class Salesorderproductsalesorderjoingraphql(graphene.ObjectType):
    sales_order_product_sales_order_join = graphene.List(SalesOrderProductSalesOrderJoinObject)

class Salesorderproductsalesorderproductreasonjoingraphql(graphene.ObjectType):
    sales_order_product_sales_order_product_reason_join = graphene.List(SalesOrderProductSalesOrderProductReasonJoinObject)

class Salesorderproductsalesorderproductstatejoingraphql(graphene.ObjectType):
    sales_order_product_sales_order_product_state_join = graphene.List(SalesOrderProductSalesOrderProductStateJoinObject)

class Salesorderproductselleraccountjoingraphql(graphene.ObjectType):
    sales_order_product_seller_account_join = graphene.List(SalesOrderProductSellerAccountJoinObject)

class Salesorderproductshippingaddrjoingraphql(graphene.ObjectType):
    sales_order_product_shipping_addr_join = graphene.List(SalesOrderProductShippingAddrJoinObject)

class Salesorderproductshippingemailjoingraphql(graphene.ObjectType):
    sales_order_product_shipping_email_join = graphene.List(SalesOrderProductShippingEmailJoinObject)

class Salesorderproductshippingphonejoingraphql(graphene.ObjectType):
    sales_order_product_shipping_phone_join = graphene.List(SalesOrderProductShippingPhoneJoinObject)

class Salesorderproductsubscriptiontermunitjoingraphql(graphene.ObjectType):
    sales_order_product_subscription_term_unit_join = graphene.List(SalesOrderProductSubscriptionTermUnitJoinObject)

class Salesorderproducttaxoriginalsalesorderproducttaxjoingraphql(graphene.ObjectType):
    sales_order_product_tax_original_sales_order_product_tax_join = graphene.List(SalesOrderProductTaxOriginalSalesOrderProductTaxJoinObject)

class Salesorderproducttaxsalesorderproductjoingraphql(graphene.ObjectType):
    sales_order_product_tax_sales_order_product_join = graphene.List(SalesOrderProductTaxSalesOrderProductJoinObject)

class Salesorderrenewaltermjoingraphql(graphene.ObjectType):
    sales_order_renewal_term_join = graphene.List(SalesOrderRenewalTermJoinObject)

class Salesordersaleschanneljoingraphql(graphene.ObjectType):
    sales_order_sales_channel_join = graphene.List(SalesOrderSalesChannelJoinObject)

class Salesordersalesorderconfirmationstatejoingraphql(graphene.ObjectType):
    sales_order_sales_order_confirmation_state_join = graphene.List(SalesOrderSalesOrderConfirmationStateJoinObject)

class Salesordersalesorderstatejoingraphql(graphene.ObjectType):
    sales_order_sales_order_state_join = graphene.List(SalesOrderSalesOrderStateJoinObject)

class Salesordersalesordertypejoingraphql(graphene.ObjectType):
    sales_order_sales_order_type_join = graphene.List(SalesOrderSalesOrderTypeJoinObject)

class Salesordersellerjoingraphql(graphene.ObjectType):
    sales_order_seller_join = graphene.List(SalesOrderSellerJoinObject)

class Salesordershiptoaddrjoingraphql(graphene.ObjectType):
    sales_order_ship_to_addr_join = graphene.List(SalesOrderShipToAddrJoinObject)

class Salesordershiptocontactjoingraphql(graphene.ObjectType):
    sales_order_ship_to_contact_join = graphene.List(SalesOrderShipToContactJoinObject)

class Salesordershiptoemailjoingraphql(graphene.ObjectType):
    sales_order_ship_to_email_join = graphene.List(SalesOrderShipToEmailJoinObject)

class Salesordersoldtocustomerjoingraphql(graphene.ObjectType):
    sales_order_sold_to_customer_join = graphene.List(SalesOrderSoldToCustomerJoinObject)

class Salesorderuserdevicesesionjoingraphql(graphene.ObjectType):
    sales_order_user_device_sesion_join = graphene.List(SalesOrderUserDeviceSesionJoinObject)

class Sellerpartyjoingraphql(graphene.ObjectType):
    seller_party_join = graphene.List(SellerPartyJoinObject)

class Serviceproductbrandjoingraphql(graphene.ObjectType):
    service_product_brand_join = graphene.List(ServiceProductBrandJoinObject)

class Serviceproductprimaryproductcategoryjoingraphql(graphene.ObjectType):
    service_product_primary_product_category_join = graphene.List(ServiceProductPrimaryProductCategoryJoinObject)

class Serviceproductprimarysaleschanneljoingraphql(graphene.ObjectType):
    service_product_primary_sales_channel_join = graphene.List(ServiceProductPrimarySalesChannelJoinObject)

class Serviceproductserviceprovideraccountjoingraphql(graphene.ObjectType):
    service_product_service_provider_account_join = graphene.List(ServiceProductServiceProviderAccountJoinObject)

class Serviceproductvalidforperioduomjoingraphql(graphene.ObjectType):
    service_product_valid_for_period_uo_m_join = graphene.List(ServiceProductValidForPeriodUoMJoinObject)

class Shipropriadjtaxshipropriadjjoingraphql(graphene.ObjectType):
    shi_pro_pri_adj_tax_shi_pro_pri_adj_join = graphene.List(ShiProPriAdjTaxShiProPriAdjJoinObject)

class Shipmentdocumentshipmentjoingraphql(graphene.ObjectType):
    shipment_document_shipment_join = graphene.List(ShipmentDocumentShipmentJoinObject)

class Shipmentpackageshipmentjoingraphql(graphene.ObjectType):
    shipment_package_shipment_join = graphene.List(ShipmentPackageShipmentJoinObject)

class Shipmentproductpriceadjustmentshipmentproductjoingraphql(graphene.ObjectType):
    shipment_product_price_adjustment_shipment_product_join = graphene.List(ShipmentProductPriceAdjustmentShipmentProductJoinObject)

class Shipmentproductsalesorderproductjoingraphql(graphene.ObjectType):
    shipment_product_sales_order_product_join = graphene.List(ShipmentProductSalesOrderProductJoinObject)

class Shipmentproductshipmentjoingraphql(graphene.ObjectType):
    shipment_product_shipment_join = graphene.List(ShipmentProductShipmentJoinObject)

class Shipmentproductshipmentpackagejoingraphql(graphene.ObjectType):
    shipment_product_shipment_package_join = graphene.List(ShipmentProductShipmentPackageJoinObject)

class Shipmentsalesorderdeliverygroupjoingraphql(graphene.ObjectType):
    shipment_sales_order_delivery_group_join = graphene.List(ShipmentSalesOrderDeliveryGroupJoinObject)

class Shipmentsalesorderjoingraphql(graphene.ObjectType):
    shipment_sales_order_join = graphene.List(ShipmentSalesOrderJoinObject)

class Shipmentshiptoaddrjoingraphql(graphene.ObjectType):
    shipment_ship_to_addr_join = graphene.List(ShipmentShipToAddrJoinObject)

class Shipmentshipmentstatejoingraphql(graphene.ObjectType):
    shipment_shipment_state_join = graphene.List(ShipmentShipmentStateJoinObject)

class Supplierpartyjoingraphql(graphene.ObjectType):
    supplier_party_join = graphene.List(SupplierPartyJoinObject)

class Uncategorizedpartyprimaryaccountjoingraphql(graphene.ObjectType):
    uncategorized_party_primary_account_join = graphene.List(UncategorizedPartyPrimaryAccountJoinObject)

class Accountcontactindividualjoingraphql(graphene.ObjectType):
    account_contact_individual_join = graphene.List(AccountContactIndividualJoinObject)

class Bundleproductmasterproductjoingraphql(graphene.ObjectType):
    bundle_product_master_product_join = graphene.List(BundleProductMasterProductJoinObject)

class Educationgraphql(graphene.ObjectType):
    education = graphene.List(EducationObject)

class Goodsproductmasterproductjoingraphql(graphene.ObjectType):
    goods_product_master_product_join = graphene.List(GoodsProductMasterProductJoinObject)

class Individualprimaryaccountjoingraphql(graphene.ObjectType):
    individual_primary_account_join = graphene.List(IndividualPrimaryAccountJoinObject)

class Individualprimaryhouseholdjoingraphql(graphene.ObjectType):
    individual_primary_household_join = graphene.List(IndividualPrimaryHouseholdJoinObject)

class Jobindividualgraphql(graphene.ObjectType):
    job_individual = graphene.List(JobIndividualObject)

class Locationgraphql(graphene.ObjectType):
    location = graphene.List(LocationObject)

class Orderdeliverymethodproductjoingraphql(graphene.ObjectType):
    order_delivery_method_product_join = graphene.List(OrderDeliveryMethodProductJoinObject)

class Personlanguageindividualjoingraphql(graphene.ObjectType):
    person_language_individual_join = graphene.List(PersonLanguageIndividualJoinObject)

class Personlifeeventindividualjoingraphql(graphene.ObjectType):
    person_life_event_individual_join = graphene.List(PersonLifeEventIndividualJoinObject)

class Portalgraphql(graphene.ObjectType):
    portal = graphene.List(PortalObject)

class Pricebookentryproductjoingraphql(graphene.ObjectType):
    price_book_entry_product_join = graphene.List(PriceBookEntryProductJoinObject)

class Productattributesetproductjoingraphql(graphene.ObjectType):
    product_attribute_set_product_join = graphene.List(ProductAttributeSetProductJoinObject)

class Productattributevalueproductjoingraphql(graphene.ObjectType):
    product_attribute_value_product_join = graphene.List(ProductAttributeValueProductJoinObject)

class Productbrandjoingraphql(graphene.ObjectType):
    product_brand_join = graphene.List(ProductBrandJoinObject)

class Productcategoryproductproductjoingraphql(graphene.ObjectType):
    product_category_product_product_join = graphene.List(ProductCategoryProductProductJoinObject)

class Productcollateralproductjoingraphql(graphene.ObjectType):
    product_collateral_product_join = graphene.List(ProductCollateralProductJoinObject)

class Productimageproductjoingraphql(graphene.ObjectType):
    product_image_product_join = graphene.List(ProductImageProductJoinObject)

class Productmasterproductjoingraphql(graphene.ObjectType):
    product_master_product_join = graphene.List(ProductMasterProductJoinObject)

class Productprimaryproductcategoryjoingraphql(graphene.ObjectType):
    product_primary_product_category_join = graphene.List(ProductPrimaryProductCategoryJoinObject)

class Productprimarysaleschanneljoingraphql(graphene.ObjectType):
    product_primary_sales_channel_join = graphene.List(ProductPrimarySalesChannelJoinObject)

class Productrelatedproductchildproductjoingraphql(graphene.ObjectType):
    product_related_product_child_product_join = graphene.List(ProductRelatedProductChildProductJoinObject)

class Productrelatedproductparentproductjoingraphql(graphene.ObjectType):
    product_related_product_parent_product_join = graphene.List(ProductRelatedProductParentProductJoinObject)

class Producttranslationproductjoingraphql(graphene.ObjectType):
    product_translation_product_join = graphene.List(ProductTranslationProductJoinObject)

class Productvalidforperioduomjoingraphql(graphene.ObjectType):
    product_valid_for_period_uo_m_join = graphene.List(ProductValidForPeriodUoMJoinObject)

class Profilegraphql(graphene.ObjectType):
    profile = graphene.List(ProfileObject)

class Salesorderproductproductjoingraphql(graphene.ObjectType):
    sales_order_product_product_join = graphene.List(SalesOrderProductProductJoinObject)

class Serviceproductmasterproductjoingraphql(graphene.ObjectType):
    service_product_master_product_join = graphene.List(ServiceProductMasterProductJoinObject)

class Shipmentproductproductjoingraphql(graphene.ObjectType):
    shipment_product_product_join = graphene.List(ShipmentProductProductJoinObject)

class Shippingmethodproductjoingraphql(graphene.ObjectType):
    shipping_method_product_join = graphene.List(ShippingMethodProductJoinObject)

class Userskillgraphql(graphene.ObjectType):
    user_skill = graphene.List(UserSkillObject)

class Educationindividualjoingraphql(graphene.ObjectType):
    education_individual_join = graphene.List(EducationIndividualJoinObject)

class Pagegraphql(graphene.ObjectType):
    page = graphene.List(PageObject)

class Resumegraphql(graphene.ObjectType):
    resume = graphene.List(ResumeObject)

class Swarmgraphql(graphene.ObjectType):
    swarm = graphene.List(SwarmObject)

class Swarmindividualgraphql(graphene.ObjectType):
    swarm_individual = graphene.List(SwarmIndividualObject)

class Workhistorygraphql(graphene.ObjectType):
    work_history = graphene.List(WorkHistoryObject)

class Workhistoryindividualjoingraphql(graphene.ObjectType):
    work_history_individual_join = graphene.List(WorkHistoryIndividualJoinObject)

class Query(graphene.ObjectType):
    ab_user = graphene.List(ab_userObject)
    ab_register_user = graphene.List(ab_register_userObject)
    ab_permission = graphene.List(ab_permissionObject)
    ab_permission_view = graphene.List(ab_permission_viewObject)
    ab_view_menu = graphene.List(ab_view_menuObject)
    ab_user_role = graphene.List(ab_user_roleObject)
    ab_role = graphene.List(ab_roleObject)
    ab_permission_view_role = graphene.List(ab_permission_view_roleObject)
    brand = graphene.List(brandObject)
    account = graphene.List(accountObject)
    app_table = graphene.List(app_tableObject)
    account_contact = graphene.List(account_contactObject)
    app_column = graphene.List(app_columnObject)
    account_contact_role = graphene.List(account_contact_roleObject)
    account_partner = graphene.List(account_partnerObject)
    attribute_set_translation = graphene.List(attribute_set_translationObject)
    attribute_translation = graphene.List(attribute_translationObject)
    app_relationship = graphene.List(app_relationshipObject)
    attribute_value = graphene.List(attribute_valueObject)
    attribute_value_translation = graphene.List(attribute_value_translationObject)
    billing_frequency = graphene.List(billing_frequencyObject)
    bundle_product = graphene.List(bundle_productObject)
    capture_payment = graphene.List(capture_paymentObject)
    competitor = graphene.List(competitorObject)
    contact_point_addr = graphene.List(contact_point_addrObject)
    contact_point_phone = graphene.List(contact_point_phoneObject)
    contact_point_type = graphene.List(contact_point_typeObject)
    coupon = graphene.List(couponObject)
    credit_tender = graphene.List(credit_tenderObject)
    customer = graphene.List(customerObject)
    customer_state_history = graphene.List(customer_state_historyObject)
    device_user_sesion = graphene.List(device_user_sesionObject)
    goods_product = graphene.List(goods_productObject)
    household = graphene.List(householdObject)
    industry = graphene.List(industryObject)
    internal_busines_unit = graphene.List(internal_busines_unitObject)
    job = graphene.List(jobObject)
    lead = graphene.List(leadObject)
    order_delivery_method = graphene.List(order_delivery_methodObject)
    party = graphene.List(partyObject)
    party_additional_name = graphene.List(party_additional_nameObject)
    party_identification = graphene.List(party_identificationObject)
    party_related_party = graphene.List(party_related_partyObject)
    party_relationship_type = graphene.List(party_relationship_typeObject)
    party_role = graphene.List(party_roleObject)
    party_web_addr = graphene.List(party_web_addrObject)
    payment = graphene.List(paymentObject)
    payment_allocation = graphene.List(payment_allocationObject)
    payment_application = graphene.List(payment_applicationObject)
    payment_authorization = graphene.List(payment_authorizationObject)
    payment_authorization_reversal = graphene.List(payment_authorization_reversalObject)
    payment_card = graphene.List(payment_cardObject)
    payment_credit_memo_allocation = graphene.List(payment_credit_memo_allocationObject)
    payment_credit_memo_application = graphene.List(payment_credit_memo_applicationObject)
    payment_gateway = graphene.List(payment_gatewayObject)
    payment_gateway_auth_reversal_log = graphene.List(payment_gateway_auth_reversal_logObject)
    payment_gateway_authorization_log = graphene.List(payment_gateway_authorization_logObject)
    payment_gateway_interaction_log = graphene.List(payment_gateway_interaction_logObject)
    payment_gateway_interaction_type = graphene.List(payment_gateway_interaction_typeObject)
    payment_gateway_payment_log = graphene.List(payment_gateway_payment_logObject)
    payment_gateway_provider = graphene.List(payment_gateway_providerObject)
    payment_gateway_result_code = graphene.List(payment_gateway_result_codeObject)
    payment_group = graphene.List(payment_groupObject)
    payment_invoice_allocation = graphene.List(payment_invoice_allocationObject)
    payment_invoice_application = graphene.List(payment_invoice_applicationObject)
    payment_method = graphene.List(payment_methodObject)
    payment_method_type = graphene.List(payment_method_typeObject)
    payment_policy = graphene.List(payment_policyObject)
    payment_treatment = graphene.List(payment_treatmentObject)
    payment_treatment_method = graphene.List(payment_treatment_methodObject)
    person_language = graphene.List(person_languageObject)
    person_life_event = graphene.List(person_life_eventObject)
    price_adjustment_group = graphene.List(price_adjustment_groupObject)
    price_adjustment_method = graphene.List(price_adjustment_methodObject)
    price_book_entry = graphene.List(price_book_entryObject)
    product_attribute_set = graphene.List(product_attribute_setObject)
    product_attribute_value = graphene.List(product_attribute_valueObject)
    product_catalog = graphene.List(product_catalogObject)
    product_catalog_translation = graphene.List(product_catalog_translationObject)
    product_category = graphene.List(product_categoryObject)
    product_category_attribute_set = graphene.List(product_category_attribute_setObject)
    product_category_product = graphene.List(product_category_productObject)
    product_category_translation = graphene.List(product_category_translationObject)
    product_collateral = graphene.List(product_collateralObject)
    product_image = graphene.List(product_imageObject)
    product_image_translation = graphene.List(product_image_translationObject)
    product_related_product = graphene.List(product_related_productObject)
    product_relationship_type = graphene.List(product_relationship_typeObject)
    product_translation = graphene.List(product_translationObject)
    product_validity_time_period_uo_m = graphene.List(product_validity_time_period_uo_mObject)
    profilesource = graphene.List(profilesourceObject)
    refund_allocation = graphene.List(refund_allocationObject)
    refund_credit_memo_allocation = graphene.List(refund_credit_memo_allocationObject)
    refund_payment = graphene.List(refund_paymentObject)
    refund_payment_allocation = graphene.List(refund_payment_allocationObject)
    renewal_term = graphene.List(renewal_termObject)
    sales_channel = graphene.List(sales_channelObject)
    sales_channel_type = graphene.List(sales_channel_typeObject)
    sales_order = graphene.List(sales_orderObject)
    sales_order_change_log = graphene.List(sales_order_change_logObject)
    sales_order_change_type = graphene.List(sales_order_change_typeObject)
    sales_order_confirmation_state = graphene.List(sales_order_confirmation_stateObject)
    sales_order_delivery_group = graphene.List(sales_order_delivery_groupObject)
    sales_order_delivery_state = graphene.List(sales_order_delivery_stateObject)
    sales_order_payment_summary = graphene.List(sales_order_payment_summaryObject)
    sales_order_price_adjustment = graphene.List(sales_order_price_adjustmentObject)
    sales_order_price_adjustment_type = graphene.List(sales_order_price_adjustment_typeObject)
    sales_order_product = graphene.List(sales_order_productObject)
    sales_order_product_group = graphene.List(sales_order_product_groupObject)
    sales_order_product_group_type = graphene.List(sales_order_product_group_typeObject)
    sales_order_product_note = graphene.List(sales_order_product_noteObject)
    sales_order_product_reason = graphene.List(sales_order_product_reasonObject)
    sales_order_product_reason_category = graphene.List(sales_order_product_reason_categoryObject)
    sales_order_product_state = graphene.List(sales_order_product_stateObject)
    sales_order_product_tax = graphene.List(sales_order_product_taxObject)
    sales_order_segment = graphene.List(sales_order_segmentObject)
    sales_order_state = graphene.List(sales_order_stateObject)
    sales_order_tax = graphene.List(sales_order_taxObject)
    sales_order_type = graphene.List(sales_order_typeObject)
    seller = graphene.List(sellerObject)
    service_product = graphene.List(service_productObject)
    shipment = graphene.List(shipmentObject)
    shipment_document = graphene.List(shipment_documentObject)
    shipment_package = graphene.List(shipment_packageObject)
    shipment_product = graphene.List(shipment_productObject)
    shipment_product_price_adjustment = graphene.List(shipment_product_price_adjustmentObject)
    shipment_product_price_adjustment_tax = graphene.List(shipment_product_price_adjustment_taxObject)
    shipment_state = graphene.List(shipment_stateObject)
    shipping_method = graphene.List(shipping_methodObject)
    skill = graphene.List(skillObject)
    supplier = graphene.List(supplierObject)
    uncategorized_party = graphene.List(uncategorized_partyObject)
    userx = graphene.List(userxObject)
    account_auto_payment_method_join = graphene.List(account_auto_payment_method_joinObject)
    account_bill_frequency_join = graphene.List(account_bill_frequency_joinObject)
    account_contact_account_join = graphene.List(account_contact_account_joinObject)
    account_contact_indirect_relation_account_contact_join = graphene.List(account_contact_indirect_relation_account_contact_joinObject)
    account_contact_reports_to_account_contact_join = graphene.List(account_contact_reports_to_account_contact_joinObject)
    account_contact_role_account_contact_join = graphene.List(account_contact_role_account_contact_joinObject)
    account_order_delivery_method_join = graphene.List(account_order_delivery_method_joinObject)
    account_parent_account_join = graphene.List(account_parent_account_joinObject)
    account_partner_account_join = graphene.List(account_partner_account_joinObject)
    account_partner_partner_account_join = graphene.List(account_partner_partner_account_joinObject)
    account_party_join = graphene.List(account_party_joinObject)
    account_party_role_join = graphene.List(account_party_role_joinObject)
    account_primary_sales_contact_point_join = graphene.List(account_primary_sales_contact_point_joinObject)
    account_shipping_contact_join = graphene.List(account_shipping_contact_joinObject)
    account_shipping_email_join = graphene.List(account_shipping_email_joinObject)
    account_shipping_phoneid_join = graphene.List(account_shipping_phoneid_joinObject)
    attribute_value_translation_attribute_value_join = graphene.List(attribute_value_translation_attribute_value_joinObject)
    bundle_product_brand_join = graphene.List(bundle_product_brand_joinObject)
    bundle_product_primary_product_category_join = graphene.List(bundle_product_primary_product_category_joinObject)
    bundle_product_primary_sales_channel_join = graphene.List(bundle_product_primary_sales_channel_joinObject)
    bundle_product_valid_for_period_uo_m_join = graphene.List(bundle_product_valid_for_period_uo_m_joinObject)
    capture_payment_account_join = graphene.List(capture_payment_account_joinObject)
    capture_payment_internal_busines_unit_join = graphene.List(capture_payment_internal_busines_unit_joinObject)
    capture_payment_latest_gateway_result_code_join = graphene.List(capture_payment_latest_gateway_result_code_joinObject)
    capture_payment_payment_authorization_join = graphene.List(capture_payment_payment_authorization_joinObject)
    capture_payment_payment_gateway_join = graphene.List(capture_payment_payment_gateway_joinObject)
    capture_payment_payment_group_join = graphene.List(capture_payment_payment_group_joinObject)
    capture_payment_payment_method_join = graphene.List(capture_payment_payment_method_joinObject)
    capture_payment_payment_treatment_join = graphene.List(capture_payment_payment_treatment_joinObject)
    capture_payment_sales_order_payment_summary_join = graphene.List(capture_payment_sales_order_payment_summary_joinObject)
    competitor_party_join = graphene.List(competitor_party_joinObject)
    coupon_manufacturer_join = graphene.List(coupon_manufacturer_joinObject)
    coupon_payment_method_type_join = graphene.List(coupon_payment_method_type_joinObject)
    credit_tender_account_join = graphene.List(credit_tender_account_joinObject)
    credit_tender_payment_method_type_join = graphene.List(credit_tender_payment_method_type_joinObject)
    customer_party_join = graphene.List(customer_party_joinObject)
    customer_state_history_party_role_join = graphene.List(customer_state_history_party_role_joinObject)
    goods_product_brand_join = graphene.List(goods_product_brand_joinObject)
    goods_product_primary_product_category_join = graphene.List(goods_product_primary_product_category_joinObject)
    goods_product_primary_sales_channel_join = graphene.List(goods_product_primary_sales_channel_joinObject)
    goods_product_valid_for_period_uo_m_join = graphene.List(goods_product_valid_for_period_uo_m_joinObject)
    household_primary_account_join = graphene.List(household_primary_account_joinObject)
    individual = graphene.List(individualObject)
    industry_job = graphene.List(industry_jobObject)
    internal_busines_unit_parent_internal_busines_unit_join = graphene.List(internal_busines_unit_parent_internal_busines_unit_joinObject)
    internal_busines_unit_primary_account_join = graphene.List(internal_busines_unit_primary_account_joinObject)
    job_skill = graphene.List(job_skillObject)
    lead_converted_to_account_contact_join = graphene.List(lead_converted_to_account_contact_joinObject)
    lead_converted_to_account_join = graphene.List(lead_converted_to_account_joinObject)
    lead_fax_contact_phone_join = graphene.List(lead_fax_contact_phone_joinObject)
    lead_mobile_contact_phone_join = graphene.List(lead_mobile_contact_phone_joinObject)
    lead_partner_account_join = graphene.List(lead_partner_account_joinObject)
    lead_party_role_join = graphene.List(lead_party_role_joinObject)
    party_additional_name_party_join = graphene.List(party_additional_name_party_joinObject)
    party_identification_party_join = graphene.List(party_identification_party_joinObject)
    party_identification_party_role_join = graphene.List(party_identification_party_role_joinObject)
    party_primary_account_join = graphene.List(party_primary_account_joinObject)
    party_related_party_party_join = graphene.List(party_related_party_party_joinObject)
    party_related_party_party_relationship_type_join = graphene.List(party_related_party_party_relationship_type_joinObject)
    party_related_party_related_party_join = graphene.List(party_related_party_related_party_joinObject)
    party_role_party_join = graphene.List(party_role_party_joinObject)
    party_web_addr_party_join = graphene.List(party_web_addr_party_joinObject)
    party_web_addr_party_role_join = graphene.List(party_web_addr_party_role_joinObject)
    pay_gat_aut_log_pay_gat_int_typ_join = graphene.List(pay_gat_aut_log_pay_gat_int_typ_joinObject)
    pay_gat_aut_rev_log_pay_aut_rev_join = graphene.List(pay_gat_aut_rev_log_pay_aut_rev_joinObject)
    pay_gat_aut_rev_log_pay_gat_int_typ_join = graphene.List(pay_gat_aut_rev_log_pay_gat_int_typ_joinObject)
    pay_gat_int_log_pay_gat_int_typ_join = graphene.List(pay_gat_int_log_pay_gat_int_typ_joinObject)
    pay_gat_pay_log_pay_gat_int_typ_join = graphene.List(pay_gat_pay_log_pay_gat_int_typ_joinObject)
    payment_account_join = graphene.List(payment_account_joinObject)
    payment_allocation_related_payment_allocation_join = graphene.List(payment_allocation_related_payment_allocation_joinObject)
    payment_application_payment_join = graphene.List(payment_application_payment_joinObject)
    payment_authorization_payment_gateway_join = graphene.List(payment_authorization_payment_gateway_joinObject)
    payment_authorization_payment_gateway_result_join = graphene.List(payment_authorization_payment_gateway_result_joinObject)
    payment_authorization_payment_group_join = graphene.List(payment_authorization_payment_group_joinObject)
    payment_authorization_payment_method_join = graphene.List(payment_authorization_payment_method_joinObject)
    payment_authorization_reversal_capture_payment_join = graphene.List(payment_authorization_reversal_capture_payment_joinObject)
    payment_authorization_reversal_payment_authorization_join = graphene.List(payment_authorization_reversal_payment_authorization_joinObject)
    payment_authorization_reversal_payment_gateway_result_join = graphene.List(payment_authorization_reversal_payment_gateway_result_joinObject)
    payment_authorization_sales_order_payment_summary_join = graphene.List(payment_authorization_sales_order_payment_summary_joinObject)
    payment_card_payment_method_type_join = graphene.List(payment_card_payment_method_type_joinObject)
    payment_credit_memo_allocation_related_payment_allocation_join = graphene.List(payment_credit_memo_allocation_related_payment_allocation_joinObject)
    payment_credit_memo_application_payment_join = graphene.List(payment_credit_memo_application_payment_joinObject)
    payment_gateway_auth_reversal_log_payment_gateway_result_join = graphene.List(payment_gateway_auth_reversal_log_payment_gateway_result_joinObject)
    payment_gateway_authorization_log_payment_authorization_join = graphene.List(payment_gateway_authorization_log_payment_authorization_joinObject)
    payment_gateway_authorization_log_payment_gateway_result_join = graphene.List(payment_gateway_authorization_log_payment_gateway_result_joinObject)
    payment_gateway_interaction_log_payment_gateway_result_join = graphene.List(payment_gateway_interaction_log_payment_gateway_result_joinObject)
    payment_gateway_payment_gateway_provider_join = graphene.List(payment_gateway_payment_gateway_provider_joinObject)
    payment_gateway_payment_log_payment_gateway_result_join = graphene.List(payment_gateway_payment_log_payment_gateway_result_joinObject)
    payment_gateway_payment_log_payment_join = graphene.List(payment_gateway_payment_log_payment_joinObject)
    payment_internal_busines_unit_join = graphene.List(payment_internal_busines_unit_joinObject)
    payment_invoice_allocation_payment_invoice_application_join = graphene.List(payment_invoice_allocation_payment_invoice_application_joinObject)
    payment_invoice_allocation_related_payment_allocation_join = graphene.List(payment_invoice_allocation_related_payment_allocation_joinObject)
    payment_invoice_application_payment_join = graphene.List(payment_invoice_application_payment_joinObject)
    payment_latest_gateway_result_code_join = graphene.List(payment_latest_gateway_result_code_joinObject)
    payment_method_payment_method_type_join = graphene.List(payment_method_payment_method_type_joinObject)
    payment_payment_gateway_join = graphene.List(payment_payment_gateway_joinObject)
    payment_payment_group_join = graphene.List(payment_payment_group_joinObject)
    payment_payment_method_join = graphene.List(payment_payment_method_joinObject)
    payment_payment_treatment_join = graphene.List(payment_payment_treatment_joinObject)
    payment_sales_order_payment_summary_join = graphene.List(payment_sales_order_payment_summary_joinObject)
    payment_treatment_payment_policy_join = graphene.List(payment_treatment_payment_policy_joinObject)
    payment_treatment_payment_treatment_method_join = graphene.List(payment_treatment_payment_treatment_method_joinObject)
    product = graphene.List(productObject)
    product_attribute_value_attribute_value_join = graphene.List(product_attribute_value_attribute_value_joinObject)
    product_catalog_translation_product_catalog_join = graphene.List(product_catalog_translation_product_catalog_joinObject)
    product_category_attribute_set_product_category_join = graphene.List(product_category_attribute_set_product_category_joinObject)
    product_category_parent_category_join = graphene.List(product_category_parent_category_joinObject)
    product_category_product_catalog_join = graphene.List(product_category_product_catalog_joinObject)
    product_category_product_product_category_join = graphene.List(product_category_product_product_category_joinObject)
    product_category_translation_product_category_join = graphene.List(product_category_translation_product_category_joinObject)
    product_image_translation_product_image_join = graphene.List(product_image_translation_product_image_joinObject)
    product_related_product_product_relationship_type_join = graphene.List(product_related_product_product_relationship_type_joinObject)
    product_related_product_sales_order_product1_join = graphene.List(product_related_product_sales_order_product1_joinObject)
    product_related_product_sales_order_product2_join = graphene.List(product_related_product_sales_order_product2_joinObject)
    refund_allocation_refund_payment_join = graphene.List(refund_allocation_refund_payment_joinObject)
    refund_allocation_related_refund_allocation_join = graphene.List(refund_allocation_related_refund_allocation_joinObject)
    refund_credit_memo_allocation_refund_payment_join = graphene.List(refund_credit_memo_allocation_refund_payment_joinObject)
    refund_credit_memo_allocation_related_refund_allocation_join = graphene.List(refund_credit_memo_allocation_related_refund_allocation_joinObject)
    refund_payment_account_join = graphene.List(refund_payment_account_joinObject)
    refund_payment_allocation_capture_payment_join = graphene.List(refund_payment_allocation_capture_payment_joinObject)
    refund_payment_allocation_refund_payment_join = graphene.List(refund_payment_allocation_refund_payment_joinObject)
    refund_payment_allocation_related_refund_allocation_join = graphene.List(refund_payment_allocation_related_refund_allocation_joinObject)
    refund_payment_internal_busines_unit_join = graphene.List(refund_payment_internal_busines_unit_joinObject)
    refund_payment_latest_gateway_result_code_join = graphene.List(refund_payment_latest_gateway_result_code_joinObject)
    refund_payment_payment_gateway_join = graphene.List(refund_payment_payment_gateway_joinObject)
    refund_payment_payment_group_join = graphene.List(refund_payment_payment_group_joinObject)
    refund_payment_payment_method_join = graphene.List(refund_payment_payment_method_joinObject)
    refund_payment_payment_treatment_join = graphene.List(refund_payment_payment_treatment_joinObject)
    refund_payment_sales_order_payment_summary_join = graphene.List(refund_payment_sales_order_payment_summary_joinObject)
    sal_ord_pro_rea_sal_ord_pro_rea_cat_join = graphene.List(sal_ord_pro_rea_sal_ord_pro_rea_cat_joinObject)
    sales_channel_sales_channel_type_join = graphene.List(sales_channel_sales_channel_type_joinObject)
    sales_order_bill_to_account_join = graphene.List(sales_order_bill_to_account_joinObject)
    sales_order_bill_to_addr_join = graphene.List(sales_order_bill_to_addr_joinObject)
    sales_order_bill_to_contact_join = graphene.List(sales_order_bill_to_contact_joinObject)
    sales_order_bill_to_email_join = graphene.List(sales_order_bill_to_email_joinObject)
    sales_order_bill_to_phone_number_join = graphene.List(sales_order_bill_to_phone_number_joinObject)
    sales_order_change_log_change_sales_order_join = graphene.List(sales_order_change_log_change_sales_order_joinObject)
    sales_order_change_log_change_sales_order_product_join = graphene.List(sales_order_change_log_change_sales_order_product_joinObject)
    sales_order_change_log_related_sales_order_join = graphene.List(sales_order_change_log_related_sales_order_joinObject)
    sales_order_change_log_related_sales_order_product_join = graphene.List(sales_order_change_log_related_sales_order_product_joinObject)
    sales_order_delivery_group_account_contact_join = graphene.List(sales_order_delivery_group_account_contact_joinObject)
    sales_order_delivery_group_contact_point_addr_join = graphene.List(sales_order_delivery_group_contact_point_addr_joinObject)
    sales_order_delivery_group_order_delivery_method_join = graphene.List(sales_order_delivery_group_order_delivery_method_joinObject)
    sales_order_delivery_group_original_delivery_group_join = graphene.List(sales_order_delivery_group_original_delivery_group_joinObject)
    sales_order_delivery_group_sales_order_delivery_state_join = graphene.List(sales_order_delivery_group_sales_order_delivery_state_joinObject)
    sales_order_delivery_group_sales_order_join = graphene.List(sales_order_delivery_group_sales_order_joinObject)
    sales_order_internal_busines_unit_join = graphene.List(sales_order_internal_busines_unit_joinObject)
    sales_order_original_order_join = graphene.List(sales_order_original_order_joinObject)
    sales_order_payment_method_join = graphene.List(sales_order_payment_method_joinObject)
    sales_order_payment_summary_payment_method_join = graphene.List(sales_order_payment_summary_payment_method_joinObject)
    sales_order_payment_summary_sales_order_join = graphene.List(sales_order_payment_summary_sales_order_joinObject)
    sales_order_price_adjustment_sales_order_join = graphene.List(sales_order_price_adjustment_sales_order_joinObject)
    sales_order_product_group_sales_order_product_group_type_join = graphene.List(sales_order_product_group_sales_order_product_group_type_joinObject)
    sales_order_product_list_price_term_uo_m_join = graphene.List(sales_order_product_list_price_term_uo_m_joinObject)
    sales_order_product_original_order_product_join = graphene.List(sales_order_product_original_order_product_joinObject)
    sales_order_product_price_book_entry_join = graphene.List(sales_order_product_price_book_entry_joinObject)
    sales_order_product_sales_order_delivery_group_join = graphene.List(sales_order_product_sales_order_delivery_group_joinObject)
    sales_order_product_sales_order_join = graphene.List(sales_order_product_sales_order_joinObject)
    sales_order_product_sales_order_product_reason_join = graphene.List(sales_order_product_sales_order_product_reason_joinObject)
    sales_order_product_sales_order_product_state_join = graphene.List(sales_order_product_sales_order_product_state_joinObject)
    sales_order_product_seller_account_join = graphene.List(sales_order_product_seller_account_joinObject)
    sales_order_product_shipping_addr_join = graphene.List(sales_order_product_shipping_addr_joinObject)
    sales_order_product_shipping_email_join = graphene.List(sales_order_product_shipping_email_joinObject)
    sales_order_product_shipping_phone_join = graphene.List(sales_order_product_shipping_phone_joinObject)
    sales_order_product_subscription_term_unit_join = graphene.List(sales_order_product_subscription_term_unit_joinObject)
    sales_order_product_tax_original_sales_order_product_tax_join = graphene.List(sales_order_product_tax_original_sales_order_product_tax_joinObject)
    sales_order_product_tax_sales_order_product_join = graphene.List(sales_order_product_tax_sales_order_product_joinObject)
    sales_order_renewal_term_join = graphene.List(sales_order_renewal_term_joinObject)
    sales_order_sales_channel_join = graphene.List(sales_order_sales_channel_joinObject)
    sales_order_sales_order_confirmation_state_join = graphene.List(sales_order_sales_order_confirmation_state_joinObject)
    sales_order_sales_order_state_join = graphene.List(sales_order_sales_order_state_joinObject)
    sales_order_sales_order_type_join = graphene.List(sales_order_sales_order_type_joinObject)
    sales_order_seller_join = graphene.List(sales_order_seller_joinObject)
    sales_order_ship_to_addr_join = graphene.List(sales_order_ship_to_addr_joinObject)
    sales_order_ship_to_contact_join = graphene.List(sales_order_ship_to_contact_joinObject)
    sales_order_ship_to_email_join = graphene.List(sales_order_ship_to_email_joinObject)
    sales_order_sold_to_customer_join = graphene.List(sales_order_sold_to_customer_joinObject)
    sales_order_user_device_sesion_join = graphene.List(sales_order_user_device_sesion_joinObject)
    seller_party_join = graphene.List(seller_party_joinObject)
    service_product_brand_join = graphene.List(service_product_brand_joinObject)
    service_product_primary_product_category_join = graphene.List(service_product_primary_product_category_joinObject)
    service_product_primary_sales_channel_join = graphene.List(service_product_primary_sales_channel_joinObject)
    service_product_service_provider_account_join = graphene.List(service_product_service_provider_account_joinObject)
    service_product_valid_for_period_uo_m_join = graphene.List(service_product_valid_for_period_uo_m_joinObject)
    shi_pro_pri_adj_tax_shi_pro_pri_adj_join = graphene.List(shi_pro_pri_adj_tax_shi_pro_pri_adj_joinObject)
    shipment_document_shipment_join = graphene.List(shipment_document_shipment_joinObject)
    shipment_package_shipment_join = graphene.List(shipment_package_shipment_joinObject)
    shipment_product_price_adjustment_shipment_product_join = graphene.List(shipment_product_price_adjustment_shipment_product_joinObject)
    shipment_product_sales_order_product_join = graphene.List(shipment_product_sales_order_product_joinObject)
    shipment_product_shipment_join = graphene.List(shipment_product_shipment_joinObject)
    shipment_product_shipment_package_join = graphene.List(shipment_product_shipment_package_joinObject)
    shipment_sales_order_delivery_group_join = graphene.List(shipment_sales_order_delivery_group_joinObject)
    shipment_sales_order_join = graphene.List(shipment_sales_order_joinObject)
    shipment_ship_to_addr_join = graphene.List(shipment_ship_to_addr_joinObject)
    shipment_shipment_state_join = graphene.List(shipment_shipment_state_joinObject)
    supplier_party_join = graphene.List(supplier_party_joinObject)
    uncategorized_party_primary_account_join = graphene.List(uncategorized_party_primary_account_joinObject)
    account_contact_individual_join = graphene.List(account_contact_individual_joinObject)
    bundle_product_master_product_join = graphene.List(bundle_product_master_product_joinObject)
    education = graphene.List(educationObject)
    goods_product_master_product_join = graphene.List(goods_product_master_product_joinObject)
    individual_primary_account_join = graphene.List(individual_primary_account_joinObject)
    individual_primary_household_join = graphene.List(individual_primary_household_joinObject)
    job_individual = graphene.List(job_individualObject)
    location = graphene.List(locationObject)
    order_delivery_method_product_join = graphene.List(order_delivery_method_product_joinObject)
    person_language_individual_join = graphene.List(person_language_individual_joinObject)
    person_life_event_individual_join = graphene.List(person_life_event_individual_joinObject)
    portal = graphene.List(portalObject)
    price_book_entry_product_join = graphene.List(price_book_entry_product_joinObject)
    product_attribute_set_product_join = graphene.List(product_attribute_set_product_joinObject)
    product_attribute_value_product_join = graphene.List(product_attribute_value_product_joinObject)
    product_brand_join = graphene.List(product_brand_joinObject)
    product_category_product_product_join = graphene.List(product_category_product_product_joinObject)
    product_collateral_product_join = graphene.List(product_collateral_product_joinObject)
    product_image_product_join = graphene.List(product_image_product_joinObject)
    product_master_product_join = graphene.List(product_master_product_joinObject)
    product_primary_product_category_join = graphene.List(product_primary_product_category_joinObject)
    product_primary_sales_channel_join = graphene.List(product_primary_sales_channel_joinObject)
    product_related_product_child_product_join = graphene.List(product_related_product_child_product_joinObject)
    product_related_product_parent_product_join = graphene.List(product_related_product_parent_product_joinObject)
    product_translation_product_join = graphene.List(product_translation_product_joinObject)
    product_valid_for_period_uo_m_join = graphene.List(product_valid_for_period_uo_m_joinObject)
    profile = graphene.List(profileObject)
    sales_order_product_product_join = graphene.List(sales_order_product_product_joinObject)
    service_product_master_product_join = graphene.List(service_product_master_product_joinObject)
    shipment_product_product_join = graphene.List(shipment_product_product_joinObject)
    shipping_method_product_join = graphene.List(shipping_method_product_joinObject)
    user_skill = graphene.List(user_skillObject)
    education_individual_join = graphene.List(education_individual_joinObject)
    page = graphene.List(pageObject)
    resume = graphene.List(resumeObject)
    swarm = graphene.List(swarmObject)
    swarm_individual = graphene.List(swarm_individualObject)
    work_history = graphene.List(work_historyObject)
    work_history_individual_join = graphene.List(work_history_individual_joinObject)

    def resolve_ab_user(self, info):
        return ab_user.query.all()

    def resolve_ab_register_user(self, info):
        return ab_register_user.query.all()

    def resolve_ab_permission(self, info):
        return ab_permission.query.all()

    def resolve_ab_permission_view(self, info):
        return ab_permission_view.query.all()

    def resolve_ab_view_menu(self, info):
        return ab_view_menu.query.all()

    def resolve_ab_user_role(self, info):
        return ab_user_role.query.all()

    def resolve_ab_role(self, info):
        return ab_role.query.all()

    def resolve_ab_permission_view_role(self, info):
        return ab_permission_view_role.query.all()

    def resolve_brand(self, info):
        return brand.query.all()

    def resolve_account(self, info):
        return account.query.all()

    def resolve_app_table(self, info):
        return app_table.query.all()

    def resolve_account_contact(self, info):
        return account_contact.query.all()

    def resolve_app_column(self, info):
        return app_column.query.all()

    def resolve_account_contact_role(self, info):
        return account_contact_role.query.all()

    def resolve_account_partner(self, info):
        return account_partner.query.all()

    def resolve_attribute_set_translation(self, info):
        return attribute_set_translation.query.all()

    def resolve_attribute_translation(self, info):
        return attribute_translation.query.all()

    def resolve_app_relationship(self, info):
        return app_relationship.query.all()

    def resolve_attribute_value(self, info):
        return attribute_value.query.all()

    def resolve_attribute_value_translation(self, info):
        return attribute_value_translation.query.all()

    def resolve_billing_frequency(self, info):
        return billing_frequency.query.all()

    def resolve_bundle_product(self, info):
        return bundle_product.query.all()

    def resolve_capture_payment(self, info):
        return capture_payment.query.all()

    def resolve_competitor(self, info):
        return competitor.query.all()

    def resolve_contact_point_addr(self, info):
        return contact_point_addr.query.all()

    def resolve_contact_point_phone(self, info):
        return contact_point_phone.query.all()

    def resolve_contact_point_type(self, info):
        return contact_point_type.query.all()

    def resolve_coupon(self, info):
        return coupon.query.all()

    def resolve_credit_tender(self, info):
        return credit_tender.query.all()

    def resolve_customer(self, info):
        return customer.query.all()

    def resolve_customer_state_history(self, info):
        return customer_state_history.query.all()

    def resolve_device_user_sesion(self, info):
        return device_user_sesion.query.all()

    def resolve_goods_product(self, info):
        return goods_product.query.all()

    def resolve_household(self, info):
        return household.query.all()

    def resolve_industry(self, info):
        return industry.query.all()

    def resolve_internal_busines_unit(self, info):
        return internal_busines_unit.query.all()

    def resolve_job(self, info):
        return job.query.all()

    def resolve_lead(self, info):
        return lead.query.all()

    def resolve_order_delivery_method(self, info):
        return order_delivery_method.query.all()

    def resolve_party(self, info):
        return party.query.all()

    def resolve_party_additional_name(self, info):
        return party_additional_name.query.all()

    def resolve_party_identification(self, info):
        return party_identification.query.all()

    def resolve_party_related_party(self, info):
        return party_related_party.query.all()

    def resolve_party_relationship_type(self, info):
        return party_relationship_type.query.all()

    def resolve_party_role(self, info):
        return party_role.query.all()

    def resolve_party_web_addr(self, info):
        return party_web_addr.query.all()

    def resolve_payment(self, info):
        return payment.query.all()

    def resolve_payment_allocation(self, info):
        return payment_allocation.query.all()

    def resolve_payment_application(self, info):
        return payment_application.query.all()

    def resolve_payment_authorization(self, info):
        return payment_authorization.query.all()

    def resolve_payment_authorization_reversal(self, info):
        return payment_authorization_reversal.query.all()

    def resolve_payment_card(self, info):
        return payment_card.query.all()

    def resolve_payment_credit_memo_allocation(self, info):
        return payment_credit_memo_allocation.query.all()

    def resolve_payment_credit_memo_application(self, info):
        return payment_credit_memo_application.query.all()

    def resolve_payment_gateway(self, info):
        return payment_gateway.query.all()

    def resolve_payment_gateway_auth_reversal_log(self, info):
        return payment_gateway_auth_reversal_log.query.all()

    def resolve_payment_gateway_authorization_log(self, info):
        return payment_gateway_authorization_log.query.all()

    def resolve_payment_gateway_interaction_log(self, info):
        return payment_gateway_interaction_log.query.all()

    def resolve_payment_gateway_interaction_type(self, info):
        return payment_gateway_interaction_type.query.all()

    def resolve_payment_gateway_payment_log(self, info):
        return payment_gateway_payment_log.query.all()

    def resolve_payment_gateway_provider(self, info):
        return payment_gateway_provider.query.all()

    def resolve_payment_gateway_result_code(self, info):
        return payment_gateway_result_code.query.all()

    def resolve_payment_group(self, info):
        return payment_group.query.all()

    def resolve_payment_invoice_allocation(self, info):
        return payment_invoice_allocation.query.all()

    def resolve_payment_invoice_application(self, info):
        return payment_invoice_application.query.all()

    def resolve_payment_method(self, info):
        return payment_method.query.all()

    def resolve_payment_method_type(self, info):
        return payment_method_type.query.all()

    def resolve_payment_policy(self, info):
        return payment_policy.query.all()

    def resolve_payment_treatment(self, info):
        return payment_treatment.query.all()

    def resolve_payment_treatment_method(self, info):
        return payment_treatment_method.query.all()

    def resolve_person_language(self, info):
        return person_language.query.all()

    def resolve_person_life_event(self, info):
        return person_life_event.query.all()

    def resolve_price_adjustment_group(self, info):
        return price_adjustment_group.query.all()

    def resolve_price_adjustment_method(self, info):
        return price_adjustment_method.query.all()

    def resolve_price_book_entry(self, info):
        return price_book_entry.query.all()

    def resolve_product_attribute_set(self, info):
        return product_attribute_set.query.all()

    def resolve_product_attribute_value(self, info):
        return product_attribute_value.query.all()

    def resolve_product_catalog(self, info):
        return product_catalog.query.all()

    def resolve_product_catalog_translation(self, info):
        return product_catalog_translation.query.all()

    def resolve_product_category(self, info):
        return product_category.query.all()

    def resolve_product_category_attribute_set(self, info):
        return product_category_attribute_set.query.all()

    def resolve_product_category_product(self, info):
        return product_category_product.query.all()

    def resolve_product_category_translation(self, info):
        return product_category_translation.query.all()

    def resolve_product_collateral(self, info):
        return product_collateral.query.all()

    def resolve_product_image(self, info):
        return product_image.query.all()

    def resolve_product_image_translation(self, info):
        return product_image_translation.query.all()

    def resolve_product_related_product(self, info):
        return product_related_product.query.all()

    def resolve_product_relationship_type(self, info):
        return product_relationship_type.query.all()

    def resolve_product_translation(self, info):
        return product_translation.query.all()

    def resolve_product_validity_time_period_uo_m(self, info):
        return product_validity_time_period_uo_m.query.all()

    def resolve_profilesource(self, info):
        return profilesource.query.all()

    def resolve_refund_allocation(self, info):
        return refund_allocation.query.all()

    def resolve_refund_credit_memo_allocation(self, info):
        return refund_credit_memo_allocation.query.all()

    def resolve_refund_payment(self, info):
        return refund_payment.query.all()

    def resolve_refund_payment_allocation(self, info):
        return refund_payment_allocation.query.all()

    def resolve_renewal_term(self, info):
        return renewal_term.query.all()

    def resolve_sales_channel(self, info):
        return sales_channel.query.all()

    def resolve_sales_channel_type(self, info):
        return sales_channel_type.query.all()

    def resolve_sales_order(self, info):
        return sales_order.query.all()

    def resolve_sales_order_change_log(self, info):
        return sales_order_change_log.query.all()

    def resolve_sales_order_change_type(self, info):
        return sales_order_change_type.query.all()

    def resolve_sales_order_confirmation_state(self, info):
        return sales_order_confirmation_state.query.all()

    def resolve_sales_order_delivery_group(self, info):
        return sales_order_delivery_group.query.all()

    def resolve_sales_order_delivery_state(self, info):
        return sales_order_delivery_state.query.all()

    def resolve_sales_order_payment_summary(self, info):
        return sales_order_payment_summary.query.all()

    def resolve_sales_order_price_adjustment(self, info):
        return sales_order_price_adjustment.query.all()

    def resolve_sales_order_price_adjustment_type(self, info):
        return sales_order_price_adjustment_type.query.all()

    def resolve_sales_order_product(self, info):
        return sales_order_product.query.all()

    def resolve_sales_order_product_group(self, info):
        return sales_order_product_group.query.all()

    def resolve_sales_order_product_group_type(self, info):
        return sales_order_product_group_type.query.all()

    def resolve_sales_order_product_note(self, info):
        return sales_order_product_note.query.all()

    def resolve_sales_order_product_reason(self, info):
        return sales_order_product_reason.query.all()

    def resolve_sales_order_product_reason_category(self, info):
        return sales_order_product_reason_category.query.all()

    def resolve_sales_order_product_state(self, info):
        return sales_order_product_state.query.all()

    def resolve_sales_order_product_tax(self, info):
        return sales_order_product_tax.query.all()

    def resolve_sales_order_segment(self, info):
        return sales_order_segment.query.all()

    def resolve_sales_order_state(self, info):
        return sales_order_state.query.all()

    def resolve_sales_order_tax(self, info):
        return sales_order_tax.query.all()

    def resolve_sales_order_type(self, info):
        return sales_order_type.query.all()

    def resolve_seller(self, info):
        return seller.query.all()

    def resolve_service_product(self, info):
        return service_product.query.all()

    def resolve_shipment(self, info):
        return shipment.query.all()

    def resolve_shipment_document(self, info):
        return shipment_document.query.all()

    def resolve_shipment_package(self, info):
        return shipment_package.query.all()

    def resolve_shipment_product(self, info):
        return shipment_product.query.all()

    def resolve_shipment_product_price_adjustment(self, info):
        return shipment_product_price_adjustment.query.all()

    def resolve_shipment_product_price_adjustment_tax(self, info):
        return shipment_product_price_adjustment_tax.query.all()

    def resolve_shipment_state(self, info):
        return shipment_state.query.all()

    def resolve_shipping_method(self, info):
        return shipping_method.query.all()

    def resolve_skill(self, info):
        return skill.query.all()

    def resolve_supplier(self, info):
        return supplier.query.all()

    def resolve_uncategorized_party(self, info):
        return uncategorized_party.query.all()

    def resolve_userx(self, info):
        return userx.query.all()

    def resolve_account_auto_payment_method_join(self, info):
        return account_auto_payment_method_join.query.all()

    def resolve_account_bill_frequency_join(self, info):
        return account_bill_frequency_join.query.all()

    def resolve_account_contact_account_join(self, info):
        return account_contact_account_join.query.all()

    def resolve_account_contact_indirect_relation_account_contact_join(self, info):
        return account_contact_indirect_relation_account_contact_join.query.all()

    def resolve_account_contact_reports_to_account_contact_join(self, info):
        return account_contact_reports_to_account_contact_join.query.all()

    def resolve_account_contact_role_account_contact_join(self, info):
        return account_contact_role_account_contact_join.query.all()

    def resolve_account_order_delivery_method_join(self, info):
        return account_order_delivery_method_join.query.all()

    def resolve_account_parent_account_join(self, info):
        return account_parent_account_join.query.all()

    def resolve_account_partner_account_join(self, info):
        return account_partner_account_join.query.all()

    def resolve_account_partner_partner_account_join(self, info):
        return account_partner_partner_account_join.query.all()

    def resolve_account_party_join(self, info):
        return account_party_join.query.all()

    def resolve_account_party_role_join(self, info):
        return account_party_role_join.query.all()

    def resolve_account_primary_sales_contact_point_join(self, info):
        return account_primary_sales_contact_point_join.query.all()

    def resolve_account_shipping_contact_join(self, info):
        return account_shipping_contact_join.query.all()

    def resolve_account_shipping_email_join(self, info):
        return account_shipping_email_join.query.all()

    def resolve_account_shipping_phoneid_join(self, info):
        return account_shipping_phoneid_join.query.all()

    def resolve_attribute_value_translation_attribute_value_join(self, info):
        return attribute_value_translation_attribute_value_join.query.all()

    def resolve_bundle_product_brand_join(self, info):
        return bundle_product_brand_join.query.all()

    def resolve_bundle_product_primary_product_category_join(self, info):
        return bundle_product_primary_product_category_join.query.all()

    def resolve_bundle_product_primary_sales_channel_join(self, info):
        return bundle_product_primary_sales_channel_join.query.all()

    def resolve_bundle_product_valid_for_period_uo_m_join(self, info):
        return bundle_product_valid_for_period_uo_m_join.query.all()

    def resolve_capture_payment_account_join(self, info):
        return capture_payment_account_join.query.all()

    def resolve_capture_payment_internal_busines_unit_join(self, info):
        return capture_payment_internal_busines_unit_join.query.all()

    def resolve_capture_payment_latest_gateway_result_code_join(self, info):
        return capture_payment_latest_gateway_result_code_join.query.all()

    def resolve_capture_payment_payment_authorization_join(self, info):
        return capture_payment_payment_authorization_join.query.all()

    def resolve_capture_payment_payment_gateway_join(self, info):
        return capture_payment_payment_gateway_join.query.all()

    def resolve_capture_payment_payment_group_join(self, info):
        return capture_payment_payment_group_join.query.all()

    def resolve_capture_payment_payment_method_join(self, info):
        return capture_payment_payment_method_join.query.all()

    def resolve_capture_payment_payment_treatment_join(self, info):
        return capture_payment_payment_treatment_join.query.all()

    def resolve_capture_payment_sales_order_payment_summary_join(self, info):
        return capture_payment_sales_order_payment_summary_join.query.all()

    def resolve_competitor_party_join(self, info):
        return competitor_party_join.query.all()

    def resolve_coupon_manufacturer_join(self, info):
        return coupon_manufacturer_join.query.all()

    def resolve_coupon_payment_method_type_join(self, info):
        return coupon_payment_method_type_join.query.all()

    def resolve_credit_tender_account_join(self, info):
        return credit_tender_account_join.query.all()

    def resolve_credit_tender_payment_method_type_join(self, info):
        return credit_tender_payment_method_type_join.query.all()

    def resolve_customer_party_join(self, info):
        return customer_party_join.query.all()

    def resolve_customer_state_history_party_role_join(self, info):
        return customer_state_history_party_role_join.query.all()

    def resolve_goods_product_brand_join(self, info):
        return goods_product_brand_join.query.all()

    def resolve_goods_product_primary_product_category_join(self, info):
        return goods_product_primary_product_category_join.query.all()

    def resolve_goods_product_primary_sales_channel_join(self, info):
        return goods_product_primary_sales_channel_join.query.all()

    def resolve_goods_product_valid_for_period_uo_m_join(self, info):
        return goods_product_valid_for_period_uo_m_join.query.all()

    def resolve_household_primary_account_join(self, info):
        return household_primary_account_join.query.all()

    def resolve_individual(self, info):
        return individual.query.all()

    def resolve_industry_job(self, info):
        return industry_job.query.all()

    def resolve_internal_busines_unit_parent_internal_busines_unit_join(self, info):
        return internal_busines_unit_parent_internal_busines_unit_join.query.all()

    def resolve_internal_busines_unit_primary_account_join(self, info):
        return internal_busines_unit_primary_account_join.query.all()

    def resolve_job_skill(self, info):
        return job_skill.query.all()

    def resolve_lead_converted_to_account_contact_join(self, info):
        return lead_converted_to_account_contact_join.query.all()

    def resolve_lead_converted_to_account_join(self, info):
        return lead_converted_to_account_join.query.all()

    def resolve_lead_fax_contact_phone_join(self, info):
        return lead_fax_contact_phone_join.query.all()

    def resolve_lead_mobile_contact_phone_join(self, info):
        return lead_mobile_contact_phone_join.query.all()

    def resolve_lead_partner_account_join(self, info):
        return lead_partner_account_join.query.all()

    def resolve_lead_party_role_join(self, info):
        return lead_party_role_join.query.all()

    def resolve_party_additional_name_party_join(self, info):
        return party_additional_name_party_join.query.all()

    def resolve_party_identification_party_join(self, info):
        return party_identification_party_join.query.all()

    def resolve_party_identification_party_role_join(self, info):
        return party_identification_party_role_join.query.all()

    def resolve_party_primary_account_join(self, info):
        return party_primary_account_join.query.all()

    def resolve_party_related_party_party_join(self, info):
        return party_related_party_party_join.query.all()

    def resolve_party_related_party_party_relationship_type_join(self, info):
        return party_related_party_party_relationship_type_join.query.all()

    def resolve_party_related_party_related_party_join(self, info):
        return party_related_party_related_party_join.query.all()

    def resolve_party_role_party_join(self, info):
        return party_role_party_join.query.all()

    def resolve_party_web_addr_party_join(self, info):
        return party_web_addr_party_join.query.all()

    def resolve_party_web_addr_party_role_join(self, info):
        return party_web_addr_party_role_join.query.all()

    def resolve_pay_gat_aut_log_pay_gat_int_typ_join(self, info):
        return pay_gat_aut_log_pay_gat_int_typ_join.query.all()

    def resolve_pay_gat_aut_rev_log_pay_aut_rev_join(self, info):
        return pay_gat_aut_rev_log_pay_aut_rev_join.query.all()

    def resolve_pay_gat_aut_rev_log_pay_gat_int_typ_join(self, info):
        return pay_gat_aut_rev_log_pay_gat_int_typ_join.query.all()

    def resolve_pay_gat_int_log_pay_gat_int_typ_join(self, info):
        return pay_gat_int_log_pay_gat_int_typ_join.query.all()

    def resolve_pay_gat_pay_log_pay_gat_int_typ_join(self, info):
        return pay_gat_pay_log_pay_gat_int_typ_join.query.all()

    def resolve_payment_account_join(self, info):
        return payment_account_join.query.all()

    def resolve_payment_allocation_related_payment_allocation_join(self, info):
        return payment_allocation_related_payment_allocation_join.query.all()

    def resolve_payment_application_payment_join(self, info):
        return payment_application_payment_join.query.all()

    def resolve_payment_authorization_payment_gateway_join(self, info):
        return payment_authorization_payment_gateway_join.query.all()

    def resolve_payment_authorization_payment_gateway_result_join(self, info):
        return payment_authorization_payment_gateway_result_join.query.all()

    def resolve_payment_authorization_payment_group_join(self, info):
        return payment_authorization_payment_group_join.query.all()

    def resolve_payment_authorization_payment_method_join(self, info):
        return payment_authorization_payment_method_join.query.all()

    def resolve_payment_authorization_reversal_capture_payment_join(self, info):
        return payment_authorization_reversal_capture_payment_join.query.all()

    def resolve_payment_authorization_reversal_payment_authorization_join(self, info):
        return payment_authorization_reversal_payment_authorization_join.query.all()

    def resolve_payment_authorization_reversal_payment_gateway_result_join(self, info):
        return payment_authorization_reversal_payment_gateway_result_join.query.all()

    def resolve_payment_authorization_sales_order_payment_summary_join(self, info):
        return payment_authorization_sales_order_payment_summary_join.query.all()

    def resolve_payment_card_payment_method_type_join(self, info):
        return payment_card_payment_method_type_join.query.all()

    def resolve_payment_credit_memo_allocation_related_payment_allocation_join(self, info):
        return payment_credit_memo_allocation_related_payment_allocation_join.query.all()

    def resolve_payment_credit_memo_application_payment_join(self, info):
        return payment_credit_memo_application_payment_join.query.all()

    def resolve_payment_gateway_auth_reversal_log_payment_gateway_result_join(self, info):
        return payment_gateway_auth_reversal_log_payment_gateway_result_join.query.all()

    def resolve_payment_gateway_authorization_log_payment_authorization_join(self, info):
        return payment_gateway_authorization_log_payment_authorization_join.query.all()

    def resolve_payment_gateway_authorization_log_payment_gateway_result_join(self, info):
        return payment_gateway_authorization_log_payment_gateway_result_join.query.all()

    def resolve_payment_gateway_interaction_log_payment_gateway_result_join(self, info):
        return payment_gateway_interaction_log_payment_gateway_result_join.query.all()

    def resolve_payment_gateway_payment_gateway_provider_join(self, info):
        return payment_gateway_payment_gateway_provider_join.query.all()

    def resolve_payment_gateway_payment_log_payment_gateway_result_join(self, info):
        return payment_gateway_payment_log_payment_gateway_result_join.query.all()

    def resolve_payment_gateway_payment_log_payment_join(self, info):
        return payment_gateway_payment_log_payment_join.query.all()

    def resolve_payment_internal_busines_unit_join(self, info):
        return payment_internal_busines_unit_join.query.all()

    def resolve_payment_invoice_allocation_payment_invoice_application_join(self, info):
        return payment_invoice_allocation_payment_invoice_application_join.query.all()

    def resolve_payment_invoice_allocation_related_payment_allocation_join(self, info):
        return payment_invoice_allocation_related_payment_allocation_join.query.all()

    def resolve_payment_invoice_application_payment_join(self, info):
        return payment_invoice_application_payment_join.query.all()

    def resolve_payment_latest_gateway_result_code_join(self, info):
        return payment_latest_gateway_result_code_join.query.all()

    def resolve_payment_method_payment_method_type_join(self, info):
        return payment_method_payment_method_type_join.query.all()

    def resolve_payment_payment_gateway_join(self, info):
        return payment_payment_gateway_join.query.all()

    def resolve_payment_payment_group_join(self, info):
        return payment_payment_group_join.query.all()

    def resolve_payment_payment_method_join(self, info):
        return payment_payment_method_join.query.all()

    def resolve_payment_payment_treatment_join(self, info):
        return payment_payment_treatment_join.query.all()

    def resolve_payment_sales_order_payment_summary_join(self, info):
        return payment_sales_order_payment_summary_join.query.all()

    def resolve_payment_treatment_payment_policy_join(self, info):
        return payment_treatment_payment_policy_join.query.all()

    def resolve_payment_treatment_payment_treatment_method_join(self, info):
        return payment_treatment_payment_treatment_method_join.query.all()

    def resolve_product(self, info):
        return product.query.all()

    def resolve_product_attribute_value_attribute_value_join(self, info):
        return product_attribute_value_attribute_value_join.query.all()

    def resolve_product_catalog_translation_product_catalog_join(self, info):
        return product_catalog_translation_product_catalog_join.query.all()

    def resolve_product_category_attribute_set_product_category_join(self, info):
        return product_category_attribute_set_product_category_join.query.all()

    def resolve_product_category_parent_category_join(self, info):
        return product_category_parent_category_join.query.all()

    def resolve_product_category_product_catalog_join(self, info):
        return product_category_product_catalog_join.query.all()

    def resolve_product_category_product_product_category_join(self, info):
        return product_category_product_product_category_join.query.all()

    def resolve_product_category_translation_product_category_join(self, info):
        return product_category_translation_product_category_join.query.all()

    def resolve_product_image_translation_product_image_join(self, info):
        return product_image_translation_product_image_join.query.all()

    def resolve_product_related_product_product_relationship_type_join(self, info):
        return product_related_product_product_relationship_type_join.query.all()

    def resolve_product_related_product_sales_order_product1_join(self, info):
        return product_related_product_sales_order_product1_join.query.all()

    def resolve_product_related_product_sales_order_product2_join(self, info):
        return product_related_product_sales_order_product2_join.query.all()

    def resolve_refund_allocation_refund_payment_join(self, info):
        return refund_allocation_refund_payment_join.query.all()

    def resolve_refund_allocation_related_refund_allocation_join(self, info):
        return refund_allocation_related_refund_allocation_join.query.all()

    def resolve_refund_credit_memo_allocation_refund_payment_join(self, info):
        return refund_credit_memo_allocation_refund_payment_join.query.all()

    def resolve_refund_credit_memo_allocation_related_refund_allocation_join(self, info):
        return refund_credit_memo_allocation_related_refund_allocation_join.query.all()

    def resolve_refund_payment_account_join(self, info):
        return refund_payment_account_join.query.all()

    def resolve_refund_payment_allocation_capture_payment_join(self, info):
        return refund_payment_allocation_capture_payment_join.query.all()

    def resolve_refund_payment_allocation_refund_payment_join(self, info):
        return refund_payment_allocation_refund_payment_join.query.all()

    def resolve_refund_payment_allocation_related_refund_allocation_join(self, info):
        return refund_payment_allocation_related_refund_allocation_join.query.all()

    def resolve_refund_payment_internal_busines_unit_join(self, info):
        return refund_payment_internal_busines_unit_join.query.all()

    def resolve_refund_payment_latest_gateway_result_code_join(self, info):
        return refund_payment_latest_gateway_result_code_join.query.all()

    def resolve_refund_payment_payment_gateway_join(self, info):
        return refund_payment_payment_gateway_join.query.all()

    def resolve_refund_payment_payment_group_join(self, info):
        return refund_payment_payment_group_join.query.all()

    def resolve_refund_payment_payment_method_join(self, info):
        return refund_payment_payment_method_join.query.all()

    def resolve_refund_payment_payment_treatment_join(self, info):
        return refund_payment_payment_treatment_join.query.all()

    def resolve_refund_payment_sales_order_payment_summary_join(self, info):
        return refund_payment_sales_order_payment_summary_join.query.all()

    def resolve_sal_ord_pro_rea_sal_ord_pro_rea_cat_join(self, info):
        return sal_ord_pro_rea_sal_ord_pro_rea_cat_join.query.all()

    def resolve_sales_channel_sales_channel_type_join(self, info):
        return sales_channel_sales_channel_type_join.query.all()

    def resolve_sales_order_bill_to_account_join(self, info):
        return sales_order_bill_to_account_join.query.all()

    def resolve_sales_order_bill_to_addr_join(self, info):
        return sales_order_bill_to_addr_join.query.all()

    def resolve_sales_order_bill_to_contact_join(self, info):
        return sales_order_bill_to_contact_join.query.all()

    def resolve_sales_order_bill_to_email_join(self, info):
        return sales_order_bill_to_email_join.query.all()

    def resolve_sales_order_bill_to_phone_number_join(self, info):
        return sales_order_bill_to_phone_number_join.query.all()

    def resolve_sales_order_change_log_change_sales_order_join(self, info):
        return sales_order_change_log_change_sales_order_join.query.all()

    def resolve_sales_order_change_log_change_sales_order_product_join(self, info):
        return sales_order_change_log_change_sales_order_product_join.query.all()

    def resolve_sales_order_change_log_related_sales_order_join(self, info):
        return sales_order_change_log_related_sales_order_join.query.all()

    def resolve_sales_order_change_log_related_sales_order_product_join(self, info):
        return sales_order_change_log_related_sales_order_product_join.query.all()

    def resolve_sales_order_delivery_group_account_contact_join(self, info):
        return sales_order_delivery_group_account_contact_join.query.all()

    def resolve_sales_order_delivery_group_contact_point_addr_join(self, info):
        return sales_order_delivery_group_contact_point_addr_join.query.all()

    def resolve_sales_order_delivery_group_order_delivery_method_join(self, info):
        return sales_order_delivery_group_order_delivery_method_join.query.all()

    def resolve_sales_order_delivery_group_original_delivery_group_join(self, info):
        return sales_order_delivery_group_original_delivery_group_join.query.all()

    def resolve_sales_order_delivery_group_sales_order_delivery_state_join(self, info):
        return sales_order_delivery_group_sales_order_delivery_state_join.query.all()

    def resolve_sales_order_delivery_group_sales_order_join(self, info):
        return sales_order_delivery_group_sales_order_join.query.all()

    def resolve_sales_order_internal_busines_unit_join(self, info):
        return sales_order_internal_busines_unit_join.query.all()

    def resolve_sales_order_original_order_join(self, info):
        return sales_order_original_order_join.query.all()

    def resolve_sales_order_payment_method_join(self, info):
        return sales_order_payment_method_join.query.all()

    def resolve_sales_order_payment_summary_payment_method_join(self, info):
        return sales_order_payment_summary_payment_method_join.query.all()

    def resolve_sales_order_payment_summary_sales_order_join(self, info):
        return sales_order_payment_summary_sales_order_join.query.all()

    def resolve_sales_order_price_adjustment_sales_order_join(self, info):
        return sales_order_price_adjustment_sales_order_join.query.all()

    def resolve_sales_order_product_group_sales_order_product_group_type_join(self, info):
        return sales_order_product_group_sales_order_product_group_type_join.query.all()

    def resolve_sales_order_product_list_price_term_uo_m_join(self, info):
        return sales_order_product_list_price_term_uo_m_join.query.all()

    def resolve_sales_order_product_original_order_product_join(self, info):
        return sales_order_product_original_order_product_join.query.all()

    def resolve_sales_order_product_price_book_entry_join(self, info):
        return sales_order_product_price_book_entry_join.query.all()

    def resolve_sales_order_product_sales_order_delivery_group_join(self, info):
        return sales_order_product_sales_order_delivery_group_join.query.all()

    def resolve_sales_order_product_sales_order_join(self, info):
        return sales_order_product_sales_order_join.query.all()

    def resolve_sales_order_product_sales_order_product_reason_join(self, info):
        return sales_order_product_sales_order_product_reason_join.query.all()

    def resolve_sales_order_product_sales_order_product_state_join(self, info):
        return sales_order_product_sales_order_product_state_join.query.all()

    def resolve_sales_order_product_seller_account_join(self, info):
        return sales_order_product_seller_account_join.query.all()

    def resolve_sales_order_product_shipping_addr_join(self, info):
        return sales_order_product_shipping_addr_join.query.all()

    def resolve_sales_order_product_shipping_email_join(self, info):
        return sales_order_product_shipping_email_join.query.all()

    def resolve_sales_order_product_shipping_phone_join(self, info):
        return sales_order_product_shipping_phone_join.query.all()

    def resolve_sales_order_product_subscription_term_unit_join(self, info):
        return sales_order_product_subscription_term_unit_join.query.all()

    def resolve_sales_order_product_tax_original_sales_order_product_tax_join(self, info):
        return sales_order_product_tax_original_sales_order_product_tax_join.query.all()

    def resolve_sales_order_product_tax_sales_order_product_join(self, info):
        return sales_order_product_tax_sales_order_product_join.query.all()

    def resolve_sales_order_renewal_term_join(self, info):
        return sales_order_renewal_term_join.query.all()

    def resolve_sales_order_sales_channel_join(self, info):
        return sales_order_sales_channel_join.query.all()

    def resolve_sales_order_sales_order_confirmation_state_join(self, info):
        return sales_order_sales_order_confirmation_state_join.query.all()

    def resolve_sales_order_sales_order_state_join(self, info):
        return sales_order_sales_order_state_join.query.all()

    def resolve_sales_order_sales_order_type_join(self, info):
        return sales_order_sales_order_type_join.query.all()

    def resolve_sales_order_seller_join(self, info):
        return sales_order_seller_join.query.all()

    def resolve_sales_order_ship_to_addr_join(self, info):
        return sales_order_ship_to_addr_join.query.all()

    def resolve_sales_order_ship_to_contact_join(self, info):
        return sales_order_ship_to_contact_join.query.all()

    def resolve_sales_order_ship_to_email_join(self, info):
        return sales_order_ship_to_email_join.query.all()

    def resolve_sales_order_sold_to_customer_join(self, info):
        return sales_order_sold_to_customer_join.query.all()

    def resolve_sales_order_user_device_sesion_join(self, info):
        return sales_order_user_device_sesion_join.query.all()

    def resolve_seller_party_join(self, info):
        return seller_party_join.query.all()

    def resolve_service_product_brand_join(self, info):
        return service_product_brand_join.query.all()

    def resolve_service_product_primary_product_category_join(self, info):
        return service_product_primary_product_category_join.query.all()

    def resolve_service_product_primary_sales_channel_join(self, info):
        return service_product_primary_sales_channel_join.query.all()

    def resolve_service_product_service_provider_account_join(self, info):
        return service_product_service_provider_account_join.query.all()

    def resolve_service_product_valid_for_period_uo_m_join(self, info):
        return service_product_valid_for_period_uo_m_join.query.all()

    def resolve_shi_pro_pri_adj_tax_shi_pro_pri_adj_join(self, info):
        return shi_pro_pri_adj_tax_shi_pro_pri_adj_join.query.all()

    def resolve_shipment_document_shipment_join(self, info):
        return shipment_document_shipment_join.query.all()

    def resolve_shipment_package_shipment_join(self, info):
        return shipment_package_shipment_join.query.all()

    def resolve_shipment_product_price_adjustment_shipment_product_join(self, info):
        return shipment_product_price_adjustment_shipment_product_join.query.all()

    def resolve_shipment_product_sales_order_product_join(self, info):
        return shipment_product_sales_order_product_join.query.all()

    def resolve_shipment_product_shipment_join(self, info):
        return shipment_product_shipment_join.query.all()

    def resolve_shipment_product_shipment_package_join(self, info):
        return shipment_product_shipment_package_join.query.all()

    def resolve_shipment_sales_order_delivery_group_join(self, info):
        return shipment_sales_order_delivery_group_join.query.all()

    def resolve_shipment_sales_order_join(self, info):
        return shipment_sales_order_join.query.all()

    def resolve_shipment_ship_to_addr_join(self, info):
        return shipment_ship_to_addr_join.query.all()

    def resolve_shipment_shipment_state_join(self, info):
        return shipment_shipment_state_join.query.all()

    def resolve_supplier_party_join(self, info):
        return supplier_party_join.query.all()

    def resolve_uncategorized_party_primary_account_join(self, info):
        return uncategorized_party_primary_account_join.query.all()

    def resolve_account_contact_individual_join(self, info):
        return account_contact_individual_join.query.all()

    def resolve_bundle_product_master_product_join(self, info):
        return bundle_product_master_product_join.query.all()

    def resolve_education(self, info):
        return education.query.all()

    def resolve_goods_product_master_product_join(self, info):
        return goods_product_master_product_join.query.all()

    def resolve_individual_primary_account_join(self, info):
        return individual_primary_account_join.query.all()

    def resolve_individual_primary_household_join(self, info):
        return individual_primary_household_join.query.all()

    def resolve_job_individual(self, info):
        return job_individual.query.all()

    def resolve_location(self, info):
        return location.query.all()

    def resolve_order_delivery_method_product_join(self, info):
        return order_delivery_method_product_join.query.all()

    def resolve_person_language_individual_join(self, info):
        return person_language_individual_join.query.all()

    def resolve_person_life_event_individual_join(self, info):
        return person_life_event_individual_join.query.all()

    def resolve_portal(self, info):
        return portal.query.all()

    def resolve_price_book_entry_product_join(self, info):
        return price_book_entry_product_join.query.all()

    def resolve_product_attribute_set_product_join(self, info):
        return product_attribute_set_product_join.query.all()

    def resolve_product_attribute_value_product_join(self, info):
        return product_attribute_value_product_join.query.all()

    def resolve_product_brand_join(self, info):
        return product_brand_join.query.all()

    def resolve_product_category_product_product_join(self, info):
        return product_category_product_product_join.query.all()

    def resolve_product_collateral_product_join(self, info):
        return product_collateral_product_join.query.all()

    def resolve_product_image_product_join(self, info):
        return product_image_product_join.query.all()

    def resolve_product_master_product_join(self, info):
        return product_master_product_join.query.all()

    def resolve_product_primary_product_category_join(self, info):
        return product_primary_product_category_join.query.all()

    def resolve_product_primary_sales_channel_join(self, info):
        return product_primary_sales_channel_join.query.all()

    def resolve_product_related_product_child_product_join(self, info):
        return product_related_product_child_product_join.query.all()

    def resolve_product_related_product_parent_product_join(self, info):
        return product_related_product_parent_product_join.query.all()

    def resolve_product_translation_product_join(self, info):
        return product_translation_product_join.query.all()

    def resolve_product_valid_for_period_uo_m_join(self, info):
        return product_valid_for_period_uo_m_join.query.all()

    def resolve_profile(self, info):
        return profile.query.all()

    def resolve_sales_order_product_product_join(self, info):
        return sales_order_product_product_join.query.all()

    def resolve_service_product_master_product_join(self, info):
        return service_product_master_product_join.query.all()

    def resolve_shipment_product_product_join(self, info):
        return shipment_product_product_join.query.all()

    def resolve_shipping_method_product_join(self, info):
        return shipping_method_product_join.query.all()

    def resolve_user_skill(self, info):
        return user_skill.query.all()

    def resolve_education_individual_join(self, info):
        return education_individual_join.query.all()

    def resolve_page(self, info):
        return page.query.all()

    def resolve_resume(self, info):
        return resume.query.all()

    def resolve_swarm(self, info):
        return swarm.query.all()

    def resolve_swarm_individual(self, info):
        return swarm_individual.query.all()

    def resolve_work_history(self, info):
        return work_history.query.all()

    def resolve_work_history_individual_join(self, info):
        return work_history_individual_join.query.all()
