"""Owned model metadata for the customer_360 PBC."""

from __future__ import annotations

import hashlib
import json
import sqlite3
from datetime import UTC, datetime

PBC_KEY = 'customer_360'
OWNED_SCHEMA = {'schema': 'customer_360',
 'table_prefix': 'customer_360_',
 'tables': ({'logical_table': 'customer_profile',
             'owned_table': 'customer_360_customer_profile',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'display_name', 'type': 'string', 'required': True},
                        {'name': 'region', 'type': 'string', 'required': True},
                        {'name': 'lifecycle_state', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'customer_profile_version',
             'owned_table': 'customer_360_customer_profile_version',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'customer_profile_attribute',
             'owned_table': 'customer_360_customer_profile_attribute',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'customer_identity',
             'owned_table': 'customer_360_customer_identity',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'identity_type', 'type': 'string', 'required': True},
                        {'name': 'identity_value_hash', 'type': 'string', 'required': True},
                        {'name': 'confidence', 'type': 'decimal', 'required': True}),
             'relationships': ()},
            {'logical_table': 'customer_identity_evidence',
             'owned_table': 'customer_360_customer_identity_evidence',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'identity_match_candidate',
             'owned_table': 'customer_360_identity_match_candidate',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'identity_survivorship_rule',
             'owned_table': 'customer_360_identity_survivorship_rule',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'customer_relationship',
             'owned_table': 'customer_360_customer_relationship',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'household',
             'owned_table': 'customer_360_household',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'household_member',
             'owned_table': 'customer_360_household_member',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'engagement_event',
             'owned_table': 'customer_360_engagement_event',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'event_type', 'type': 'string', 'required': True},
                        {'name': 'channel', 'type': 'string', 'required': True},
                        {'name': 'value', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'engagement_score',
             'owned_table': 'customer_360_engagement_score',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'communication_preference',
             'owned_table': 'customer_360_communication_preference',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'preference_history',
             'owned_table': 'customer_360_preference_history',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'touchpoint',
             'owned_table': 'customer_360_touchpoint',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'channel_interaction',
             'owned_table': 'customer_360_channel_interaction',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'consent_record',
             'owned_table': 'customer_360_consent_record',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'purpose', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'confidence', 'type': 'decimal', 'required': True}),
             'relationships': ()},
            {'logical_table': 'consent_policy',
             'owned_table': 'customer_360_consent_policy',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'privacy_request',
             'owned_table': 'customer_360_privacy_request',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'customer_timeline',
             'owned_table': 'customer_360_customer_timeline',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'customer_timeline_event',
             'owned_table': 'customer_360_customer_timeline_event',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'customer_segment_projection',
             'owned_table': 'customer_360_customer_segment_projection',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'customer_segment_membership',
             'owned_table': 'customer_360_customer_segment_membership',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'customer_value_snapshot',
             'owned_table': 'customer_360_customer_value_snapshot',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'customer_health_signal',
             'owned_table': 'customer_360_customer_health_signal',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'customer_churn_forecast',
             'owned_table': 'customer_360_customer_churn_forecast',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'profile_merge_case',
             'owned_table': 'customer_360_profile_merge_case',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'profile_merge_decision',
             'owned_table': 'customer_360_profile_merge_decision',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'customer_exception_case',
             'owned_table': 'customer_360_customer_exception_case',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'customer_remediation_task',
             'owned_table': 'customer_360_customer_remediation_task',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'commerce_customer_projection',
             'owned_table': 'customer_360_commerce_customer_projection',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'billing_account_projection',
             'owned_table': 'customer_360_billing_account_projection',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'service_timeline_projection',
             'owned_table': 'customer_360_service_timeline_projection',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'loyalty_profile_projection',
             'owned_table': 'customer_360_loyalty_profile_projection',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'notification_projection',
             'owned_table': 'customer_360_notification_projection',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'customer_api_projection',
             'owned_table': 'customer_360_customer_api_projection',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'customer_proof',
             'owned_table': 'customer_360_customer_proof',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'customer_policy_screening',
             'owned_table': 'customer_360_customer_policy_screening',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'customer_control_assertion',
             'owned_table': 'customer_360_customer_control_assertion',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'customer_federation_view',
             'owned_table': 'customer_360_customer_federation_view',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'customer_resilience_drill',
             'owned_table': 'customer_360_customer_resilience_drill',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'customer_crypto_epoch',
             'owned_table': 'customer_360_customer_crypto_epoch',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'carbon_customer_window',
             'owned_table': 'customer_360_carbon_customer_window',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'customer_segment_optimization',
             'owned_table': 'customer_360_customer_segment_optimization',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'customer_channel_allocation',
             'owned_table': 'customer_360_customer_channel_allocation',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'customer_anomaly_signal',
             'owned_table': 'customer_360_customer_anomaly_signal',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'customer_exposure_forecast',
             'owned_table': 'customer_360_customer_exposure_forecast',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'customer_identity_attestation',
             'owned_table': 'customer_360_customer_identity_attestation',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'customer_governed_model',
             'owned_table': 'customer_360_customer_governed_model',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'customer_seed_data',
             'owned_table': 'customer_360_customer_seed_data',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'customer_rule',
             'owned_table': 'customer_360_customer_rule',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'customer_parameter',
             'owned_table': 'customer_360_customer_parameter',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'customer_configuration',
             'owned_table': 'customer_360_customer_configuration',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'profile_id', 'type': 'string', 'required': True},
                        {'name': 'status', 'type': 'string', 'required': True},
                        {'name': 'attributes', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'appgen_outbox_event',
             'owned_table': 'customer_360_appgen_outbox_event',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'event_type', 'type': 'string', 'required': True},
                        {'name': 'payload', 'type': 'json', 'required': True},
                        {'name': 'idempotency_key', 'type': 'string', 'required': True}),
             'relationships': ()},
            {'logical_table': 'appgen_inbox_event',
             'owned_table': 'customer_360_appgen_inbox_event',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'event_type', 'type': 'string', 'required': True},
                        {'name': 'payload', 'type': 'json', 'required': True},
                        {'name': 'attempts', 'type': 'integer', 'required': True}),
             'relationships': ()},
            {'logical_table': 'dead_letter_event',
             'owned_table': 'customer_360_dead_letter_event',
             'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
                        {'name': 'tenant', 'type': 'string', 'required': True},
                        {'name': 'created_at', 'type': 'datetime', 'required': True},
                        {'name': 'updated_at', 'type': 'datetime', 'required': True},
                        {'name': 'event_type', 'type': 'string', 'required': True},
                        {'name': 'payload', 'type': 'json', 'required': True},
                        {'name': 'reason', 'type': 'string', 'required': True}),
             'relationships': ()})}
MODELS = ({'class_name': 'Customer360CustomerProfile',
  'table': 'customer_360_customer_profile',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'display_name', 'type': 'string', 'required': True},
             {'name': 'region', 'type': 'string', 'required': True},
             {'name': 'lifecycle_state', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360CustomerProfileVersion',
  'table': 'customer_360_customer_profile_version',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360CustomerProfileAttribute',
  'table': 'customer_360_customer_profile_attribute',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360CustomerIdentity',
  'table': 'customer_360_customer_identity',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'identity_type', 'type': 'string', 'required': True},
             {'name': 'identity_value_hash', 'type': 'string', 'required': True},
             {'name': 'confidence', 'type': 'decimal', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360CustomerIdentityEvidence',
  'table': 'customer_360_customer_identity_evidence',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360IdentityMatchCandidate',
  'table': 'customer_360_identity_match_candidate',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360IdentitySurvivorshipRule',
  'table': 'customer_360_identity_survivorship_rule',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360CustomerRelationship',
  'table': 'customer_360_customer_relationship',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360Household',
  'table': 'customer_360_household',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360HouseholdMember',
  'table': 'customer_360_household_member',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360EngagementEvent',
  'table': 'customer_360_engagement_event',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'event_type', 'type': 'string', 'required': True},
             {'name': 'channel', 'type': 'string', 'required': True},
             {'name': 'value', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360EngagementScore',
  'table': 'customer_360_engagement_score',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360CommunicationPreference',
  'table': 'customer_360_communication_preference',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360PreferenceHistory',
  'table': 'customer_360_preference_history',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360Touchpoint',
  'table': 'customer_360_touchpoint',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360ChannelInteraction',
  'table': 'customer_360_channel_interaction',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360ConsentRecord',
  'table': 'customer_360_consent_record',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'purpose', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'confidence', 'type': 'decimal', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360ConsentPolicy',
  'table': 'customer_360_consent_policy',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360PrivacyRequest',
  'table': 'customer_360_privacy_request',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360CustomerTimeline',
  'table': 'customer_360_customer_timeline',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360CustomerTimelineEvent',
  'table': 'customer_360_customer_timeline_event',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360CustomerSegmentProjection',
  'table': 'customer_360_customer_segment_projection',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360CustomerSegmentMembership',
  'table': 'customer_360_customer_segment_membership',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360CustomerValueSnapshot',
  'table': 'customer_360_customer_value_snapshot',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360CustomerHealthSignal',
  'table': 'customer_360_customer_health_signal',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360CustomerChurnForecast',
  'table': 'customer_360_customer_churn_forecast',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360ProfileMergeCase',
  'table': 'customer_360_profile_merge_case',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360ProfileMergeDecision',
  'table': 'customer_360_profile_merge_decision',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360CustomerExceptionCase',
  'table': 'customer_360_customer_exception_case',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360CustomerRemediationTask',
  'table': 'customer_360_customer_remediation_task',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360CommerceCustomerProjection',
  'table': 'customer_360_commerce_customer_projection',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360BillingAccountProjection',
  'table': 'customer_360_billing_account_projection',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360ServiceTimelineProjection',
  'table': 'customer_360_service_timeline_projection',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360LoyaltyProfileProjection',
  'table': 'customer_360_loyalty_profile_projection',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360NotificationProjection',
  'table': 'customer_360_notification_projection',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360CustomerApiProjection',
  'table': 'customer_360_customer_api_projection',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360CustomerProof',
  'table': 'customer_360_customer_proof',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360CustomerPolicyScreening',
  'table': 'customer_360_customer_policy_screening',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360CustomerControlAssertion',
  'table': 'customer_360_customer_control_assertion',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360CustomerFederationView',
  'table': 'customer_360_customer_federation_view',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360CustomerResilienceDrill',
  'table': 'customer_360_customer_resilience_drill',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360CustomerCryptoEpoch',
  'table': 'customer_360_customer_crypto_epoch',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360CarbonCustomerWindow',
  'table': 'customer_360_carbon_customer_window',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360CustomerSegmentOptimization',
  'table': 'customer_360_customer_segment_optimization',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360CustomerChannelAllocation',
  'table': 'customer_360_customer_channel_allocation',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360CustomerAnomalySignal',
  'table': 'customer_360_customer_anomaly_signal',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360CustomerExposureForecast',
  'table': 'customer_360_customer_exposure_forecast',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360CustomerIdentityAttestation',
  'table': 'customer_360_customer_identity_attestation',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360CustomerGovernedModel',
  'table': 'customer_360_customer_governed_model',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360CustomerSeedData',
  'table': 'customer_360_customer_seed_data',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360CustomerRule',
  'table': 'customer_360_customer_rule',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360CustomerParameter',
  'table': 'customer_360_customer_parameter',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360CustomerConfiguration',
  'table': 'customer_360_customer_configuration',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'profile_id', 'type': 'string', 'required': True},
             {'name': 'status', 'type': 'string', 'required': True},
             {'name': 'attributes', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360AppgenOutboxEvent',
  'table': 'customer_360_appgen_outbox_event',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'event_type', 'type': 'string', 'required': True},
             {'name': 'payload', 'type': 'json', 'required': True},
             {'name': 'idempotency_key', 'type': 'string', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360AppgenInboxEvent',
  'table': 'customer_360_appgen_inbox_event',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'event_type', 'type': 'string', 'required': True},
             {'name': 'payload', 'type': 'json', 'required': True},
             {'name': 'attempts', 'type': 'integer', 'required': True}),
  'relationships': ()},
 {'class_name': 'Customer360DeadLetterEvent',
  'table': 'customer_360_dead_letter_event',
  'fields': ({'name': 'id', 'type': 'integer', 'required': True, 'primary_key': True, 'nullable': False},
             {'name': 'tenant', 'type': 'string', 'required': True},
             {'name': 'created_at', 'type': 'datetime', 'required': True},
             {'name': 'updated_at', 'type': 'datetime', 'required': True},
             {'name': 'event_type', 'type': 'string', 'required': True},
             {'name': 'payload', 'type': 'json', 'required': True},
             {'name': 'reason', 'type': 'string', 'required': True}),
  'relationships': ()})


def model_manifest():
    """Return executable owned model/table alignment evidence."""
    schema_tables = tuple(table['owned_table'] for table in OWNED_SCHEMA.get('tables', ()))
    model_tables = tuple(model['table'] for model in MODELS)
    missing_models = tuple(table for table in schema_tables if table not in model_tables)
    external_models = tuple(table for table in model_tables if not table.startswith(f'{PBC_KEY}_'))
    relationship_targets = tuple(
        relationship.get('target_table')
        for table in OWNED_SCHEMA.get('tables', ())
        for relationship in table.get('relationships', ())
        if relationship.get('target_table')
    )
    cross_pbc_relationships = tuple(
        target for target in relationship_targets if not target.startswith(f'{PBC_KEY}_')
    )
    return {
        'ok': bool(schema_tables)
        and bool(model_tables)
        and not missing_models
        and not external_models
        and not cross_pbc_relationships,
        'pbc': PBC_KEY,
        'schema_tables': schema_tables,
        'model_tables': model_tables,
        'missing_models': missing_models,
        'external_models': external_models,
        'cross_pbc_relationships': cross_pbc_relationships,
        'relationship_targets': relationship_targets,
        'side_effects': (),
    }


def instantiate_model(table_name, values=None):
    """Create a side-effect-free model payload for validation and tests."""
    model = next((item for item in MODELS if item['table'] == table_name), None)
    if model is None:
        return {'ok': False, 'reason': 'unknown_model', 'table': table_name, 'side_effects': ()}
    supplied = dict(values or {})
    fields = tuple(field['name'] if isinstance(field, dict) else field for field in model.get('fields', ()))
    payload = {field: supplied.get(field) for field in fields}
    return {
        'ok': table_name.startswith(f'{PBC_KEY}_') and bool(fields),
        'pbc': PBC_KEY,
        'model': model['class_name'],
        'table': table_name,
        'fields': fields,
        'payload': payload,
        'side_effects': (),
    }


def smoke_test():
    """Exercise model alignment and model payload creation."""
    manifest = model_manifest()
    first_table = manifest['model_tables'][0] if manifest['model_tables'] else None
    instance = instantiate_model(first_table, {'id': 1}) if first_table else {'ok': False}
    return {
        'ok': manifest['ok'] and instance.get('ok') is True,
        'manifest': manifest,
        'instance': instance,
        'side_effects': (),
    }


STANDALONE_SQLITE_TABLES = (
    {
        "table": "customer_360_customer_profile",
        "description": "Primary customer profile spine for the standalone one-PBC app.",
        "key_field": "profile_id",
        "columns": (
            ("profile_id", "TEXT PRIMARY KEY"),
            ("tenant", "TEXT NOT NULL"),
            ("display_name", "TEXT NOT NULL"),
            ("region", "TEXT NOT NULL"),
            ("lifecycle_state", "TEXT NOT NULL"),
            ("account_type", "TEXT NOT NULL"),
            ("attributes", "TEXT NOT NULL"),
            ("created_at", "TEXT NOT NULL"),
            ("updated_at", "TEXT NOT NULL"),
        ),
    },
    {
        "table": "customer_360_customer_identity",
        "description": "Identity evidence linked to a customer profile.",
        "key_field": "identity_id",
        "columns": (
            ("identity_id", "TEXT PRIMARY KEY"),
            ("tenant", "TEXT NOT NULL"),
            ("profile_id", "TEXT NOT NULL"),
            ("identity_type", "TEXT NOT NULL"),
            ("identity_value_hash", "TEXT NOT NULL"),
            ("confidence", "REAL NOT NULL"),
            ("verified", "INTEGER NOT NULL"),
            ("evidence", "TEXT NOT NULL"),
            ("linked_at", "TEXT NOT NULL"),
        ),
    },
    {
        "table": "customer_360_consent_record",
        "description": "Consent state used by the standalone preference center.",
        "key_field": "consent_id",
        "columns": (
            ("consent_id", "TEXT PRIMARY KEY"),
            ("tenant", "TEXT NOT NULL"),
            ("profile_id", "TEXT NOT NULL"),
            ("purpose", "TEXT NOT NULL"),
            ("region", "TEXT NOT NULL"),
            ("status", "TEXT NOT NULL"),
            ("confidence", "REAL NOT NULL"),
            ("effective", "INTEGER NOT NULL"),
            ("captured_at", "TEXT NOT NULL"),
        ),
    },
    {
        "table": "customer_360_communication_preference",
        "description": "Channel/topic preference records for standalone workbench edits.",
        "key_field": "preference_id",
        "columns": (
            ("preference_id", "TEXT PRIMARY KEY"),
            ("tenant", "TEXT NOT NULL"),
            ("profile_id", "TEXT NOT NULL"),
            ("channel", "TEXT NOT NULL"),
            ("topic", "TEXT NOT NULL"),
            ("status", "TEXT NOT NULL"),
            ("locale", "TEXT NOT NULL"),
            ("quiet_hours", "TEXT NOT NULL"),
            ("effective", "INTEGER NOT NULL"),
            ("updated_at", "TEXT NOT NULL"),
        ),
    },
    {
        "table": "customer_360_touchpoint",
        "description": "Captured touchpoints for timeline reconstruction.",
        "key_field": "touchpoint_id",
        "columns": (
            ("touchpoint_id", "TEXT PRIMARY KEY"),
            ("tenant", "TEXT NOT NULL"),
            ("profile_id", "TEXT NOT NULL"),
            ("channel", "TEXT NOT NULL"),
            ("source", "TEXT NOT NULL"),
            ("status", "TEXT NOT NULL"),
            ("occurred_at", "TEXT NOT NULL"),
            ("metadata", "TEXT NOT NULL"),
        ),
    },
    {
        "table": "customer_360_engagement_event",
        "description": "Engagement and projected inbox events used by timeline and workbench.",
        "key_field": "event_id",
        "columns": (
            ("event_id", "TEXT PRIMARY KEY"),
            ("tenant", "TEXT NOT NULL"),
            ("profile_id", "TEXT NOT NULL"),
            ("event_type", "TEXT NOT NULL"),
            ("channel", "TEXT NOT NULL"),
            ("value", "REAL NOT NULL"),
            ("sentiment", "REAL NOT NULL"),
            ("occurred_at", "TEXT NOT NULL"),
            ("metadata", "TEXT NOT NULL"),
        ),
    },
    {
        "table": "customer_360_profile_merge_case",
        "description": "Merge-review queue for duplicate profile remediation.",
        "key_field": "merge_case_id",
        "columns": (
            ("merge_case_id", "TEXT PRIMARY KEY"),
            ("tenant", "TEXT NOT NULL"),
            ("winning_profile_id", "TEXT NOT NULL"),
            ("candidate_profile_id", "TEXT NOT NULL"),
            ("match_score", "REAL NOT NULL"),
            ("reason", "TEXT NOT NULL"),
            ("status", "TEXT NOT NULL"),
            ("resolved_by", "TEXT"),
            ("created_at", "TEXT NOT NULL"),
            ("updated_at", "TEXT NOT NULL"),
        ),
    },
    {
        "table": "customer_360_appgen_outbox_event",
        "description": "AppGen-X emitted event queue for standalone package flows.",
        "key_field": "event_id",
        "columns": (
            ("event_id", "TEXT PRIMARY KEY"),
            ("event_type", "TEXT NOT NULL"),
            ("tenant", "TEXT NOT NULL"),
            ("payload", "TEXT NOT NULL"),
            ("status", "TEXT NOT NULL"),
            ("attempts", "INTEGER NOT NULL"),
            ("published_at", "TEXT NOT NULL"),
            ("idempotency_key", "TEXT NOT NULL UNIQUE"),
        ),
    },
    {
        "table": "customer_360_appgen_inbox_event",
        "description": "Idempotent AppGen-X inbox queue for consumed events.",
        "key_field": "event_id",
        "columns": (
            ("event_id", "TEXT PRIMARY KEY"),
            ("event_type", "TEXT NOT NULL"),
            ("handler", "TEXT NOT NULL"),
            ("payload", "TEXT NOT NULL"),
            ("attempts", "INTEGER NOT NULL"),
            ("status", "TEXT NOT NULL"),
            ("processed_at", "TEXT NOT NULL"),
        ),
    },
    {
        "table": "customer_360_dead_letter_event",
        "description": "Dead-letter evidence for unsupported or failed inbox events.",
        "key_field": "event_id",
        "columns": (
            ("event_id", "TEXT PRIMARY KEY"),
            ("event_type", "TEXT NOT NULL"),
            ("failure_reason", "TEXT NOT NULL"),
            ("payload", "TEXT NOT NULL"),
            ("attempts", "INTEGER NOT NULL"),
            ("failed_at", "TEXT NOT NULL"),
        ),
    },
)
_JSON_TEXT_COLUMNS = {"attributes", "evidence", "quiet_hours", "metadata", "payload"}
_STANDALONE_ALLOWED_CONSUMED_EVENTS = (
    "InvoiceIssued",
    "PaymentCaptured",
    "OrderVerified",
    "ServiceTicketClosed",
    "LoyaltyRewardEarned",
    "CandidateHired",
)


def standalone_model_contract() -> dict:
    tables = tuple(item["table"] for item in STANDALONE_SQLITE_TABLES)
    return {
        "format": "appgen.customer-360-standalone-model-contract.v1",
        "ok": bool(tables) and all(table.startswith(f"{PBC_KEY}_") for table in tables),
        "pbc": PBC_KEY,
        "development_database_backend": "sqlite",
        "deployment_database_backends": ("postgresql", "mysql", "mariadb"),
        "tables": STANDALONE_SQLITE_TABLES,
        "table_keys": tables,
        "event_tables": (
            "customer_360_appgen_outbox_event",
            "customer_360_appgen_inbox_event",
            "customer_360_dead_letter_event",
        ),
        "side_effects": (),
    }


def standalone_sqlite_schema() -> str:
    statements = []
    for table in STANDALONE_SQLITE_TABLES:
        columns = ",\n  ".join(f"{name} {column_type}" for name, column_type in table["columns"])
        statements.append(f"CREATE TABLE IF NOT EXISTS {table['table']} (\n  {columns}\n);")
    return "\n\n".join(statements)


def _standalone_timestamp() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _standalone_json(value: object) -> str:
    return json.dumps(value, sort_keys=True)


def _row_to_dict(row: sqlite3.Row | None) -> dict | None:
    if row is None:
        return None
    data = dict(row)
    for key in tuple(data):
        if key in _JSON_TEXT_COLUMNS and isinstance(data[key], str):
            try:
                data[key] = json.loads(data[key])
            except json.JSONDecodeError:
                continue
        if key in {"verified", "effective"} and data[key] is not None:
            data[key] = bool(data[key])
    return data


class Customer360StandaloneStore:
    """SQLite-backed standalone store for the package-local one-PBC app."""

    def __init__(self, database_path: str = ":memory:", connection: sqlite3.Connection | None = None):
        self.database_path = database_path
        self.connection = connection or sqlite3.connect(database_path)
        self.connection.row_factory = sqlite3.Row
        self._ensure_schema()

    def close(self) -> None:
        self.connection.close()

    def _ensure_schema(self) -> None:
        self.connection.executescript(standalone_sqlite_schema())
        self.connection.commit()

    def _query_one(self, sql: str, params: tuple = ()) -> dict | None:
        return _row_to_dict(self.connection.execute(sql, params).fetchone())

    def _query_all(self, sql: str, params: tuple = ()) -> tuple[dict, ...]:
        rows = self.connection.execute(sql, params).fetchall()
        return tuple(_row_to_dict(row) for row in rows if row is not None)

    def _upsert(self, table: str, key_field: str, record: dict) -> str:
        existing = self._query_one(
            f"SELECT {key_field} FROM {table} WHERE {key_field} = ?",
            (record[key_field],),
        )
        if existing:
            columns = [column for column in record if column != key_field]
            assignments = ", ".join(f"{column} = ?" for column in columns)
            values = tuple(record[column] for column in columns) + (record[key_field],)
            self.connection.execute(
                f"UPDATE {table} SET {assignments} WHERE {key_field} = ?",
                values,
            )
            action = "updated"
        else:
            columns = tuple(record)
            placeholders = ", ".join("?" for _ in columns)
            self.connection.execute(
                f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})",
                tuple(record[column] for column in columns),
            )
            action = "created"
        self.connection.commit()
        return action

    def _append_outbox(self, event_type: str, tenant: str, payload: dict, *, key: str) -> dict:
        now = _standalone_timestamp()
        record = {
            "event_id": key,
            "event_type": event_type,
            "tenant": tenant,
            "payload": _standalone_json(payload),
            "status": "pending",
            "attempts": 0,
            "published_at": now,
            "idempotency_key": key,
        }
        self._upsert("customer_360_appgen_outbox_event", "event_id", record)
        return record

    def create_profile(self, payload: dict) -> dict:
        required = ("profile_id", "tenant", "display_name", "region")
        missing = tuple(field for field in required if not payload.get(field))
        if missing:
            return {"ok": False, "reason": "missing_fields", "missing": missing}
        now = _standalone_timestamp()
        core_fields = {"profile_id", "tenant", "display_name", "region", "lifecycle_state", "account_type"}
        record = {
            "profile_id": payload["profile_id"],
            "tenant": payload["tenant"],
            "display_name": payload["display_name"],
            "region": payload["region"],
            "lifecycle_state": payload.get("lifecycle_state", "active"),
            "account_type": payload.get("account_type", "consumer"),
            "attributes": _standalone_json(
                {key: value for key, value in payload.items() if key not in core_fields}
            ),
            "created_at": payload.get("created_at", now),
            "updated_at": now,
        }
        action = self._upsert("customer_360_customer_profile", "profile_id", record)
        self._append_outbox(
            "CustomerUpdated",
            payload["tenant"],
            {"profile_id": payload["profile_id"], "region": payload["region"]},
            key=f"customer_360:profile:{payload['profile_id']}",
        )
        return {"ok": True, "action": action, "profile": self.get_profile(payload["profile_id"])}

    def get_profile(self, profile_id: str) -> dict | None:
        return self._query_one(
            "SELECT * FROM customer_360_customer_profile WHERE profile_id = ?",
            (profile_id,),
        )

    def list_profiles(self, tenant: str) -> tuple[dict, ...]:
        return self._query_all(
            "SELECT * FROM customer_360_customer_profile WHERE tenant = ? ORDER BY profile_id",
            (tenant,),
        )

    def link_identity(self, payload: dict) -> dict:
        required = ("identity_id", "tenant", "profile_id", "identity_type", "value")
        missing = tuple(field for field in required if not payload.get(field))
        if missing:
            return {"ok": False, "reason": "missing_fields", "missing": missing}
        if not self.get_profile(payload["profile_id"]):
            return {"ok": False, "reason": "profile_not_found", "profile_id": payload["profile_id"]}
        record = {
            "identity_id": payload["identity_id"],
            "tenant": payload["tenant"],
            "profile_id": payload["profile_id"],
            "identity_type": payload["identity_type"],
            "identity_value_hash": hashlib.sha256(str(payload["value"]).encode("utf-8")).hexdigest(),
            "confidence": float(payload.get("confidence", 0.0)),
            "verified": int(bool(payload.get("verified", False))),
            "evidence": _standalone_json(payload.get("evidence", {"source": "standalone_form"})),
            "linked_at": payload.get("linked_at", _standalone_timestamp()),
        }
        action = self._upsert("customer_360_customer_identity", "identity_id", record)
        self._append_outbox(
            "CustomerIdentityLinked",
            payload["tenant"],
            {"profile_id": payload["profile_id"], "identity_type": payload["identity_type"]},
            key=f"customer_360:identity:{payload['identity_id']}",
        )
        identity = self._query_one(
            "SELECT * FROM customer_360_customer_identity WHERE identity_id = ?",
            (payload["identity_id"],),
        )
        return {"ok": True, "action": action, "identity": identity}

    def record_consent(self, payload: dict) -> dict:
        required = ("consent_id", "tenant", "profile_id", "purpose", "region", "status")
        missing = tuple(field for field in required if not payload.get(field))
        if missing:
            return {"ok": False, "reason": "missing_fields", "missing": missing}
        effective = payload["status"] == "granted" and float(payload.get("confidence", 0.0)) >= 0.9
        record = {
            "consent_id": payload["consent_id"],
            "tenant": payload["tenant"],
            "profile_id": payload["profile_id"],
            "purpose": payload["purpose"],
            "region": payload["region"],
            "status": payload["status"],
            "confidence": float(payload.get("confidence", 0.0)),
            "effective": int(effective),
            "captured_at": payload.get("captured_at", _standalone_timestamp()),
        }
        action = self._upsert("customer_360_consent_record", "consent_id", record)
        self._append_outbox(
            "ConsentRecorded",
            payload["tenant"],
            {"profile_id": payload["profile_id"], "purpose": payload["purpose"], "status": payload["status"]},
            key=f"customer_360:consent:{payload['consent_id']}",
        )
        consent = self._query_one(
            "SELECT * FROM customer_360_consent_record WHERE consent_id = ?",
            (payload["consent_id"],),
        )
        return {"ok": True, "action": action, "consent": consent}

    def set_preference(self, payload: dict) -> dict:
        required = ("preference_id", "tenant", "profile_id", "channel", "topic", "status")
        missing = tuple(field for field in required if not payload.get(field))
        if missing:
            return {"ok": False, "reason": "missing_fields", "missing": missing}
        effective = payload["status"] == "opt_in"
        record = {
            "preference_id": payload["preference_id"],
            "tenant": payload["tenant"],
            "profile_id": payload["profile_id"],
            "channel": payload["channel"],
            "topic": payload["topic"],
            "status": payload["status"],
            "locale": payload.get("locale", "en-US"),
            "quiet_hours": _standalone_json(payload.get("quiet_hours", {"start": "22:00", "end": "07:00"})),
            "effective": int(effective),
            "updated_at": payload.get("updated_at", _standalone_timestamp()),
        }
        action = self._upsert("customer_360_communication_preference", "preference_id", record)
        self._append_outbox(
            "PreferenceChanged",
            payload["tenant"],
            {"profile_id": payload["profile_id"], "channel": payload["channel"], "topic": payload["topic"]},
            key=f"customer_360:preference:{payload['preference_id']}",
        )
        preference = self._query_one(
            "SELECT * FROM customer_360_communication_preference WHERE preference_id = ?",
            (payload["preference_id"],),
        )
        return {"ok": True, "action": action, "preference": preference}

    def capture_touchpoint(self, payload: dict) -> dict:
        required = ("touchpoint_id", "tenant", "profile_id", "channel", "source")
        missing = tuple(field for field in required if not payload.get(field))
        if missing:
            return {"ok": False, "reason": "missing_fields", "missing": missing}
        record = {
            "touchpoint_id": payload["touchpoint_id"],
            "tenant": payload["tenant"],
            "profile_id": payload["profile_id"],
            "channel": payload["channel"],
            "source": payload["source"],
            "status": payload.get("status", "captured"),
            "occurred_at": payload.get("occurred_at", _standalone_timestamp()),
            "metadata": _standalone_json(payload.get("metadata", {})),
        }
        action = self._upsert("customer_360_touchpoint", "touchpoint_id", record)
        self._append_outbox(
            "TouchpointCaptured",
            payload["tenant"],
            {"profile_id": payload["profile_id"], "channel": payload["channel"]},
            key=f"customer_360:touchpoint:{payload['touchpoint_id']}",
        )
        touchpoint = self._query_one(
            "SELECT * FROM customer_360_touchpoint WHERE touchpoint_id = ?",
            (payload["touchpoint_id"],),
        )
        return {"ok": True, "action": action, "touchpoint": touchpoint}

    def ingest_engagement_event(self, payload: dict, *, emit_outbox: bool = True) -> dict:
        required = ("event_id", "tenant", "profile_id", "event_type", "channel")
        missing = tuple(field for field in required if not payload.get(field))
        if missing:
            return {"ok": False, "reason": "missing_fields", "missing": missing}
        record = {
            "event_id": payload["event_id"],
            "tenant": payload["tenant"],
            "profile_id": payload["profile_id"],
            "event_type": payload["event_type"],
            "channel": payload["channel"],
            "value": float(payload.get("value", 0.0)),
            "sentiment": float(payload.get("sentiment", 0.0)),
            "occurred_at": payload.get("occurred_at", _standalone_timestamp()),
            "metadata": _standalone_json(payload.get("metadata", {})),
        }
        action = self._upsert("customer_360_engagement_event", "event_id", record)
        if emit_outbox:
            self._append_outbox(
                "CustomerSegmentUpdated",
                payload["tenant"],
                {"profile_id": payload["profile_id"], "event_type": payload["event_type"]},
                key=f"customer_360:engagement:{payload['event_id']}",
            )
        engagement = self._query_one(
            "SELECT * FROM customer_360_engagement_event WHERE event_id = ?",
            (payload["event_id"],),
        )
        return {"ok": True, "action": action, "engagement": engagement}

    def open_merge_case(self, payload: dict) -> dict:
        required = (
            "merge_case_id",
            "tenant",
            "winning_profile_id",
            "candidate_profile_id",
            "match_score",
            "reason",
        )
        missing = tuple(field for field in required if payload.get(field) in (None, ""))
        if missing:
            return {"ok": False, "reason": "missing_fields", "missing": missing}
        now = _standalone_timestamp()
        record = {
            "merge_case_id": payload["merge_case_id"],
            "tenant": payload["tenant"],
            "winning_profile_id": payload["winning_profile_id"],
            "candidate_profile_id": payload["candidate_profile_id"],
            "match_score": float(payload["match_score"]),
            "reason": payload["reason"],
            "status": payload.get("status", "open"),
            "resolved_by": payload.get("resolved_by"),
            "created_at": payload.get("created_at", now),
            "updated_at": now,
        }
        action = self._upsert("customer_360_profile_merge_case", "merge_case_id", record)
        self._append_outbox(
            "ProfileMergeCaseOpened",
            payload["tenant"],
            {"merge_case_id": payload["merge_case_id"], "winning_profile_id": payload["winning_profile_id"]},
            key=f"customer_360:merge:{payload['merge_case_id']}:open",
        )
        merge_case = self._query_one(
            "SELECT * FROM customer_360_profile_merge_case WHERE merge_case_id = ?",
            (payload["merge_case_id"],),
        )
        return {"ok": True, "action": action, "merge_case": merge_case}

    def resolve_merge_case(self, merge_case_id: str, resolved_by: str) -> dict:
        merge_case = self._query_one(
            "SELECT * FROM customer_360_profile_merge_case WHERE merge_case_id = ?",
            (merge_case_id,),
        )
        if not merge_case:
            return {"ok": False, "reason": "merge_case_not_found", "merge_case_id": merge_case_id}
        self.connection.execute(
            """
            UPDATE customer_360_profile_merge_case
            SET status = ?, resolved_by = ?, updated_at = ?
            WHERE merge_case_id = ?
            """,
            ("resolved", resolved_by, _standalone_timestamp(), merge_case_id),
        )
        self.connection.commit()
        self._append_outbox(
            "ProfileMergeResolved",
            merge_case["tenant"],
            {"merge_case_id": merge_case_id, "resolved_by": resolved_by},
            key=f"customer_360:merge:{merge_case_id}:resolved",
        )
        return {
            "ok": True,
            "merge_case": self._query_one(
                "SELECT * FROM customer_360_profile_merge_case WHERE merge_case_id = ?",
                (merge_case_id,),
            ),
        }

    def receive_event(self, payload: dict) -> dict:
        event_id = payload.get("event_id")
        event_type = payload.get("event_type")
        data = dict(payload.get("payload") or {})
        if not event_id or not event_type:
            return {"ok": False, "reason": "missing_event_identity"}
        existing = self._query_one(
            "SELECT event_id, status, attempts FROM customer_360_appgen_inbox_event WHERE event_id = ?",
            (event_id,),
        )
        if existing and existing["status"] == "processed":
            return {"ok": True, "duplicate": True, "event_id": event_id, "status": existing["status"]}
        now = _standalone_timestamp()
        attempts = int(existing["attempts"]) + 1 if existing else 1
        retry_limit = 3
        if event_type not in _STANDALONE_ALLOWED_CONSUMED_EVENTS or not data:
            status = "dead_letter" if attempts >= retry_limit else "retrying"
            inbox = {
                "event_id": event_id,
                "event_type": event_type,
                "handler": f"handle_{str(event_type).lower()}",
                "payload": _standalone_json(data),
                "attempts": attempts,
                "status": status,
                "processed_at": now,
            }
            self._upsert("customer_360_appgen_inbox_event", "event_id", inbox)
            if status == "dead_letter":
                dead_letter = {
                    "event_id": event_id,
                    "event_type": event_type,
                    "failure_reason": "unsupported_or_missing_payload",
                    "payload": _standalone_json(data),
                    "attempts": attempts,
                    "failed_at": now,
                }
                self._upsert("customer_360_dead_letter_event", "event_id", dead_letter)
                return {"ok": False, "duplicate": False, "status": "dead_letter", "event": dead_letter, "attempts": attempts}
            return {"ok": False, "duplicate": False, "status": "retrying", "event": inbox, "attempts": attempts}
        inbox = {
            "event_id": event_id,
            "event_type": event_type,
            "handler": f"handle_{event_type.lower()}",
            "payload": _standalone_json(data),
            "attempts": attempts,
            "status": "processed",
            "processed_at": now,
        }
        self._upsert("customer_360_appgen_inbox_event", "event_id", inbox)
        if data.get("profile_id"):
            self.ingest_engagement_event(
                {
                    "event_id": f"inbox_{event_id}",
                    "tenant": data.get("tenant", "tenant_default"),
                    "profile_id": data["profile_id"],
                    "event_type": event_type,
                    "channel": "appgen_inbox",
                    "value": data.get("amount", 0.0),
                    "sentiment": 0.0,
                    "metadata": {"source_event_id": event_id},
                    "occurred_at": data.get("occurred_at", now),
                },
                emit_outbox=False,
            )
        return {"ok": True, "duplicate": False, "status": "processed", "event_id": event_id, "attempts": attempts}

    def build_timeline(self, profile_id: str) -> dict:
        touchpoints = self._query_all(
            "SELECT touchpoint_id AS entry_id, occurred_at, channel, source, status, metadata FROM customer_360_touchpoint WHERE profile_id = ?",
            (profile_id,),
        )
        engagements = self._query_all(
            "SELECT event_id AS entry_id, occurred_at, channel, event_type, value, sentiment, metadata FROM customer_360_engagement_event WHERE profile_id = ?",
            (profile_id,),
        )
        consents = self._query_all(
            "SELECT consent_id AS entry_id, captured_at AS occurred_at, purpose, status, effective FROM customer_360_consent_record WHERE profile_id = ?",
            (profile_id,),
        )
        preferences = self._query_all(
            "SELECT preference_id AS entry_id, updated_at AS occurred_at, channel, topic, status, effective FROM customer_360_communication_preference WHERE profile_id = ?",
            (profile_id,),
        )
        entries = tuple(
            sorted(
                (
                    *({"kind": "touchpoint", **row} for row in touchpoints),
                    *({"kind": "engagement", **row} for row in engagements),
                    *({"kind": "consent", **row} for row in consents),
                    *({"kind": "preference", **row} for row in preferences),
                ),
                key=lambda row: row["occurred_at"],
                reverse=True,
            )
        )
        return {"ok": True, "profile_id": profile_id, "entries": entries, "event_count": len(entries)}

    def build_workbench(self, tenant: str) -> dict:
        counts = {
            "profile_count": self.connection.execute(
                "SELECT COUNT(*) FROM customer_360_customer_profile WHERE tenant = ?",
                (tenant,),
            ).fetchone()[0],
            "identity_count": self.connection.execute(
                "SELECT COUNT(*) FROM customer_360_customer_identity WHERE tenant = ?",
                (tenant,),
            ).fetchone()[0],
            "consent_count": self.connection.execute(
                "SELECT COUNT(*) FROM customer_360_consent_record WHERE tenant = ?",
                (tenant,),
            ).fetchone()[0],
            "effective_consent_count": self.connection.execute(
                "SELECT COUNT(*) FROM customer_360_consent_record WHERE tenant = ? AND effective = 1",
                (tenant,),
            ).fetchone()[0],
            "preference_count": self.connection.execute(
                "SELECT COUNT(*) FROM customer_360_communication_preference WHERE tenant = ?",
                (tenant,),
            ).fetchone()[0],
            "opt_in_count": self.connection.execute(
                "SELECT COUNT(*) FROM customer_360_communication_preference WHERE tenant = ? AND effective = 1",
                (tenant,),
            ).fetchone()[0],
            "touchpoint_count": self.connection.execute(
                "SELECT COUNT(*) FROM customer_360_touchpoint WHERE tenant = ?",
                (tenant,),
            ).fetchone()[0],
            "engagement_event_count": self.connection.execute(
                "SELECT COUNT(*) FROM customer_360_engagement_event WHERE tenant = ?",
                (tenant,),
            ).fetchone()[0],
            "open_merge_case_count": self.connection.execute(
                "SELECT COUNT(*) FROM customer_360_profile_merge_case WHERE tenant = ? AND status != 'resolved'",
                (tenant,),
            ).fetchone()[0],
            "outbox_count": self.connection.execute(
                "SELECT COUNT(*) FROM customer_360_appgen_outbox_event WHERE tenant = ?",
                (tenant,),
            ).fetchone()[0],
        }
        inbox_count = self.connection.execute(
            "SELECT COUNT(*) FROM customer_360_appgen_inbox_event",
        ).fetchone()[0]
        dead_letter_count = self.connection.execute(
            "SELECT COUNT(*) FROM customer_360_dead_letter_event",
        ).fetchone()[0]
        customer_value = self.connection.execute(
            "SELECT COALESCE(SUM(value), 0) FROM customer_360_engagement_event WHERE tenant = ?",
            (tenant,),
        ).fetchone()[0]
        return {
            "ok": True,
            "tenant": tenant,
            **counts,
            "customer_value": round(float(customer_value or 0.0), 2),
            "inbox_count": inbox_count,
            "dead_letter_count": dead_letter_count,
            "profiles": self.list_profiles(tenant),
        }


def standalone_store_smoke_test() -> dict:
    store = Customer360StandaloneStore()
    try:
        profile = store.create_profile(
            {
                "profile_id": "cust_smoke",
                "tenant": "tenant_smoke",
                "display_name": "Smoke Customer",
                "region": "US",
            }
        )
        identity = store.link_identity(
            {
                "identity_id": "id_smoke",
                "tenant": "tenant_smoke",
                "profile_id": "cust_smoke",
                "identity_type": "email",
                "value": "smoke@example.com",
                "confidence": 0.97,
                "verified": True,
            }
        )
        consent = store.record_consent(
            {
                "consent_id": "consent_smoke",
                "tenant": "tenant_smoke",
                "profile_id": "cust_smoke",
                "purpose": "marketing",
                "region": "US",
                "status": "granted",
                "confidence": 0.95,
            }
        )
        preference = store.set_preference(
            {
                "preference_id": "pref_smoke",
                "tenant": "tenant_smoke",
                "profile_id": "cust_smoke",
                "channel": "email",
                "topic": "offers",
                "status": "opt_in",
            }
        )
        touchpoint = store.capture_touchpoint(
            {
                "touchpoint_id": "tp_smoke",
                "tenant": "tenant_smoke",
                "profile_id": "cust_smoke",
                "channel": "web",
                "source": "portal",
            }
        )
        engagement = store.ingest_engagement_event(
            {
                "event_id": "eng_smoke",
                "tenant": "tenant_smoke",
                "profile_id": "cust_smoke",
                "event_type": "purchase",
                "channel": "web",
                "value": 125.0,
            }
        )
        inbox = store.receive_event(
            {
                "event_id": "evt_smoke",
                "event_type": "InvoiceIssued",
                "payload": {
                    "tenant": "tenant_smoke",
                    "profile_id": "cust_smoke",
                    "amount": 125.0,
                },
            }
        )
        timeline = store.build_timeline("cust_smoke")
        workbench = store.build_workbench("tenant_smoke")
        return {
            "ok": all(
                result.get("ok") is True
                for result in (profile, identity, consent, preference, touchpoint, engagement, inbox, timeline, workbench)
            )
            and timeline["event_count"] >= 4
            and workbench["profile_count"] == 1
            and workbench["outbox_count"] >= 5,
            "contract": standalone_model_contract(),
            "profile": profile,
            "timeline": timeline,
            "workbench": workbench,
            "side_effects": (),
        }
    finally:
        store.close()
